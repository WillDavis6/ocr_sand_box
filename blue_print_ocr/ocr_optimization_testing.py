import cv2 as cv
from matplotlib import pyplot as plt
from opt_preprocessing import return_horizontal_vertical_lines
from opt_text_extraction import crop_ROI, find_text
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'




          




def ocr_magic(blueprint_url, export_url, buffer, linValue, overlap_buffer, table, template_url):

    # Prepare template by reading and converting to gray scale
    template = cv.imread(template_url)
    template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)


    # Prepare all lines to overlay image
    merged_horizontal_lines, merged_vertical_lines, cImage_color = return_horizontal_vertical_lines(blueprint_url, buffer, linValue, overlap_buffer)

    first_line_index = 0
    last_line_index = len(merged_vertical_lines)-1
    first_row_index = 0
    last_row_index = len(merged_horizontal_lines)-1

    # Build sql table row by row
    from tables_ocr import add_row

    for i in range(first_row_index, last_row_index):
        #print(f'On row {i}: j range: {first_line_index} : {last_line_index}')
        row_values = []
        for j in range(first_line_index, last_line_index):
            
            left_line_index = j
            right_line_index = j+1
            top_line_index = i
            bottom_line_index = i+1
            

            cropped_image, (x1, y1, w, h) = crop_ROI(cImage_color, merged_horizontal_lines, merged_vertical_lines, left_line_index, right_line_index, top_line_index, bottom_line_index)
           
            text_num = find_text(cropped_image, is_number=True)
            print(text_num)
            # text = find_text(cropped_image, is_number=False)
            # print(text)


            # Template match for field note images. 
            if text_num:
                row_values.append(text_num)
            else:
                # Convert ROI into correct data type and depth
                print(f'################## DATA TYPE OF ROI: {type(cImage_color)}')
                roi_converted = cv.imread(cropped_image)
                roi_gray = cv.cvtColor(roi_converted, cv.COLOR_BGR2GRAY)

                threshold = 0.8
                roi_result = cv.matchTemplate(roi_gray, template_gray, cv.TM_CCOEFF_NORMED)
                max_val = np.max(roi_result)

                if max_val >= threshold:
                    row_values.append('Template matched, insert: 1')
                else:
                    row_values.append(None)

           

        print(f'Rows to add {row_values}')
        add_row(row_values, table)


         



    # return plt.show()

# if scr is None:
#     sys.exit("Could not read the image.")

# cv.imshow("Display window", scr)
# k = cv.waitKey(0)

# if k == ord('s'):
#     cv.imwrite(export_url, scr)






# Buffer distance, min line length, and secondary buffer distance
