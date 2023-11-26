import pytesseract
import cv2
import pyautogui
from helpers.screen import *

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

def read_text_in_region(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(r"D:\ComputerVision\bot\text.png")
    img = cv2.imread(r"D:\ComputerVision\bot\text.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(threshold_img)
    return text

def capture_demon_lord_result():
    return read_text_in_region(axis_to_region(184, 150, 687, 202))


text = capture_demon_lord_result()
print(text)