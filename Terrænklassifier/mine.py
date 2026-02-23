import cv2
import numpy as np

#############################################################################################################################
#############################################################################################################################





#############################################################################################################################
#############################################################################################################################

def main():
    for i in range(1, 74): 

        filename = f"{i}.jpg"
        print(f"Processing {filename}")

        brikker = cv2.imread(filename)
        cv2.imshow("originale", brikker)
       # Convert BGR to HSV
        brikker_hsv = cv2.cvtColor(brikker, cv2.COLOR_BGR2HSV)

            # Forest-brik range
        lower_mine = np.array([0, 0, 0])
        upper_mine = np.array([200, 40, 74])

        # Lav maske (hvid = pixels indenfor range)
        mask_mine = cv2.inRange(brikker_hsv, lower_mine, upper_mine)

            # Behold KUN pixels i masken
        result_mine = cv2.bitwise_and(brikker, brikker, mask=mask_mine)
        filename = f"{i}.jpg"
        print(f"Processing {filename}") 
        def get_tiles(brikker):
                tiles = []
                for y in range(5):
                    tiles.append([])
                    for x in range(5):
                        tiles[-1].append(brikker[y*100:(y+1)*100, x*100:(x+1)*100])
                return tiles

        tiles = get_tiles(brikker)

        for y in range(5):
                for x in range(5):
                    tile = tiles[y][x]

                    tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
                    tile_mask = cv2.inRange(tile_hsv, lower_mine, upper_mine)

                    black_pixels = cv2.countNonZero(tile_mask)
                    print(f"Tile ({y},{x}) black pixels: {black_pixels}")

                    if black_pixels < 462 :
                        tiles[y][x][:] = 0  # gør tile sort


            # Saml boardet igen
        result = brikker.copy()
        for y in range(5):
                for x in range(5):
                    result[y*100:(y+1)*100, x*100:(x+1)*100] = tiles[y][x]
########################################################################################################################### 
            # ---------- STEP 2: Find mine via gul farve ----------

        
            
            # Forest-brik range
        lower_yellow = np.array([20, 19, 35])
        upper_yellow = np.array([35, 255, 255])

            # Lav maske (hvid = pixels indenfor range)
        mask_mine_yellow = cv2.inRange(result, lower_yellow, upper_yellow)

            # Behold KUN pixels i masken
        result_mine = cv2.bitwise_and(result, result, mask=mask_mine_yellow)

            
        def y_get_tiles(result):
                tiles = []
                for y in range(5):
                    tiles.append([])
                    for x in range(5):
                        tiles[-1].append(result[y*100:(y+1)*100, x*100:(x+1)*100])
                return tiles

        tiles = y_get_tiles(result)

        for y in range(5):
                for x in range(5):
                    tile = tiles[y][x]

                    tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
                    tile_mask = cv2.inRange(tile_hsv, lower_yellow, upper_yellow)

                    Yellow_pixels = cv2.countNonZero(tile_mask)
                    print(f"Tile ({y},{x}) Yellow pixels: {Yellow_pixels}")

                    if  5000 < Yellow_pixels :
                        tiles[y][x][:] = 0  # gør tile sort
                    if  1500 > Yellow_pixels :
                        tiles[y][x][:] = 0  # gør tile sort


        # Saml boardet igen
        y_result = result.copy()
        for y in range(5):
            for x in range(5):
                result[y*100:(y+1)*100, x*100:(x+1)*100] = tiles[y][x]
        
       
###########################################################################################################################    
        # ---------- STEP 2: Find mine via gul farve ----------

        
            
            # Forest-brik range
        lower_Brown = np.array([0, 3, 0])
        upper_Brown = np.array([31, 101, 38])

            # Lav maske (hvid = pixels indenfor range)
        mask_mine_Brown = cv2.inRange(y_result, lower_Brown, upper_Brown)

            # Behold KUN pixels i masken
        result_mine = cv2.bitwise_and(y_result, y_result, mask=mask_mine_Brown)

            
        def b_get_tiles(y_result):
                tiles = []
                for y in range(5):
                    tiles.append([])
                    for x in range(5):
                        tiles[-1].append(y_result[y*100:(y+1)*100, x*100:(x+1)*100])
                return tiles

        tiles = b_get_tiles(y_result)

        for y in range(5):
                for x in range(5):
                    tile = tiles[y][x]

                    tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
                    tile_mask = cv2.inRange(tile_hsv, lower_Brown, upper_Brown)

                    Yellow_pixels = cv2.countNonZero(tile_mask)

                    hsv_tile = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
                    hue, saturation, value = np.median(hsv_tile, axis=(0, 1))
                    # print(f"H: {hue}, S: {saturation}, V: {value}")

                    if  Yellow_pixels < 618 :
                        tiles[y][x][:] = 0  # gør tile sort
                        
                    
        for y in range(5):
                for x in range(5):
                    tile = tiles[y][x]

                    tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
                    tile_mask = cv2.inRange(tile_hsv, lower_Brown, upper_Brown)

                    Yellow_pixels = cv2.countNonZero(tile_mask)

                    hsv_tile = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
                    hue, saturation, value = np.median(hsv_tile, axis=(0, 1))

                    if Yellow_pixels > 0 : 
                     print(f"H: {hue}, S: {saturation}, V: {value},   Tile ({y},{x}) Brown pixels: {Yellow_pixels}")

                    
        # Saml boardet igen
        b_result = result.copy()
        for y in range(5):
            for x in range(5):
                result[y*100:(y+1)*100, x*100:(x+1)*100] = tiles[y][x]


         # Gem felter fra y_result der opfylder kriterierne
        import os
        output_folder = "mine felter billeder.py"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Hent tiles fra y_result
        save_tiles = b_get_tiles(b_result)
        
        for y in range(5):
            for x in range(5):
                tile = save_tiles[y][x]
                
                # Tjek om tile ikke er helt sort (mørk)
                if np.sum(tile) > 0:  # Hvis der er nogle pixels der ikke er sorte
                    # Konverter til HSV og find median hue
                    tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
                    hue, saturation, value = np.median(tile_hsv, axis=(0, 1))
                    
                    # Gem hvis hue er under 31 eller over 104
                    if hue < 31 or hue > 104:
                        output_filename = os.path.join(output_folder, f"image{i}_tile_y{y}_x{x}_hue{int(hue)}.jpg")
                        cv2.imwrite(output_filename, tile)
                        print(f"Saved: {output_filename} (Hue: {hue})")
        

        cv2.imshow("m_mask", b_result)
   
        cv2.imshow("Filtered board", y_result)

        key = cv2.waitKey(0)

        if key == 27:  # ESC
                cv2.destroyWindow("Filtered board")
                continue



if __name__ == "__main__":
    main()