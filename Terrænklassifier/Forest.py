import cv2
import numpy as np

#############################################################################################################################
#############################################################################################################################

# Open picture
brikker = cv2.imread("69.jpg")

# Convert BGR to HSV
brikker_hsv = cv2.cvtColor(brikker, cv2.COLOR_BGR2HSV)

# Forest-brik range
lower_forest = np.array([50, 68, 25])
upper_forest = np.array([78, 239, 128])

# Lav maske (hvid = pixels indenfor range)
mask_forest = cv2.inRange(brikker_hsv, lower_forest, upper_forest)

# Behold KUN pixels i masken
result_forest = cv2.bitwise_and(brikker, brikker, mask=mask_forest)

cv2.imshow("Original", brikker)

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

    tiles = get_tiles(brikker)

    for y in range(5):
        for x in range(5):
            tile = tiles[y][x]

            tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
            tile_mask = cv2.inRange(tile_hsv, lower_forest, upper_forest)

            green_pixels = cv2.countNonZero(tile_mask)
            print(f"Tile ({y},{x}) grønne pixels: {green_pixels}")

            if green_pixels < 800:
                tiles[y][x][:] = 0  # gør tile sort

    # Saml boardet igen
    result = brikker.copy()
    for y in range(5):
        for x in range(5):
            result[y*100:(y+1)*100, x*100:(x+1)*100] = tiles[y][x]

    cv2.imshow("Filtered board", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()