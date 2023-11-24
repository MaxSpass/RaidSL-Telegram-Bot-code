import os
import cv2

"""
Contour detection and drawing using different extraction modes to complement
the understanding of hierarchies
"""

img = cv2.imread(os.path.join('images', 'screens', 'collection_expand.png'), -1)

img_gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh2 = cv2.threshold(img_gray2, 150, 255, cv2.THRESH_BINARY)
contours6, hierarchy6 = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
image_copy7 = img.copy()
cv2.drawContours(image_copy7, contours6, -1, (0, 255, 0), 2, cv2.LINE_AA)
# see the results
cv2.imshow('TREE', image_copy7)
print(f"TREE: {hierarchy6}")
cv2.waitKey(0)
cv2.imwrite('contours_retr_tree.jpg', image_copy7)
cv2.destroyAllWindows()
