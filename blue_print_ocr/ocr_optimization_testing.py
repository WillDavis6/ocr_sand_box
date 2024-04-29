import cv2 as cv
import sys
from matplotlib import pyplot as plt
from opt_preprocessing import get_all_grayscales, detect_lines, show_merged_lines
from opt_text_extraction import crop_ROI, find_text
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


blueprint_url =  "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\images\\table_test.png"
#blueprint_url =  "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\images\\Screenshot 2024-04-24 081630.png"

export_url = "C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\test_updated_image_cv2.png"


def ocr_magic(bluprint_url, export_url):

    
    all_lines = []
    images, titles = get_all_grayscales(blueprint_url)

    for i, image in enumerate(images):
        image_lines = []
        cimage, horizontal_lines, veritcal_lines = detect_lines(image, minLinLength=500, display=True, write=True)
        image_lines.append([horizontal_lines, veritcal_lines])
        images[i] = cimage
        # cv.imshow(f'image iteration {i}', cimage)
        # cv.waitKey(0)
        all_lines.append(image_lines)

    # SHOWS ALL EXAMPLES OF cv.LINE FOR EACH DIFFEREING THRESHOLD

    # for i in range(10):
    #     plt.subplot(2,5,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    #     plt.title(titles[i])
    #     plt.xticks([]),plt.yticks([])

    
    merged_horizontal_lines, merged_vertical_lines, cImage_color = show_merged_lines(all_lines, blueprint_url)

    first_line_index = 0
    last_line_index = len(merged_vertical_lines)
    first_row_index = 0
    last_row_index = len(merged_horizontal_lines)

    for i in range(first_line_index, last_line_index-1):
        print(f'j range: {last_line_index}')
        for j in range(first_row_index, last_row_index):
            
            left_line_index = j
            right_line_index = j+1
            top_line_index = i
            bottom_line_index = i+1

            cropped_image, (x1, y1, w, h) = crop_ROI(cImage_color, merged_horizontal_lines, merged_vertical_lines, left_line_index, right_line_index, top_line_index, bottom_line_index)
            
            text = find_text(cropped_image, is_number=True)
            print(text)
            text = find_text(cropped_image, is_number=False)
            print(text)
            print(f'left line index {j}: right line index {j+1}')

            #cv.imshow(f'row shot {i}: column {j}', cropped_image)
            #cv.waitKey(0)



    # return plt.show()

# if scr is None:
#     sys.exit("Could not read the image.")

# cv.imshow("Display window", scr)
# k = cv.waitKey(0)

# if k == ord('s'):
#     cv.imwrite(export_url, scr)



ocr_magic(blueprint_url, export_url)