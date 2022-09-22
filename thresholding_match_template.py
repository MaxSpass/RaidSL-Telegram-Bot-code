import os
import numpy as np
import cv2
from helpers.screen import *

screenshot = cv2.imread(os.path.join('images', 'screens', 'demon_lord_with_rewards_scrolled.png'))
# needle_img = cv2.imread(os.path.join('images', 'sliced', 'lyudoed.png'))

# needle_img_not_resized = cv2.imread(os.path.join('dataset', 'images', 'heroes', 'maneater_profile.png'))
# needle_img_not_resized = cv2.imread(os.path.join('dataset', 'images', 'heroes', 'ninja_profile.png'))
# needle_img_not_resized = cv2.imread(os.path.join('dataset', 'images', 'heroes', 'seeker_profile.png'))
needle_img_not_resized = cv2.imread(os.path.join('dataset', 'images', 'heroes', 'painkeeper_profile.png'))



needle_origin_w = 45
needle_origin_h = 59
needle_captured_w = 34
needle_captured_h = 14
needle_offset_x = needle_captured_h / 2
needle_offset_y = needle_captured_w / 2
# needle_img = cv2.resize(needle_img_not_resized, (44, 54), interpolation=cv2.INTER_AREA)
needle_img_resized = image_resize(needle_img_not_resized, height=needle_origin_h)
needle_img = cut_image_center(needle_img_resized, needle_captured_w, needle_captured_h)

needle_dataset_aspect_ratio = needle_img_not_resized.shape[1] / needle_img_not_resized.shape[0]
needle_img_aspect_ratio = needle_origin_w / needle_origin_h

koeff_aspect_ratio = needle_img_aspect_ratio / needle_dataset_aspect_ratio

print(needle_dataset_aspect_ratio, needle_img_aspect_ratio, koeff_aspect_ratio * needle_img_not_resized.shape[0])

result = cv2.matchTemplate(screenshot, needle_img, cv2.TM_CCOEFF_NORMED)

def extend_coordinates(*arr):
    arr.append(needle_origin_w)
    arr.append(needle_origin_h)

    return arr

w = needle_origin_w
h = needle_origin_h
threshold = 0.8
yloc, xloc = np.where(result >= threshold)
for (x, y) in zip(xloc, yloc):
    cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0,255,255), 2)

rectangles = []
for (x, y) in zip(xloc, yloc):
    rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles.append([int(x), int(y), int(w), int(h)])

rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.6)
# There is a bug here | Found elements overlaps each other
# print(locations, len(locations))

print(rectangles)
#https://github.com/ClarityCoders/ComputerVision-OpenCV/blob/master/Lesson3-TemplateMatching/Tutorial.ipynb
locations = False

if locations:
    print('Found needle')

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]
    line_color = (0, 255, 0)
    # line_type = cv2.LINE_4

    # need to loop over all the locations and draw their rectangle
    for index, loc in enumerate(locations):
        # determine the box positions
        # top_left = loc
        # bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

        #draw the full box
        top_left = (
            round(loc[0] - needle_offset_x),
            round((loc[1] - needle_offset_y) * koeff_aspect_ratio)
        )
        bottom_right = (top_left[0] + needle_origin_w, round((top_left[1] + needle_origin_h) * koeff_aspect_ratio))

        # save files
        # file_name = "%s.jpg" % index
        # coordinates = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
        # cv2.imwrite(file_name, crop(screenshot, *coordinates))
        # print(file_name)

        cv2.rectangle(screenshot, top_left, bottom_right, line_color)

    cv2.imshow('Matches', screenshot)
    cv2.waitKey()

else:
    print('Needle not found')


