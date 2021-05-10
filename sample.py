import cv2 as cv 
import sys
import numpy as np

img = cv.imread("IMG_0039.jpg")

if img is None:
    sys.exit("Could not read the image.")

# HSV色空間に変換する
img_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# 色相(Hue)、彩度(Saturation・Chroma)、明度(Value・Brightness)に分割する
img_H, img_S, img_V = cv.split(img_HSV)

# 色相の閾値でマスク画像を作る
# https://qiita.com/oyngtmhr/items/26a2feec9ca9b09a8d72
_thre, img_marker = cv.threshold(img_H, 0, 60, cv.THRESH_BINARY)

# 輪郭取得
contours, hierarchy = cv.findContours(img_marker, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)


for i in range(0, len(contours)):
    if len(contours[i]) > 0:

        # 輪郭の面積が小さいものは無視する (これがないと細かい色の変化も輪郭描いちゃう)
        if cv.contourArea(contours[i]) < 500:
            continue

        # 輪郭から外接矩形を取得して画像に書き込む（確認用）
        rect = contours[i]
        x, y, w, h = cv.boundingRect(rect)
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 10)

        # 外接矩形で画像を切り出して出力する
        cv.imwrite(str(i) + ".jpg", img[y:y+h, x:x+w])

        print(x, y, w, h)

cv.imshow('maker2.jpg', img)

cv.waitKey(0)