import cv2
import pyautogui

from classes.task_iterator import TaskIterator
from helpers.common import *


def test_func(msg, limit=3):
    counter = 0
    while counter < limit:
        print(msg)
        sleep(1)
    return True


def in_progress_determine_quests_text():
    # screenshot = pyautogui.screenshot(region=axis_to_region(191, 179, 579, 257))
    screenshot = pyautogui.screenshot(region=axis_to_region(186, 166, 579, 204))
    screenshot_scaled = scale_up(screenshot, factor=2)
    # show_pyautogui_image(screenshot_scaled)

    image = screenshot_to_image(screenshot_scaled)

    configs = [
        '--psm 1 --oem 3',
        '--psm 3 --oem 3',
        '--psm 4 --oem 3',
        '--psm 6 --oem 3',
        '--psm 7 --oem 3',
        '--psm 8 --oem 3',
        '--psm 9 --oem 3',
        '--psm 10 --oem 3',
        '--psm 11 --oem 3',
        '--psm 12 --oem 3',
    ]

    # Display the result
    # cv2.imshow('Outlined Text', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # text = pytesseract.image_to_string(gray)

    for i in range(len(configs)):
        config = configs[i]
        boxes = pytesseract.image_to_boxes(gray, config=config)

        # Split the bounding boxes into lines
        box_lines = boxes.splitlines()

        # Initialize lists to store bounding boxes for each line
        line1_boxes = []
        line2_boxes = []

        # Find the midpoint of the image (assuming the text is split into two lines at the midpoint)
        midpoint = gray.shape[0] // 2

        print('box_lines', box_lines)

        # Iterate through bounding boxes and separate them into two lines
        for box in box_lines:
            data = box.split()
            if len(data) >= 6:
                _, y1, _, y2, _ = map(int, data[1:6])
                # Calculate the vertical midpoint of the box
                y_mid = (y1 + y2) // 2
                # print('data', data)
                if y_mid > midpoint:
                    line2_boxes.append(data)
                else:
                    line1_boxes.append(data)

        # Concatenate bounding boxes for each line into single strings
        concatenated_line1_boxes = ' '.join(' '.join(data) for data in line1_boxes)
        concatenated_line2_boxes = ' '.join(' '.join(data) for data in line2_boxes)

        # for i in range(len(configs)):
        #     config = configs[i]
        #     str_config_1 = f'{config} -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -c bbox={concatenated_line1_boxes}'
        #     str_config_2 = f'{config} -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -c bbox={concatenated_line2_boxes}'
        #     text_from_line1 = pytesseract.image_to_string(gray, config=str_config_1)
        #     text_from_line2 = pytesseract.image_to_string(gray, config=str_config_2)
        #
        #     # Concatenate the extracted text from both lines
        #     full_text = text_from_line1.strip() + '\n' + text_from_line2.strip()
        #     print(full_text)

        # # Use Tesseract to extract text from concatenated bounding boxes
        text_from_line1 = pytesseract.image_to_string(gray)
        text_from_line2 = pytesseract.image_to_string(gray)

        # Concatenate the extracted text from both lines
        full_text = text_from_line1.strip() + '\n' + text_from_line2.strip()

        print(full_text)

        # Draw rectangles around the text regions
        # for box in boxes.splitlines():
        #     box = box.split()
        #     x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
        #     cv2.rectangle(image, (x, image.shape[0] - y), (w, image.shape[0] - h), (0, 255, 0), 1)
        #

    return


def in_progress_task_iterator():
    pixel_red = [750, 450, [136, 0, 21]]
    pixel_black = [750, 450, [0, 0, 0]]
    pixel_grey = [750, 450, [127, 127, 127]]

    tasks = [
        {
            "predicate": lambda: pixels_wait([pixel_red], wait_limit=10)
        },
        {
            "predicate": lambda: pixels_wait([pixel_black], wait_limit=10)
        },
        {
            "predicate": lambda: pixels_wait([pixel_black], wait_limit=10)
        }
    ]

    def case_first(res):
        if res[0]:
            return 1
            # click(auto_mode[0], auto_mode[1])
            # battle_result = pixels_wait(
            #     [victory, defeat],
            #     msg='Victory or Defeat',
            #     timeout=2,
            #     mistake=20,
            #     wait_limit=1200,
            #     debug=True
            # )

    tasks = [
        {
            "predicate": lambda res: pixels_wait([[], [], []], msg='My turn or Defeat'),
            "tasks": [
                {
                    "predicate": lambda res: case_first(res),
                },
                # {
                #     "predicate": lambda res: self._save_result(res[0]),
                # },
            ]
        }
    ]

    task_iterator = TaskIterator({
        'tasks': tasks
    })

    print(pyautogui.pixel(750, 450))


def in_progress_find_squares():
    def find_squares(image, min_width, min_height, tolerance=5):
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        squares = []

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detect edges using Canny edge detection
        edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

        # Find contours in the edge-detected image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop over the contours
        for cnt in contours:
            # Approximate the contour with a polygon
            epsilon = 0.1 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            # If the contour has four vertices and is convex, it could be a square
            if len(approx) == 4 and cv2.isContourConvex(approx):
                # Calculate the bounding box of the contour
                x, y, w, h = cv2.boundingRect(approx)

                # If the width and height are within the tolerance range of the desired size, add the square to the list
                if min_width - tolerance <= w <= min_width + tolerance and min_height - tolerance <= h <= min_height + tolerance:
                    squares.append(approx)

        return squares

    # Load the image
    screenshot = pyautogui.screenshot(region=axis_to_region(258, 115, 620, 480))
    image = screenshot_to_image(screenshot)

    # Specify the minimum width and height for squares
    min_width = 50
    min_height = 50

    # Find squares with the specified minimum size in the image
    squares = find_squares(image, min_width, min_height)

    # Draw the squares on the original image
    for square in squares:
        cv2.drawContours(image, [square], -1, (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Squares', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
