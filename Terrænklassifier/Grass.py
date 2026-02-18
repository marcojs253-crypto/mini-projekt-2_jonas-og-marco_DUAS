import cv2
import numpy as np

#############################################################################################################################
#############################################################################################################################

# Open picture
brikker = cv2.imread("57.jpg")

# Convert BGR to HSV
brikker_hsv = cv2.cvtColor(brikker, cv2.COLOR_BGR2HSV)

# Forest-brik range
lower_Grass = np.array([34, 240 , 129])
upper_Grass = np.array([48, 248, 164])

# Lav maske (hvid = pixels indenfor range)
mask_Grass = cv2.inRange(brikker_hsv, lower_Grass, upper_Grass)

# Behold KUN pixels i masken
result_Grass = cv2.bitwise_and(brikker, brikker, mask=mask_Grass)

cv2.imshow("Original", brikker)
cv2.imshow("Mask (hvid = fundet)", mask_Grass)

cv2.waitKey(0)
cv2.destroyAllWindows()

#############################################################################################################################
#############################################################################################################################