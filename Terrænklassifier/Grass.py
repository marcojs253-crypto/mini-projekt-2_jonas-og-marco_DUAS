import cv2
import numpy as np

lower_Grass = np.array([70, 80, 50])
upper_Grass = np.array([138, 127, 104])

# Open picture
brikker = cv2.imread("57.jpg")

def main():

    def get_tiles(img):
        tiles = []
        for y in range(5):
            tiles.append([])
            for x in range(5):
                tiles[-1].append(img[y*100:(y+1)*100, x*100:(x+1)*100])
        return tiles

    for i in range(1, 74):  # 1.jpg til 40.jpg

        filename = f"{i}.jpg"
        print(f"Processing {filename}")

        brikker = cv2.imread(filename)
        brikker_2 = cv2.imread(filename)

        if brikker is None:
            print("File not found")
            continue

        # Convert BGR to YCrCb
        brikker_ycrcb = cv2.cvtColor(brikker, cv2.COLOR_BGR2YCrCb)

        mask_Grass = cv2.inRange(brikker_ycrcb, lower_Grass, upper_Grass)
        result_Grass = cv2.bitwise_and(brikker, brikker, mask=mask_Grass)

        tiles = get_tiles(brikker)

        for y in range(5):
            for x in range(5):
                tile = tiles[y][x]

                tile_ycrcb = cv2.cvtColor(tile, cv2.COLOR_BGR2YCrCb)
                tile_mask = cv2.inRange(tile_ycrcb, lower_Grass, upper_Grass)

                grass_pixels = cv2.countNonZero(tile_mask)
                print(f"Tile ({y},{x}) grass pixels: {grass_pixels}")

                if grass_pixels < 2250:
                    tiles[y][x][:] = 0

        result = brikker.copy()
        for y in range(5):
            for x in range(5):
                result[y*100:(y+1)*100, x*100:(x+1)*100] = tiles[y][x]

        combined = np.hstack((brikker_2, result))

        cv2.imshow("Filtered board", combined)
        cv2.imshow("Filtered board", combined)

        key = cv2.waitKey(0)

        if key == 27:  # ESC
            cv2.destroyWindow("Filtered board")
            continue


    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
