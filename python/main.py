# coding=utf-8
import json
import imutils
from imutils import contours
import base64
import cv2
import numpy as np
import flask
from flask import request
from utils import detection, decorator

STATICS = "web"
app = flask.Flask(__name__, root_path=".", static_folder=STATICS)


@app.route('/', methods=["GET"])
def root():
    return app.send_static_file('index.html')


@app.route("/ledDetection", methods=["POST"])
@decorator.exception_handler
def led_detection():
    args = json.loads(request.form["data"])

    np_arr = np.frombuffer(base64.b64decode(args["img"]), np.uint8)
    lower_b = np.array(args["lowerb"])
    upper_b = np.array(args["upperb"])

    img = cv2.imdecode(np_arr, cv2.IMREAD_ANYCOLOR)
    img = imutils.resize(img, height=800)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_b, upper_b)
    blurred = cv2.GaussianBlur(mask, (5, 5), 0)
    dilate = cv2.dilate(blurred, (3, 3), iterations=1)
    erode = cv2.erode(dilate, (3, 3), iterations=1)
    edged = cv2.Canny(erode, 50, 200, 255)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    x_res, y_res, w_res, h_res = 0, 0, 0, 0
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w * h > w_res * h_res:
            x_res, y_res, w_res, h_res = x, y, w, h

    output = cv2.rectangle(img, (x_res, y_res), (x_res + w_res, y_res + h_res), (0, 255, 0), 2)

    crop_img = img[y_res:y_res + h_res, x_res:x_res + w_res]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    morph_image = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    cnts_digital = cv2.findContours(morph_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_digital = imutils.grab_contours(cnts_digital)
    digitCnts = contours.sort_contours(cnts_digital, method="left-to-right")[0]

    x_res, y_res, w_res, h_res = 0, 0, 0, 0
    for i, c in enumerate(digitCnts):
        (x, y, w, h) = cv2.boundingRect(c)
        if w * h > w_res * h_res:
            x_res, y_res, w_res, h_res = x, y, w, h

    crop_thresh = 255 - thresh[y_res:y_res + h_res, x_res:x_res + w_res]
    height, width = crop_thresh.shape

    dilate = cv2.dilate(crop_thresh, None, iterations=2)
    erode = cv2.erode(dilate, None, iterations=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    morph_image = cv2.morphologyEx(dilate, cv2.MORPH_OPEN, kernel)

    cnts_digital = cv2.findContours(morph_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_digital = imutils.grab_contours(cnts_digital)
    digitCnts = contours.sort_contours(cnts_digital, method="left-to-right")[0]

    digits = []
    for i, c in enumerate(digitCnts):
        (x, y, w, h) = cv2.boundingRect(c)
        roi = crop_thresh[y:y + h, x:x + w]
        if (h > height * 0.5) & (w < width * 0.3):
            digit = detection.resolve_digit(roi)
            if digit is None:
                digits.append(1)
            else:
                digits.append(digit)
    print(digits)

    retval, buffer = cv2.imencode('.png', output)
    mask_as_text = base64.b64encode(buffer)

    return {"result": "data:image/png;base64," + mask_as_text.decode('utf-8'), "success": True}


@app.route("/digitRecognize", methods=["POST"])
@decorator.exception_handler
def digit_recognize():
    args = json.loads(request.form["data"])

    np_arr = np.frombuffer(base64.b64decode(args["img"]), np.uint8)
    lower_b = np.array(args["lowerb"])
    upper_b = np.array(args["upperb"])

    img = cv2.imdecode(np_arr, cv2.IMREAD_ANYCOLOR)
    img = imutils.resize(img, height=800)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_b, upper_b)
    blurred = cv2.GaussianBlur(mask, (5, 5), 0)
    dilate = cv2.dilate(blurred, (3, 3), iterations=1)
    erode = cv2.erode(dilate, (3, 3), iterations=1)
    edged = cv2.Canny(erode, 50, 200, 255)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    x_res, y_res, w_res, h_res = 0, 0, 0, 0
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w * h > w_res * h_res:
            x_res, y_res, w_res, h_res = x, y, w, h

    output = cv2.rectangle(img, (x_res, y_res), (x_res + w_res, y_res + h_res), (0, 255, 0), 2)

    crop_img = img[y_res:y_res + h_res, x_res:x_res + w_res]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    morph_image = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    cnts_digital = cv2.findContours(morph_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_digital = imutils.grab_contours(cnts_digital)
    digitCnts = contours.sort_contours(cnts_digital, method="left-to-right")[0]

    x_res, y_res, w_res, h_res = 0, 0, 0, 0
    for i, c in enumerate(digitCnts):
        (x, y, w, h) = cv2.boundingRect(c)
        if w * h > w_res * h_res:
            x_res, y_res, w_res, h_res = x, y, w, h

    crop_thresh = 255 - thresh[y_res:y_res + h_res, x_res:x_res + w_res]
    height, width = crop_thresh.shape

    dilate = cv2.dilate(crop_thresh, None, iterations=2)
    erode = cv2.erode(dilate, None, iterations=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    morph_image = cv2.morphologyEx(dilate, cv2.MORPH_OPEN, kernel)

    cnts_digital = cv2.findContours(morph_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_digital = imutils.grab_contours(cnts_digital)
    digitCnts = contours.sort_contours(cnts_digital, method="left-to-right")[0]

    digits = []
    for i, c in enumerate(digitCnts):
        (x, y, w, h) = cv2.boundingRect(c)
        roi = crop_thresh[y:y + h, x:x + w]
        if (h > height * 0.5) & (w < width * 0.3):
            digit = detection.resolve_digit(roi)
            if digit is None:
                digits.append(1)
            else:
                digits.append(digit)
    print(digits)

    retval, buffer = cv2.imencode('.png', output)
    mask_as_text = base64.b64encode(buffer)

    return {"result": "data:image/png;base64," + mask_as_text.decode('utf-8'), "success": True}


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
