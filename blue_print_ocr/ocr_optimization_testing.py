import cv2 as cv
from matplotlib import pyplot as plt
from opt_preprocessing import return_horizontal_vertical_lines
from opt_text_extraction import crop_ROI, find_text
import pytesseract
import numpy as np
from rich.progress import Progress



pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def ocr_magic(blueprint_url, export_url, buffer, linValue, overlap_buffer, index, metadata, engine, Session):

    #Import table format inside function to prevent circular imports
    from tables_ocr import DynamicTable, add_row
    session = Session()

    # Prepare all lines to overlay image
    merged_horizontal_lines, merged_vertical_lines, cImage_color = return_horizontal_vertical_lines(blueprint_url, buffer, linValue, overlap_buffer)
    
    #Dynamically build sql table by number of lines detected
    table = DynamicTable.create_table(len(merged_vertical_lines), index, metadata, engine)


    first_line_index = 0
    last_line_index = len(merged_vertical_lines)-1
    first_row_index = 0
    last_row_index = len(merged_horizontal_lines)-1
    

    rows_range = range(first_row_index, last_row_index)
   
  
    progress = Progress()

    task = progress.add_task("[green]Processing Table", total=len(rows_range))

    with progress:
        for i in rows_range:
          
            row_values = []
            for j in range(first_line_index, last_line_index):
                
                left_line_index = j
                right_line_index = j+1
                top_line_index = i-1
                bottom_line_index = i
                
                #Simultaniously crop the image for lines and crop another gray scale for comparision to template // issue with data type previously.
                #Convert the cropped ROI for match temple after cropping.
                cropped_image, (x1, y1, w, h) = crop_ROI(cImage_color, merged_horizontal_lines, merged_vertical_lines, left_line_index, right_line_index, top_line_index, bottom_line_index)

                
                if i == rows_range[-1]:
                
                    text = find_text(cropped_image, is_number=False)
        
                    row_values.append(text)

                else:

                    text = find_text(cropped_image, is_number=True)
        
                    row_values.append(text)
            
            #print(f'Rows to add {row_values}')
            add_row(row_values, table, session)
            progress.update(task, advance=1)

    
    return f"dynamic_table_{index}"
    


         

