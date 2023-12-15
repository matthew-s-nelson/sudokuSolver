import cv2
import easyocr


# # Capture image from camera
# cap = cv2.VideoCapture(0)
# ret, frame = cap.read()

# Read image
image = cv2.imread('image2.png')

# Show the image
# cv2.imshow('original', image) 

# When any key is pressed, the window closes
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# Preprocess the image

def preprocess_image(image):
    # Graysclae the image
    grayed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('grayed', grayed)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Use gaussian blur to sharpen the image and reduce noise
    blurred = cv2.GaussianBlur(grayed, (5, 5), 0)
    # cv2.imshow('blurred', blurred)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Create a binary image. Helps to account for lighting differences in the image
    binary_image = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # cv2.imshow('binary', binary_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

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
    # cv2.imshow('cropped', cropped_board)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return cropped_board

def process_nums(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped)

    digits = [detection[1] for detection in result]
    print(digits)
    return digits


# Release the camera
# cap.release()
preprocessed = preprocess_image(image)
border = find_border(preprocessed)
cropped = crop_image(border, preprocessed)
process_nums(cropped)

# reader = easyocr.Reader(['en'])
# result = reader.readtext(cropped)

# for detection in result:
#     text = detection[1]
#     print(f"Detected text: {text}")
