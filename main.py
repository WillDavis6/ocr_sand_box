# SOURCE fazlurnu https://github.com/fazlurnu/Text-Extraction-Table-Image/blob/master/scripts/main.py

from preprocessing import get_grayscale, get_binary_gaussian, invert_area, draw_text, detect
from ocr import detect_lines, get_ROI
import cv2 as cv

def main(display = False, print_text = False, write = False):
    filename = "C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\5005 AD.png"

    src = cv.imread(cv.samples.findFile(filename))

    ret,src = cv.threshold(src,127,255,cv.THRESH_BINARY)

    horizontal, vertical = detect_lines(src, minLinLength=400, display=True, write=True)

    print(f'horizontal: {horizontal}, vertical: {vertical}')

    ## invert area
    left_line_index = 0
    right_line_index = 4
    top_line_index = 0
    bottom_line_index = -1

    cropped_image, (x, y, w, h) = get_ROI(src, horizontal, vertical, left_line_index, right_line_index, top_line_index, bottom_line_index)

    gray = get_grayscale(src)
    bw = get_binary_gaussian(gray)
    cv.imshow("bw", bw)
    cv.imwrite("bw.png", bw)
    bw = invert_area(bw, x, y, w, h, display=True)
    cv.imwrite("bw_inver.png", bw)
    #bw = erode(bw, kernel_size=2)

    cv.waitKey(0)

    ##set keywords
    keywords = ['no', 'kabupaten', 'kb_otg', 'kl_otg', 'sm_otg', 'ks_otg', 'not_cvd_otg',
            'kb_odp', 'kl_odp', 'sm_odp', 'ks_odp', 'not_cvd_odp',
            'kb_pdp', 'kl_pdp', 'sm_pdp', 'ks_pdp', 'not_cvd_pdp',
            'positif', 'sembuh', 'meninggal']
    
    dict_kabupaten = {}
    for keyword in keywords:
        dict_kabupaten[keyword] = []

    ## set counter for image indexing
    counter = 0

    ## set line index
    first_line_index = 1
    last_line_index = 14

    ## read text
    print("Start detecting text...")
    for i in range(first_line_index, last_line_index):
        for j, keyword in enumerate(keywords):
            counter += 1

            progress = counter/((last_line_index-first_line_index)*len(keywords)) * 100
            percentage = '%.2f' % progress 
            print("Progress: " + percentage + "%")

            left_line_index = j
            right_line_index = j+1
            top_line_index = i
            bottom_line_index = i+1

            cropped_image, (x,y,w,h) = get_ROI(bw, horizontal, vertical, left_line_index, right_line_index, top_line_index, bottom_line_index)

            if (keyword[j]=='kabupaten'):
                text = detect(cropped_image)
                dict_kabupaten[keyword].append(text)

                if(print_text):
                    print("Not number" + ', Row: ', str(i), ', Keyword: ' + keyword + ', Text: ', text )
            else: 
                text = detect(cropped_image, is_number=True)
                dict_kabupaten[keyword].append(text)

                if(print_text):
                    print("Is number" + ', Row: ', str(i), ', Keyword: ' + keyword + ', Text: ', text)

            if (display or write):
                image_with_text = draw_text(src, x, y, w, h, text)

            if (display):
                cv.imshow('detect', image_with_text)
                cv.waitKey(0)
                cv.destroyAllWindows()
            
            if(write):
                cv.imwrite('../static/images/' + str(counter) + '.png', image_with_text)

    print(dict_kabupaten)
    return 0

if __name__ == '__main__':
    main()