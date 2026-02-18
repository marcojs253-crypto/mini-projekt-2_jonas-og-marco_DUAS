import cv2
import numpy as np

#############################################################################################################################
#############################################################################################################################

# Open picture
brikker = cv2.imread("1.jpg")

# Convert BGR to HSV
brikker_hsv = cv2.cvtColor(brikker, cv2.COLOR_BGR2HSV)

# Forest-brik range
lower_mine = np.array([28, 68, 25])
upper_mine = np.array([78, 239, 128])

# Lav maske (hvid = pixels indenfor range)
mask_forest = cv2.inRange(brikker_hsv, lower_mine, upper_mine)

# Behold KUN pixels i masken
result_forest = cv2.bitwise_and(brikker, brikker, mask=mask_forest)

cv2.imshow("Original", brikker)
cv2.imshow("Only green kept", result_forest)
cv2.waitKey(0)
cv2.destroyAllWindows()

#############################################################################################################################
#############################################################################################################################