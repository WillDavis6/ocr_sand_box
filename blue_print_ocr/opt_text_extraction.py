import pytesseract
import numpy as np
import cv2
from google.cloud import vision
import chardet
import io

client = vision.ImageAnnotatorClient()

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def get_cropped_image(image, x, y, w, h):
    cropped_image = image[y:y+h, x:x+w]
    
    return cropped_image

def crop_ROI(image, horizontal, vertical, left_line_index, right_line_index, top_line_index, bottom_line_index, offset=4):
    x1 = vertical[left_line_index][2] + offset
    y1 = horizontal[top_line_index][3] + offset
    x2 = vertical[right_line_index][2] - offset
    y2 = horizontal[bottom_line_index][3] - offset

    w = x2 - x1
    h = y2 - y1

    cropped_image = get_cropped_image(image, x1, y1, w, h)

    return cropped_image, (x1, y1, w, h)

def find_text(cropped_frame):
    # if(is_number):
    #     text = pytesseract.image_to_string(cropped_frame, config= '-c tessedit_char_whitelist=0123456789 --psm 10 --oem 3')

    # else: 
    #     text = pytesseract.image_to_string(cropped_frame, config= '--psm 10 --oem 3')

    _, buffer = cv2.imencode('.jpg', cropped_frame)
    image_bytes = buffer.tobytes()

    image = vision.Image(content = image_bytes)

    response = client.text_detection(image=image)

    texts = response.text_annotations

    

    if texts:
        text = texts[0].description

   
        return text

