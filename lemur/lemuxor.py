import cv2
foo = cv2.imread("./lemux.png")
bar = cv2.imread("./flag.png")
key = cv2.bitwise_xor(foo, bar)
cv2.imwrite("xoreddata.png", key)

