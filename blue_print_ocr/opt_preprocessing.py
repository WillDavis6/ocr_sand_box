import cv2 as cv
import numpy as np

def erode(img, kernel_size = 5):

    kernel = np.ones((kernel_size, kernel_size), np.uint64)
    img_erosion = cv.erode(img, kernel, iterations=4)
    return img_erosion

def get_all_grayscales(blueprint_url):

    scr = cv.imread(cv.samples.findFile(blueprint_url), cv.IMREAD_GRAYSCALE)

    scr2 = cv.medianBlur(scr,5)
    blur = cv.GaussianBlur(scr,(5,5),0)

    scr = erode(scr, 1)
    scr2 = erode(scr2, 1)
    blur = erode(blur, 1)


    ret, test1 = cv.threshold(scr,127,255,cv.THRESH_BINARY)
    ret, test2 = cv.threshold(scr,127,255,cv.THRESH_BINARY_INV)
    ret, test3 = cv.threshold(scr,127,255,cv.THRESH_TRUNC)
    ret, test4 = cv.threshold(scr,127,255,cv.THRESH_TOZERO)
    ret, test5 = cv.threshold(scr,127,255,cv.THRESH_TOZERO_INV)
    test6 = cv.adaptiveThreshold(scr2,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,11,2)
    test7 = cv.adaptiveThreshold(scr2,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
    ret, test8 = cv.threshold(scr,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    ret, test9 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    images = [scr, scr2, blur, test1, test2, test3, test4, test5, test6, test7, test8, test9]
    titles = ['Gray Scale', 'Medium Blur', 'Gaussian Blur', 'Thresh Binary', 'Thresh Binary Inv', 'Thresh Trunc', 'Thresh To Zero', 'Thresh To Zero Inv', 'Adaptive Thresh Mean C', 'Adaptive Thresh Gaussian C', 'Thresh Binary + Thresh Otsu', 'Blur + Thresh Binary + Thresh Otsu']

    return images, titles

def is_vertical(line):
    return line[0]==line[2]

def is_horizontal(line):
    return line[1]==line[3]

def overlapping_filter(lines, sorting_index):
# Check lines for one image against other lines of the same axis, uses currently line and previous line in a iterated list, if is closer than 20 pixels filtered out

    filtered_lines = []

    lines = sorted(lines, key=lambda lines: lines[sorting_index])

    for i in range(len(lines)):
        line_current = lines[i]
        if(i>0):
            line_previous = lines[i-1]
            if( (line_current[sorting_index] - line_previous[sorting_index]) > 4):
                #filtered_lines.append(line_current)
                pass
            else:
                filtered_lines.append(line_current)
    
    return filtered_lines




0

def detect_lines(image, title='default', rho = 1, theta = np.pi/180, threshold = 7, minLinLength = 1500, maxLinGap = 20, display = False, write = False):

    if image is None:
        print('Error opening image!')
        return -1
    
    height, width = image.shape[:2]
    
    dst = cv.Canny(image, 50, 150, False, 3)

    cImage = np.copy(image)

    cImage_color = cv.cvtColor(cImage, cv.COLOR_GRAY2BGR)

    linesP = cv.HoughLinesP(dst, rho, theta, threshold, None, minLinLength, maxLinGap)

    horizontal_lines = []
    vertical_lines = []
   

    if linesP is not None:

        for i in range(0, len(linesP)):
            l = linesP[i][0]

            if (is_vertical(l)):
                x1, y1, x2, y2 = l

                y1 = 0

                y2 = height

                vertical_lines.append([x1, y1, x2, y2])

            elif (is_horizontal(l)):
                x1, y1, x2, y2 = l

                x1 = 0

                x2 = width

                horizontal_lines.append([x1, y1, x2, y2])

        horizontal_lines = overlapping_filter(horizontal_lines, 1)
        vertical_lines = overlapping_filter(vertical_lines, 0)

        

    if (display):
        for i, line in enumerate(horizontal_lines):
            cv.line(cImage_color, (0, line[1]), (width, line[3]), (0,255,0), 1, cv.LINE_AA)

        for i, line in enumerate(vertical_lines):
            cv.line(cImage_color, (line[0], 0), (line[2], height), (0,0,255), 1, cv.LINE_AA)
  
        # cv.imshow("Thresh -> Lines -> To Color", cImage_color)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

    return cImage_color, horizontal_lines, vertical_lines



def euclidean_distance(line1, line2):
    """
    Calculate the Euclidean distance between the endpoints of two lines.
    """
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    dx = min(abs(x1 - x3), abs(x1 - x4), abs(x2 - x3), abs(x2 - x4))
    dy = min(abs(y1 - y3), abs(y1 - y4), abs(y2 - y3), abs(y2 - y4))
    return np.sqrt(dx**2 + dy**2)

def merge_lines(list_of_lines, buffer_zone):
    """
    Merge lines while avoiding duplicates within each sublist and across sublists.
    """
    merged_horizontal_lines = []
    merged_vertical_lines = []
    horizontal_lines = []
    vertical_lines = []

    num_images = 0
    num_hor_versus_vert = 0
    num_pack_of_lines = 0
    num_lines = 0


    for individual_image_lines in list_of_lines:
        num_images += 1
        for hor_versus_vert_lines in individual_image_lines:
            num_hor_versus_vert += 1
            for pack_of_lines in hor_versus_vert_lines:
                num_pack_of_lines += 1
                for line in pack_of_lines:
                    num_lines += 1
                    if is_horizontal(line):
                        horizontal_lines.append(line)
                        line_check(line, merged_horizontal_lines, buffer_zone)
                    elif is_vertical(line):
                        vertical_lines.append(line)
                        line_check(line, merged_vertical_lines, buffer_zone)
                    else:
                        pass

    print(f'Merge lines report, number of images: {num_images}. Number of packs of horizontal versus vertical {num_hor_versus_vert}. Number of pack of lines: {num_pack_of_lines}. Number of lines: {num_lines}')
    print(f'Number of merged horizontal lines: {len(merged_horizontal_lines)}.')
    print(f'Number of merged vertical lines: {len(merged_vertical_lines)}.')
    print(f'Number of horizontal lines: {len(horizontal_lines)}.')
    print(f'Number of vertical lines: {len(vertical_lines)}.')

    return [merged_horizontal_lines, merged_vertical_lines]





def line_check(line, merged_lines, buffer_zone):
    """
    Merge a line into the list of merged lines while avoiding duplicates.
    """

    if len(merged_lines) != 0:
    
        if any(euclidean_distance(line, merged_line) < buffer_zone for merged_line in merged_lines):
            pass
        else:
            merged_lines.append(line)
    elif len(merged_lines) == 0:
        print(f'This should only print once for line {line}')
        merged_lines.append(line)
     
def sort_lines(lines, sorting_index):

    sorted_lines = sorted(lines, key=lambda lines: lines[sorting_index])
    
    return sorted_lines


def show_merged_lines(all_lines, image_url):
    
    merged_horizontal_lines, merged_vertical_lines = merge_lines(all_lines, 20)

    merged_horizontal_lines = sort_lines(merged_horizontal_lines, 1)
    merged_vertical_lines = sort_lines(merged_vertical_lines, 0)

    cImage_color = cv.imread(image_url)

    height, width = cImage_color.shape[:2]
  
    for i, line in enumerate(merged_horizontal_lines):
        cv.line(cImage_color, (0, line[1]), (width, line[3]), (0,255,0), 1, cv.LINE_AA)

        cv.putText(cImage_color, str(i) + 'line', (0, line[1] + 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
    
    for i, line in enumerate(merged_vertical_lines):
        cv.line(cImage_color, (line[0], 0), (line[2], height), (0,0,255), 1, cv.LINE_AA)

        cv.putText(cImage_color, str(i) + 'line', (line[0], 0 + 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)

    

    #cv.imshow("Merged Lines", cImage_color)
    #cv.waitKey(0)
    #cv.destroyAllWindows()

    return merged_horizontal_lines, merged_vertical_lines, cImage_color