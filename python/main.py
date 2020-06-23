import json
import imutils
from imutils.perspective import four_point_transform
import base64
import cv2
from io import BytesIO
from PIL import Image
import numpy as np
import flask
from flask import request

STATICS = "web"
app = flask.Flask(__name__, root_path=".", static_folder=STATICS)


@app.route('/', methods=["GET"])
def root():
    return app.send_static_file('index.html')


@app.route("/ledDetection", methods=["POST"])
def led_detection():
    args = json.loads(request.form["data"])

    # missing_padding = len(args["img"]) % 4
    # if missing_padding != 0:
    #     args["img"] += '=' * (4 - missing_padding)
    nparr = np.frombuffer(base64.b64decode(args["img"]), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array(args["lowerb"])
    upper_red = np.array(args["upperb"])

    # Here we are defining range of bluecolor in HSV
    # This creates a mask of white coloured
    # objects found in the frame.
    mask = cv2.inRange(hsv, lower_red, upper_red)

    blurred = cv2.GaussianBlur(mask, (13, 13), 0)

    edged = cv2.Canny(blurred, 100, 200, 255)

    # Dilate it , number of iterations will depend on the image
    dilate = cv2.dilate(edged, (5, 5), iterations=1)
    # perform erosion
    erode = cv2.erode(dilate, (5, 5), iterations=1)

    # find contours in the edge map, then sort them by their
    # size in descending order
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    displayCnts = []
    # loop over the contours
    for c in cnts:
        # approximate the contour
        if cv2.contourArea(c) > 115:
            print(cv2.contourArea(c))
        # peri = cv2.arcLength(c, True)
        # approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if the contour has four vertices, then we have found
        # the thermostat display
        if cv2.contourArea(c) > 115:
            displayCnts.append(c)
    for displayCnt in displayCnts:
        print(cv2.contourArea(displayCnt))
    # output = four_point_transform(img, displayCnts[0].reshape(4, 2))
    output = cv2.drawContours(img, displayCnts, -1, (0, 255, 255), 8)

    # The bitwise and of the frame and mask is done so
    # that only the blue coloured objects are highlighted
    # and stored in res
    # res = cv2.bitwise_and(img, img, mask=mask)
    # # Blur the image
    # res = cv2.GaussianBlur(mask, (13, 13), 0)
    # # Edge detection
    # edged = cv2.Canny(res, 50, 200, 255)

    retval, buffer = cv2.imencode('.png', mask)
    mask_as_text = base64.b64encode(buffer)

    return {"result": "data:image/png;base64," + mask_as_text.decode('utf-8')}


@app.route("/digitRecognize", methods=["POST"])
def digit_recognize():
    print(request.form)
    return request.form


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
