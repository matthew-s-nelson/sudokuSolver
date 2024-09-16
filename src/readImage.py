import cv2
from src.scanner import scan_image
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
from src.solver import *
from copy import deepcopy

def split_boxes(image):
    height = image.shape[0]
    width = image.shape[1]
    box_height = height/9
    box_width = width/9
    padding = -3
    boxes = []
    for y in range(1, 10):
        for x in range(1, 10):
            y1 = max(0, int(box_height*(y-1)) - padding)
            y2 = min(int(box_height*y) + padding, height)
            x1 = max(0, int(box_width*(x-1)) - padding)
            x2 = min(int(box_width*x) + padding, width)
            box = image[y1:y2, x1:x2]
            boxes.append(box)
            
    return boxes

def clean_digit(image):
    # Find the contours of the binary image, the digit should be the biggest contour
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    digit = max(contours, key=cv2.contourArea)

    # Crop to the digit
    x, y, w, h = cv2.boundingRect(digit)
    digit = image[y:y+h, x:x+w]
    digit = cv2.resize(digit, (28, 28))

    return digit


def tesseract(image):
    # Get tesseract data from the box
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    details = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
    text = details['text']
    conf = details['conf']

    for i in range(len(text)):
        # If it's a digit and the confidence is high enough, return the digit
        if text[i].isdigit() and int(conf[i]) > 50:
            return int(text[i])
        
    return None


def get_grid(filePath):
    preprocessed = scan_image(filePath)

    boxes = split_boxes(preprocessed)
    count = 0
    grid = []
    row = []
    for box in boxes:
        # clean up each individual box to make the digit more identifiable
        cleanDigit = clean_digit(box)

        if count < 8:
            if cleanDigit is not None:
                row.append(tesseract(cleanDigit))
            else:
                row.append(None)
            count += 1
            print(row)
        else:
            if cleanDigit is not None:
                row.append(tesseract(cleanDigit))
            else:
                row.append(None)
            grid.append(row)
            print("row: ",row)
            print("grid: ", grid)

            count = 0
            row = []
    return grid

# grid = get_grid()
# to_solve = sudokuBoard(grid)

# print(str(to_solve))
# if to_solve.solve():
#     print(str(to_solve))
# else:
#     print("Can't be solved")

