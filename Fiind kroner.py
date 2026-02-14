from copy import deepcopy

import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

image = cv2.imread("1.jpg")
#cv2.imshow("Fruits", image)

"hvis vi får brug for at splitte billedet i tiles, så kan vi bruge denne funktion"
# def get_tiles(image):
#     tiles = []
#     for y in range(5):
#         tiles.append([])
#         for x in range(5):
#             tiles[-1].append(image[y*100:(y+1)*100, x*100:(x+1)*100])
#     return tiles

# tiles = get_tiles(image)
# preprossesing af billedet

blurred = cv2.filter2D(image, cv2.CV_8U, np.ones((7, 7), dtype=np.uint8) / 49)


hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
#cv2.imshow("HSV", hsv)

hue = hsv[:, :, 0]
# cv2.imshow("Hue", hue)

# Edge detection FØRST
edges_h = cv2.filter2D(
    hue,
    cv2.CV_32F,
    np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32),
)
edges_h = cv2.convertScaleAbs(edges_h)


edges_v = cv2.filter2D(
    hue,
    cv2.CV_32F,
    np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32),
)
edges_v = cv2.convertScaleAbs(edges_v)


all_edges = cv2.convertScaleAbs(edges_v + edges_h)
cv2.imshow("All edges", all_edges)



# Threshold på edges i stedet for hue
_, blobs = cv2.threshold(all_edges, 20, 255, cv2.THRESH_BINARY)
cv2.imshow("Blobs", blobs)
kernel = np.ones((2, 2), dtype=np.uint8)
# Luk huller/forbind fragmenter
blobs = cv2.morphologyEx(blobs, cv2.MORPH_CLOSE, kernel)
cv2.imshow("Blobs after closing", blobs)

contours, _ = cv2.findContours(blobs, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
outlines = cv2.drawContours(deepcopy(image), contours, -1, (0, 255, 0))
cv2.imshow("Outlines", outlines)

xs = []
coordinates = []
for contour in contours:
             mask = np.zeros(hue.shape, dtype=np.uint8)
             mask = cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
             
cv2.imshow("Mask", mask)
xs.append([cv2.mean(hue, mask)[0]]) 
coordinates.append(contour[0][0])

cv2.waitKey()
