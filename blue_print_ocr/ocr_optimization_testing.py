import cv2 as cv
import sys
from matplotlib import pyplot as plt
from opt_preprocessing import get_all_grayscales, detect_lines, show_merged_lines, crop_ROI, find_text
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

    first_line_index = 1
    last_line_index = len(merged_vertical_lines)

    for i in range(first_line_index, last_line_index):

    crop_ROI(cImage_color, merged_horizontal_lines, merged_vertical_lines,)



    # return plt.show()

# if scr is None:
#     sys.exit("Could not read the image.")

# cv.imshow("Display window", scr)
# k = cv.waitKey(0)

# if k == ord('s'):
#     cv.imwrite(export_url, scr)



ocr_magic(blueprint_url, export_url)