import os
import cv2

screenshot = cv2.imread(os.path.join('images', 'test.png'))
# needle_img = cv2.imread(os.path.join('images', 'needles', 'battles.jpg'))
# needle_img = cv2.imread(os.path.join('images', 'needles', 'quick_move.jpg'))
# needle_img = cv2.imread(os.path.join('images', 'needles', 'quick_move_2.jpg'))
needle_img = cv2.imread(os.path.join('images', 'needles', 'quick_move_2.jpg'))

result = cv2.matchTemplate(screenshot, needle_img, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)


threshold = 0.3
if max_val >= threshold:
    # get the best march position
    print('Best match top left position: %s' % str(max_loc))
    print('Best match confidence: %s' % max_val)

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

    cv2.rectangle(screenshot, top_left, bottom_right,
                  color=(0, 0, 255), thickness=2, lineType=cv2.LINE_4)

    cv2.imshow('Result', screenshot)
    cv2.waitKey(0)

else:
    print('Needle not found')

