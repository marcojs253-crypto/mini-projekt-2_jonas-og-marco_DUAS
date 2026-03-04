import cv2
import numpy as np
import os

def detect_forest_blobs(tile):
    """
    Detekterer forest baseret på blob-mønster + farve backup
    Returnerer antal blobs og om det er forest
    """
    # Convert til HSV
    tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
    
    # Beregn gennemsnitlig V (brightness) for at ekskludere grass
    avg_v = np.mean(tile_hsv[:,:,2])
    
    # Find MØRKE grønne områder (træer)
    # Forest træer er mørke: H=30-55, S>100, V=20-70
    lower_tree = np.array([30, 100, 20])
    upper_tree = np.array([55, 255, 70])
    
    tree_mask = cv2.inRange(tile_hsv, lower_tree, upper_tree)
    
    # Morphological operations for at rense støj
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    tree_mask = cv2.morphologyEx(tree_mask, cv2.MORPH_OPEN, kernel_small)
    tree_mask = cv2.morphologyEx(tree_mask, cv2.MORPH_CLOSE, kernel_small)
    
    # Setup SimpleBlobDetector parameters (lempeligere)
    params = cv2.SimpleBlobDetector_Params()
    
    # Filter by Area
    params.filterByArea = True
    params.minArea = 10        # Mindre minimum
    params.maxArea = 600       # Større maximum
    
    # Filter by Circularity (mere lempeligt)
    params.filterByCircularity = True
    params.minCircularity = 0.2  # Lavere krav
    
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.3    # Lavere krav
    
    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.1  # Lavere krav
    
    # Opret detector
    detector = cv2.SimpleBlobDetector_create(params)
    
    # Inverter maske (blob detector leder efter lyse blobs på mørk baggrund)
    tree_mask_inv = cv2.bitwise_not(tree_mask)
    
    # Detekter blobs
    keypoints = detector.detect(tree_mask_inv)
    num_blobs = len(keypoints)
    
    # Beregn hvor meget af tile der er mørk grøn
    tree_pixels = cv2.countNonZero(tree_mask)
    total_pixels = tile.shape[0] * tile.shape[1]
    tree_percentage = (tree_pixels / total_pixels) * 100
    
    # MEGET LEMPELIG APPROACH FOR HØJ RECALL:
    # Prioriter at fange ALLE forest tiles (accepter false positives)
    # Forest hvis:
    # 1. Mindst 1 blob OG tree% > 15% (træer med god coverage)
    # 2. ELLER tree% > 30% selv uden blobs (mørk grøn area)
    # 3. ELLER mange blobs (>= 5) uanset tree% (mange små træer)
    
    cond1 = (num_blobs >= 1 and tree_percentage > 15)
    cond2 = (tree_percentage > 30)
    cond3 = (num_blobs >= 5)
    
    is_forest = cond1 or cond2 or cond3
    
    return num_blobs, tree_percentage, is_forest, tree_mask, avg_v

# Find script directory og parent directory
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

# Load image 42
filename = os.path.join(parent_dir, "42.jpg")
print(f"=== Analyserer {filename} ===\n")

brikker = cv2.imread(filename)

def get_tiles(image):
    tiles = []
    for y in range(5):
        tiles.append([])
        for x in range(5):
            tiles[-1].append(image[y*100:(y+1)*100, x*100:(x+1)*100])
    return tiles

tiles = get_tiles(brikker)

for y in range(5):
    for x in range(5):
        tile = tiles[y][x]
        
        # Brug blob detection til at identificere forest
        num_blobs, tree_pct, is_forest, tree_mask, avg_v = detect_forest_blobs(tile)
        
        print(f"Tile ({y},{x}): blobs={num_blobs}, tree%={tree_pct:.1f}%, avg_v={avg_v:.1f}, forest={is_forest}")
        
        # Special attention to tile (1,2)
        if y == 1 and x == 2:
            print(f"  >>> TILE (1,2) DETALJER:")
            print(f"      Condition 1 (blobs>=1 AND tree%>15): {num_blobs >= 1} AND {tree_pct > 15} = {num_blobs >= 1 and tree_pct > 15}")
            print(f"      Condition 2 (tree%>30): {tree_pct > 30}")
            print(f"      Condition 3 (blobs>=5): {num_blobs >= 5}")
            print(f"      IS_FOREST: {is_forest}")
            
            # Vis tile
            cv2.imshow("Tile (1,2)", tile)
            cv2.imshow("Tile (1,2) Tree Mask", tree_mask)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
