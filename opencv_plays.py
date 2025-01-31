import cv2 as cv

pic_path = ""
img = cv.imread(pic_path)
cv.imshow("Image", img)
k = cv.waitKey(0)
