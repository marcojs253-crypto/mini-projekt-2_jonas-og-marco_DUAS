import cv2 as cv
import numpy as np
import os

def main():
    image_path = "1.jpg"
    if not os.path.isfile(image_path):
        print("Image not found")
        return
    image = cv.imread(image_path)
    tiles = get_tiles(image)
    print(len(tiles))
    # Fra chatgpt
    terrain_counts = {}
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            print(f"Tile ({x}, {y}):")

    print("\nTerrain counts:")
    for terrain, count in terrain_counts.items():
        print(f"{terrain}: {count}")

# Break a board into tiles
def get_tiles(image):
    tiles = []
    for y in range(5):
        tiles.append([])
        for x in range(5):
            tiles[-1].append(image[y*100:(y+1)*100, x*100:(x+1)*100])
    return tiles

if __name__ == "__main__":
    main()

    #NY