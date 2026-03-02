import cv2 as cv
import numpy as np
import os
import cv2

#############################################################################################################################
#############################################################################################################################

# Field HSV range
lower_field = np.array([19, 192, 105])
upper_field = np.array([34, 255, 206])

#############################################################################################################################
#############################################################################################################################
def main():

    def get_tiles(brikker):
        tiles = []
        for y in range(5):
            tiles.append([])
            for x in range(5):
                tiles[-1].append(brikker[y*100:(y+1)*100, x*100:(x+1)*100])
        return tiles

    # Find script directory og parent directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    # Opret mappe til at gemme field felter
    output_folder = os.path.join(parent_dir, "felter billeder", "Feilds")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop gennem alle billeder 1-74
    for i in range(25, 75):
        filename = os.path.join(parent_dir, f"{i}.jpg")
        print(f"\n=== Processing {i}.jpg ===")
        
        brikker = cv2.imread(filename)
        
        if brikker is None:
            print(f"  Kunne ikke indlæse {filename}, springer over")
            continue
        
        brikker_original = brikker.copy()  # Gem kopi af original

        tiles = get_tiles(brikker)

        for y in range(5):
            for x in range(5):
                tile = tiles[y][x]

                tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
                tile_mask = cv2.inRange(tile_hsv, lower_field, upper_field)

                # Efter masken er lavet:
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
                tile_mask = cv2.morphologyEx(tile_mask, cv2.MORPH_OPEN, kernel)  # Fjern små prikker
                tile_mask = cv2.morphologyEx(tile_mask, cv2.MORPH_CLOSE, kernel)  # Fyld små huller

                yellow_pixels = cv2.countNonZero(tile_mask)
                
                # Beregn procentdel i stedet for absolut antal
                tile_total_pixels = tile.shape[0] * tile.shape[1]
                yellow_percentage = (yellow_pixels / tile_total_pixels) * 100
                
                print(f"Tile ({y},{x}) gule pixels: {yellow_pixels} ({yellow_percentage:.1f}%)")
                
                # Filtrer hvis > 30% af tile er gul
                if yellow_percentage > 20:  
                    # Dette ER et field-felt, gem det
                    output_filename = f"{output_folder}/field_{i}_{y}_{x}.jpg"
                    cv2.imwrite(output_filename, tile)
                    print(f"  -> Gemt som field_{i}_{y}_{x}.jpg")
                else:
                    tiles[y][x][:] = 0  # Ikke et field, gør sort

        # Saml det filtrerede board igen
        result = brikker.copy()
        for y in range(5):
            for x in range(5):
                result[y*100:(y+1)*100, x*100:(x+1)*100] = tiles[y][x]

        # Vis original og filtreret i separate vinduer
        cv2.imshow("Original", brikker_original)
        cv2.imshow("Filtreret", result)
        
        print("\nTryk ESC for næste billede...")
        while True:
            key = cv2.waitKey(0)
            if key == 27:  # ESC tast
                cv2.destroyAllWindows()
                break

    print(f"\n✓ Færdig! Field-felter gemt i: {output_folder}")
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


#############################################################################################################################
#############################################################################################################################