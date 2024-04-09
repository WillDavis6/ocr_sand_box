import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math
import sys

# SIMPLE THRESHING EXAMPLE

# img = cv.imread('C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\25-2355-865 F.png', cv.IMREAD_GRAYSCALE)
# assert img is not None, "file could not be read, check with os.path.exists()"
# ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
# ret,thresh2 = cv.threshold(img,127,255,cv.THRESH_BINARY_INV)
# ret,thresh3 = cv.threshold(img,127,255,cv.THRESH_TRUNC)
# ret,thresh4 = cv.threshold(img,127,255,cv.THRESH_TOZERO)
# ret,thresh5 = cv.threshold(img,127,255,cv.THRESH_TOZERO_INV)
 
# titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
# images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
 
# for i in range(6):
#  plt.subplot(2,3,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
#  plt.title(titles[i])
#  plt.xticks([]),plt.yticks([])
 
# plt.show()

#ADAPTIVE THRESHING EXAMPLE

# img = cv.imread('C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\25-2355-865 F.png', cv.IMREAD_GRAYSCALE)
# assert img is not None, "file could not read, check with os.path.exists"
# # img = cv.medianBlur(img,5)

# ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
# th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,11,2)
# th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)

# titles = ['Original Blueprint', 'Global Thresholding (v=127)', 'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
# images = [img, th1, th2, th3]

# for i in range(4):
#     plt.subplot(2,2,i+1),plt.imshow(images[i], 'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()

# OTSU'S THRESHOLDING EXAMPLE

# img = cv.imread('C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\25-2355-865 F.png', cv.IMREAD_GRAYSCALE)
# assert img is not None, 'file could not be read, check with os.path.exists()'

# #global thresholding
# ret1,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)

# #Otsu's thesholding
# ret2,th2 = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

# #Otsu's thresholding after Gaussian filetering
# blur = cv.GaussianBlur(img,(5,5),0)
# ret3,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

# # plot all the images adn their histograms
# images = [img, 0, th1, img, 0, th2, blur, 0, th3]
# titles = ['Original Nosiy Image', 'Histogram', 'Global Thresholding (v=127)', 'Original Noisy Image', 'Histogram', "Otsu's Thresholding", 'Gaussian filtered Image', 'Histogram', "Otsu's Thresholding"]

# for i in range(3):
#     plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
#     plt.title(titles[i*3]),plt.xticks([]),plt.yticks([])
#     plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
#     plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
#     plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2], 'gray')
#     plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
# plt.show() 


#The ideal pixel height for capital letters is 30-33px

#Try Dilation and Erosion for bleeding ink and expanded glyphs 

# SOURCE: https://github.com/fazlurnu/Text-Extraction-Table-Image/blob/master/scripts/ROI_selection.py

def is_vertical(line):
    return line[0]==line[2]

def is_horizontal(line):
    return line[1]==line[3]

def overlapping_filter(lines, sorting_index):
    filtered_lines = []

    lines = sorted(lines, key=lambda lines: lines[sorting_index])

    for i in range(len(lines)):
        l_curr = lines[i]
        if(i>0):
            l_prev = lines[i-1]
            if ( (l_curr[sorting_index] - l_prev[sorting_index]) > 5):
                filtered_lines.append(l_curr)
            else:
                filtered_lines.append(l_curr)

    return filtered_lines

def detect_lines(image, title='default', rho = 1, theta = np.pi/180, threshold = 50, minLinLength = 290, maxLineGap = 30, display = False, write = False):
    # Check if image is loaded fine
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    if gray is None:
        print('Error opening image!')
        return -1
    
    dst = cv.Canny(gray, 50, 150, None, 3)

    # Copy edges to the image that will display the results in BGR
    cImage = np.copy(image)

    #linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 290, 6)
    linesP = cv.HoughLinesP(dst, rho, theta, threshold, None, minLinLength, maxLineGap)

    horizontal_lines = []
    vertical_lines = []

    if linesP is not None:
        
        for i in range(0, len(linesP)):
            l = linesP[i][0]

            if (is_vertical(l)):
                vertical_lines.append(l)

            elif (is_horizontal(l)):
                horizontal_lines.append(l)

        horizontal_lines = overlapping_filter(horizontal_lines, 1)
        vertical_lines = overlapping_filter(vertical_lines, 0)

    if (display):
        for i, line in enumerate(horizontal_lines):
            cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,255,0), 3, cv.LINE_AA)

            cv.putText(cImage, str(i) + "v", (line[0], line[1] + 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)

        for i, line in enumerate(vertical_lines):
            cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
            cv.putText(cImage, str(i) + "v", (line[0], line[1] + 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)

        cv.imshow("Source", cImage)
        cv.waitKey(0)
        cv.destroyAllWindows()

    if (write):
        cv.imwrite("../Images/" + title + ".png", cImage)

    return (horizontal_lines, vertical_lines)

def get_cropped_image(image, x, y, w, h):
    cropped_image = image[ y:y+h , x:x+w]
    return cropped_image

def get_ROI(image, horizontal, vertical, left_line_index, right_line_index, top_line_index, bottom_line_index, offset=4):
    x1 = vertical[left_line_index][2] + offset
    y1 = horizontal[top_line_index][3] + offset
    x2 = vertical[right_line_index][2] - offset
    y2 = horizontal[bottom_line_index][3] - offset

    w = x2 - x1
    h = y2 - y1

    cropped_image = get_cropped_image(image, x1, y1, w, h)

    return cropped_image, (x1, y1, w, h)

def main(argv):

    default_file = '"C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\Screenshot 2024-04-08 123224.png"'
    filename = argv[0] if len(argv) > 0 else default_file

    src = cv.imread(cv.samples.findFile(filename))

    # Loads an image
    horizontal, vertical = detect_lines(src, display=True)

    return 0

if __name__ == "__main__":
    main(sys.argv[1:])