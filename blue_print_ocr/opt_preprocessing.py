import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
import cv2 as cv
import numpy as np

def erode(img, kernel_size = 5):

    kernel = np.ones((kernel_size, kernel_size), np.unit8)
    img_erosion = cv.dilate(img, kernel, iternations=2)
    return img_erosion

def get_all_grayscales(blueprint_url):

    scr = cv.imread(cv.samples.findFile(blueprint_url), cv.IMREAD_GRAYSCALE)
    scr2 = cv.medianBlur(scr,5)
    blur = cv.GaussianBlur(scr,(5,5),0)


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

def detect_lines(image, title='default', rho = 1, theta = np.pi/180, threshold = 7, minLinLength = 1500, maxLinGap = 30, display = False, wrtie = False):

    if image is None:
        print('Error opening image!')
        return -1
    
    dst = cv.Canny(image, 50, 150, 3, True)

    cImage = np.copy(image)

    linesP = cv.HoughLinesP(dst, rho, theta, threshold, None, minLinLength, maxLinGap)

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
            cv.line(cImage, (0, line[1]), (800, line[3]), (0,255,0), 3, cv.LINE_AA)

