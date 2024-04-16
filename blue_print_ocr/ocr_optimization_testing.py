import cv2 as cv
import sys
from matplotlib import pyplot as plt
from opt_preprocessing import get_all_grayscales, detect_lines


blueprint_url =  "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\images\\table_test.png"
export_url = "C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\test_updated_image_cv2.png"


def ocr_magic(bluprint_url, export_url):

    

    images, titles = get_all_grayscales(blueprint_url)

    for i, image in enumerate(images):
        cimage = detect_lines(image, minLinLength=500, display=True, write=True)
        images[i] = cimage
        # cv.imshow(f'image iteration {i}', cimage)
        # cv.waitKey(0)

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

ocr_magic(blueprint_url, export_url)