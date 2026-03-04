import cv2
import numpy as np
import os

#############################################################################################################################
# FOREST DETECTION MED BLOB DETECTION:
# Forest har et karakteristisk mønster med mange små mørke træblobs
# Vi bruger blob detection til at identificere og tælle træer
# Forest = mange blobs (10-30 træer per tile)
# Grass = ingen/få blobs (homogen overflade)
#############################################################################################################################

def detect_forest_blobs(tile):
    """
    Detekterer forest baseret på blob-mønster + farve backup
    Returnerer antal blobs og om det er forest
    """
    # Convert til HSV
    tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
    
    # Beregn gennemsnitlig V (brightness) for at ekskludere for lyse felter
    avg_v = np.mean(tile_hsv[:,:,2])
    
    # Hvis feltet er for lyst, er det ikke forest (grass er typisk lysere)
    if avg_v > 100:  # Lysintensitet threshold
        return 0, 0, False, np.zeros((tile.shape[0], tile.shape[1]), dtype=np.uint8)
    
    # Find MØRKE grønne områder (træer)
    # Forest træer baseret på mean HSV værdier: H=28-78, S=68-239, V=25-128
    lower_tree = np.array([28, 68, 25])
    upper_tree = np.array([78, 239, 128])
    
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
    # 1. Mindst 1 blob OG tree% > 10% (MEGET lavt krav - fanger næsten alt)
    # 2. ELLER tree% > 25% selv uden blobs (mørk grøn area)
    # 3. ELLER mange blobs (>= 5) uanset tree% (mange små træer)
    
    cond1 = (num_blobs >= 1 and tree_percentage > 10)
    cond2 = (tree_percentage > 42)
    cond3 = (num_blobs >= 5)
    
    is_forest = cond1 or cond2 or cond3
    
    return num_blobs, tree_percentage, is_forest, tree_mask

def main():
    
    # Find script directory og parent directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    # Opret mappe til at gemme forest felter
    output_folder = os.path.join(parent_dir, "felter billeder", "Forest")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i in range(56, 74): 
        filename = os.path.join(parent_dir, f"{i}.jpg")
        print(f"\n=== Processing {filename} ===")

        brikker = cv2.imread(filename)
        
        if brikker is None:
            print(f"  Kunne ikke indlæse {filename}, springer over")
            continue
            
        cv2.imshow("originale", brikker)

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
                num_blobs, tree_pct, is_forest, tree_mask = detect_forest_blobs(tile)
                
                # Beregn og vis lysintensitet
                tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
                avg_v = np.mean(tile_hsv[:,:,2])
                
                print(f"Tile ({y},{x}): lys={avg_v:.1f}, blobs={num_blobs}, tree%={tree_pct:.1f}%, forest={is_forest}")
                
                # Hvis ikke forest, gør tile sort
                if not is_forest:
                    tiles[y][x][:] = 0

        # Saml boardet igen
        final_result = brikker.copy()
        for y in range(5):
            for x in range(5):
                final_result[y*100:(y+1)*100, x*100:(x+1)*100] = tiles[y][x]

        # Gem forest tiles
        for y in range(5):
            for x in range(5):
                tile = tiles[y][x]
                
                # Tjek om tile ikke er helt sort
                if np.sum(tile) > 0:
                    output_filename = os.path.join(output_folder, f"forest_{i}_{y}_{x}.jpg")
                    cv2.imwrite(output_filename, tile)
                    print(f"  ✓ Saved: forest_{i}_{y}_{x}.jpg")

        cv2.imshow("Forest Detection", final_result)

        key = cv2.waitKey(0)

        if key == 27:  # ESC
            cv2.destroyWindow("Forest Detection")
            cv2.destroyWindow("originale")
            continue

    print(f"\n✓ Færdig! Forest-felter gemt i: {output_folder}")
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()