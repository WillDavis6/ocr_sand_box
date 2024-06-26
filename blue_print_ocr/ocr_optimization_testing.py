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
                top_line_index = i
                bottom_line_index = i +1
                
                #Simultaniously crop the image for lines and crop another gray scale for comparision to template // issue with data type previously.
   
                cropped_image, (x1, y1, w, h) = crop_ROI(cImage_color, merged_horizontal_lines, merged_vertical_lines, left_line_index, right_line_index, top_line_index, bottom_line_index)

                
                if i == rows_range[-1]:
                
                    text = find_text(cropped_image)
        
                    row_values.append(text)

                else:

                    text = find_text(cropped_image)
                    # if 'i' in text or 'lt >' in text or '[>' in text or  'L' in text or '1' in text:
                        
                    #     row_values.append('1')
                    # # elif 's' in text:

                    # #     row_values.append('9')
                    # elif '2' in text or '[a>' in text:

                    #     row_values.append('2')
                    # elif '3' in text or 'es' in text:

                    #     row_values.append('3')
                    # elif 'ee' in text or 'BS' in text or 'Bn' in text or 'Be' in text or 're' in text:

                    #     row_values.append('')
                    # else:

                    row_values.append(text)
            
            #print(f'Rows to add {row_values}')
            add_row(row_values, table, session)
            progress.update(task, advance=1)

    
    return f"dynamic_table_{index}"


def drop_tables(tables_list, metadata, engine, Fore, inspect, text):
    with engine.begin() as connection:
        inspector = inspect(engine)
        for table_name in tables_list:
            if table_name in inspector.get_table_names():
                connection.execute(text(f'DROP TABLE {table_name};'))
                print(Fore.CYAN + f'Dropped table: {table_name}')
            else:
                print(Fore.RED + f'Table {table_name} does not exist')




    


         

