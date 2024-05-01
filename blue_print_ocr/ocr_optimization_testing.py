import cv2 as cv
from matplotlib import pyplot as plt
from opt_preprocessing import gather_all_lines, show_merged_lines
from opt_text_extraction import crop_ROI, find_text
from tables_ocr import build_dynamic_table, DynamicTable
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'




          


def ocr_magic(bluprint_url, export_url, buffer, linValue, overlap_buffer):

    
   all_lines = gather_all_lines(blueprint_url, linValue, overlap_buffer)

    merged_horizontal_lines, merged_vertical_lines, cImage_color = show_merged_lines(lambda: all_lines, blueprint_url, buffer)

    first_line_index = 0
    last_line_index = len(merged_vertical_lines)-1
    first_row_index = 0
    last_row_index = len(merged_horizontal_lines)-1

   

    for i in range(first_row_index, last_row_index):
        #print(f'On row {i}: j range: {first_line_index} : {last_line_index}')
        for j in range(first_line_index, last_line_index):
            
            left_line_index = j
            right_line_index = j+1
            top_line_index = i
            bottom_line_index = i+1

            cropped_image, (x1, y1, w, h) = crop_ROI(cImage_color, merged_horizontal_lines, merged_vertical_lines, left_line_index, right_line_index, top_line_index, bottom_line_index)
            
            text = find_text(cropped_image, is_number=True)
            print(text)
            text = find_text(cropped_image, is_number=False)
            print(text)
            #print(f'Row {i}. Left line index {j}: right line index {j+1}')

            # cv.imshow(f'row shot {i}: column {j}', cropped_image)
            # cv.waitKey(0)



    # return plt.show()

# if scr is None:
#     sys.exit("Could not read the image.")

# cv.imshow("Display window", scr)
# k = cv.waitKey(0)

# if k == ord('s'):
#     cv.imwrite(export_url, scr)


blueprint_url =  "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\images\\table_test.png"
#blueprint_url =  "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\images\\Screenshot 2024-04-24 081630.png"

export_url = "C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\test_updated_image_cv2.png"


ocr_magic(blueprint_url, export_url, 20, 500, 4)