import os
from cv2 import imshow, imread, imwrite, waitKey, cvtColor, findContours, threshold, drawContours, destroyAllWindows, THRESH_BINARY, RETR_TREE, LINE_AA, COLOR_BGR2GRAY, CHAIN_APPROX_NONE

"""
Contour detection and drawing using different extraction modes to complement
the understanding of hierarchies
"""

img = imread(os.path.join('images', 'screens', 'collection_expand.png'), -1)

img_gray2 = cvtColor(img, COLOR_BGR2GRAY)
ret, thresh2 = threshold(img_gray2, 150, 255, THRESH_BINARY)
contours6, hierarchy6 = findContours(thresh2, RETR_TREE, CHAIN_APPROX_NONE)
image_copy7 = img.copy()
drawContours(image_copy7, contours6, -1, (0, 255, 0), 2, LINE_AA)
# see the results
imshow('TREE', image_copy7)
print(f"TREE: {hierarchy6}")
waitKey(0)
imwrite('contours_retr_tree.jpg', image_copy7)
destroyAllWindows()
