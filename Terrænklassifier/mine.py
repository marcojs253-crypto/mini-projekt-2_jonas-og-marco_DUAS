import cv2
import numpy as np

#############################################################################################################################
#############################################################################################################################

# Open picture
brikker = cv2.imread("59.jpg")

# Convert BGR to HSV
brikker_hsv = cv2.cvtColor(brikker, cv2.COLOR_BGR2HSV)

# Forest-brik range
lower_mine = np.array([0, 0, 0])
upper_mine = np.array([200, 35, 64])

# Lav maske (hvid = pixels indenfor range)
mask_mine = cv2.inRange(brikker_hsv, lower_mine, upper_mine)

# Behold KUN pixels i masken
result_mine = cv2.bitwise_and(brikker, brikker, mask=mask_mine)

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
            tile_mask = cv2.inRange(tile_hsv, lower_mine, upper_mine)

            black_pixels = cv2.countNonZero(tile_mask)
            print(f"Tile ({y},{x}) black pixels: {black_pixels}")

            if black_pixels < 200:
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