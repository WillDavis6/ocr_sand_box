import cv2 as cv
import sys
from matplotlib import pyplot as plt
from preprocessing import detect_lines


blueprint_url =  "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\images\\table_test.png"
export_url = "C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\test_updated_image_cv2.png"


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

for i, image in enumerate(images):
    horizontal_lines, vertical_lines, cimage = detect_lines(image, minLinLength=500, display=True, write=True)
    images[i] = cimage

for i in range(10):
    plt.subplot(2,5,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()

# if scr is None:
#     sys.exit("Could not read the image.")

# cv.imshow("Display window", scr)
# k = cv.waitKey(0)

# if k == ord('s'):
#     cv.imwrite(export_url, scr)