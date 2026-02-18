import cv2
import numpy as np

#############################################################################################################################
#############################################################################################################################

# Open picture
brikker = cv2.imread("75.jpg")

# Convert BGR to HSV
brikker_hsv = cv2.cvtColor(brikker, cv2.COLOR_BGR2HSV)

# Forest-brik range
lower_water = np.array([78, 193 , 109])
upper_water = np.array([109, 255, 204])

# Lav maske (hvid = pixels indenfor range)
mask_water = cv2.inRange(brikker_hsv, lower_water, upper_water)

# Behold KUN pixels i masken
result_water = cv2.bitwise_and(brikker, brikker, mask=mask_water)

cv2.imshow("Original", brikker)
cv2.imshow("Mask (hvid = fundet)", mask_water)

cv2.waitKey(0)
cv2.destroyAllWindows()

#############################################################################################################################
#############################################################################################################################