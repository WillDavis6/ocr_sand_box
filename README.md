# ocr_sand_box
Data base for ocr pre image processing and enhancment

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

Notes about Dilation and Erosion to be added.

Notes about ideal pixel height (30-33px) For tesseract.



Prerequisities/Dependencies

PyTesseract
Numpy
OpenCV => 2.4.8