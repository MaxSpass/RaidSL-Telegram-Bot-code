import os
import numpy as np
import cv2

screenshot = cv2.imread(os.path.join('images', 'screens', 'demon_lord_with_rewards_scrolled.png'))
needle_img = cv2.imread(os.path.join('images', 'sliced', 'lyudoed.png'))

result = cv2.matchTemplate(screenshot, needle_img, cv2.TM_CCOEFF_NORMED)

threshold = 0.8
locations = np.where(result >= threshold)
locations = list(zip(*locations[::-1]))

if locations:
    print('Found needle')

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]
    line_color = (0, 0, 255)
    line_type = cv2.LINE_4

    # need to loop over all the locations and draw their rectangle
    for loc in locations:
        # determine the box positions
        top_left = loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        #draw the box
        cv2.rectangle(screenshot, top_left, bottom_right, line_color, line_type)

    cv2.imshow('Matches', screenshot)
    cv2.waitKey()

else:
    print('Needle not found')


