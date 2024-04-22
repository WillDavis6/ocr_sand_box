# ocr_optimization_for_poor_quality_blueprints
Compilation of ocr preprocessing options. Current ocr_optimization_testing.py involves using all mentioned threshing strategies, followed by cv.line, finally compiled with a euclidean distance function to find all possible lines. This work is primarly for images that are poor and can only improved with erosion, dilation, and different threshold stratigies. The primary use for these strategies are reading legacy blueprints.

Holds examples for threshing including, simple, adaptive and Otsu threshing.
    THRESH_BINARY
    THRESH_BINARY_INV
    THRESH_TRUNC
    THRESH_TOZERO
    THRESH_TOZERO_INV

    ADAPTIVE_THRESH_MEAN_C
    ADAPTIVE_THRESH_GAUSSIAN_C

    THRESH_OTSU

Additioanl long form example of how to perform OCR while ignoring table lines in both x and y directions. 



Notes about ideal pixel height (30-33px) For tesseract.



Prerequisities/Dependencies

PyTesseract
Numpy
OpenCV => 2.4.8


SOURCES: 
https://numpy.org/doc/
https://docs.opencv.org/4.x/index.html
https://tesseract-ocr.github.io/tessdoc/

SOURCE FOR LINE EXTRACTION:
https://github.com/fazlurnu/Text-Extraction-Table-Image/blob/master/scripts/ROI_selection.py
