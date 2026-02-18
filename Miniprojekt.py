import cv2

# Open picture
brikker = cv2.imread("/Users/jonassvirkaer/Desktop/python_projekter/P2 - Opgaver/Design og udvikling af AI-systemer/Miniprojekt/King_domino.png")

# Converts BGR to HSV values
brikker_hsv = cv2.cvtColor(brikker, cv2.COLOR_BGR2HSV)

#######################################################################################################################################

brikker_value = brikker_hsv[:, :, 2]
brikker_saturation = brikker_hsv[:, : ,1]
brikker_hue = brikker_hsv[:, :, 0]
#######################################################################################################################################

mask_v = cv2.inRange(brikker_value, 200, 225)
mask_s = cv2.inRange(brikker_saturation, 1, 150)
mask_h = cv2.inRange(brikker_hue, 20, 40)
mask_combined = cv2.bitwise_and(mask_h, mask_s)
mask_combined = cv2.bitwise_and(mask_combined, mask_v)

#######################################################################################################################################

kernel = cv2.getStructuringElement(cv2.MORPH_DIAMOND, (5,5))
mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_CLOSE, kernel, iterations=2)
contours, _ = cv2.findContours(mask_combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#######################################################################################################################################

out = brikker.copy()
kept = []
for c in contours:
    area = cv2.contourArea(c)
    if area < 180:
        continue
    if area > 2000:
        continue
    kept.append(c)

for element in kept:
    print(cv2.contourArea(element))

#######################################################################################################################################

final_kept = []
for element in kept:
    perimeter = cv2.arcLength(element, True)

    if perimeter > 10000:
        continue
    final_kept.append(element)
    print("Area:", area, "Perimeter:", perimeter)

#######################################################################################################################################

#######################################################################################################################################

# Tegn kun de “store nok” konturer
cv2.drawContours(out, final_kept, -1, (0, 255, 0), 2)

cv2.imshow("Mask - Value", mask_combined)
cv2.imshow("Contours (filtered by area)", out)
cv2.waitKey(0)

#######################################################################################################################################

#Close display with escape-button
while True:
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()