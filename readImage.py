import cv2
# import easyocr
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

from solver import *
from copy import deepcopy

# Read image
image = cv2.imread('image3.png')

# Show the image
# cv2.imshow('original', image) 

# When any key is pressed, the window closes
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# Preprocess the image

def preprocess_image(image):
    # Graysclae the image
    grayed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use gaussian blur to sharpen the image and reduce noise
    blurred = cv2.GaussianBlur(grayed, (5, 5), 0)

    # Create a binary image. Helps to account for lighting differences in the image
    binary_image = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


    return binary_image


def find_border(image):
    # Finds the contours of the binary image
    # RETR_External tells it to find the extreme outer contour (the border of the sudoku board)
    # CHAIN_APPROX_SIMPLE simplifies the list of returned points. It only includes the endpoints if it's a straight line (which it is in this case).
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)

    # Finds the biggest contour of the image, based on area, which should be the border of the board
    border = max(contours, key=cv2.contourArea)
    # print(border)

    return border

# Crops the image so the edges are the edges of the grid
def crop_image(border, image):
    # Find the x, y of the starting point of the border
    x, y, width, height = cv2.boundingRect(border)

    cropped_board = image[y:y+height, x:x+width]
    cv2.imshow('cropped', cropped_board)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return cropped_board

def split_boxes(image):
    height = image.shape[0]
    width = image.shape[1]
    box_height = height/9
    box_width = width/9
    boxes = []
    for y in range(1, 10):
        for x in range(1, 10):
            box = image[int(box_height*(y-1)):int(box_height*y), int(box_width*(x-1)):int(box_width*x)]
            boxes.append(box)
            
    return boxes


def tesseract(image):
    _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    custom_config = r'--oem 3 --psm 6'
    result = pytesseract.image_to_string(thresh, config=custom_config)

    # Extract digits from the result
    digits = [int(char) for char in result if char.isdigit()]

    if digits:
        return digits[0]
    else:
        return None


preprocessed = preprocess_image(image)
border = find_border(preprocessed)

cropped = crop_image(border, preprocessed)
boxes = split_boxes(cropped)
count = 0
grid = []
row = []
for box in boxes:
    # cv2.imshow('box', box)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows() 
    if count < 8:
        row.append(tesseract(box))
        count += 1
        print(row)
    else:
        row.append(tesseract(box))
        grid.append(row)
        print("row: ",row)
        print("grid: ", grid)

        count = 0
        row = []


# grid = [[None, 3, None, None, None, None, None, None, None],
# [None, None, None, 1, 9, 5, None, None, None],
# [None, 9, 8, None, None, None, None, 6, None],
# [8, None, None, None, 6, None, None, None, None],
# [4, None, None, None, None, 3, None, None, 1],
# [None, None, None, None, 2, None, None, None, None],
# [None, 6, None, None, None, None, 2, 8, None],
# [None, None, None, None, 1, 9, None, None, 5],
# [None, None, None, None, None, None, None, None, None]]

to_solve = sudokuBoard(grid)

print(str(to_solve))
if to_solve.solve():
    print(str(to_solve))
else:
    print("Can't be solved")

