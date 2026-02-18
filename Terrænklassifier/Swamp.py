import cv2
import numpy as np

#############################################################################################################################
#############################################################################################################################

# Open picture
brikker = cv2.imread("14.jpg")

# Convert BGR to HSV
brikker_hsv = cv2.cvtColor(brikker, cv2.COLOR_BGR2HSV)

# Forest-brik range
lower_Swamp = np.array([78, 193 , 109])
upper_Swamp = np.array([109, 255, 204])

# Lav maske (hvid = pixels indenfor range)
mask_Swamp = cv2.inRange(brikker_hsv, lower_Swamp, upper_Swamp)

# Behold KUN pixels i masken
result_Swamp = cv2.bitwise_and(brikker, brikker, mask=mask_Swamp)

cv2.imshow("Original", brikker)
cv2.imshow("Mask (hvid = fundet)", mask_Swamp)

cv2.waitKey(0)
cv2.destroyAllWindows()

#############################################################################################################################
#############################################################################################################################