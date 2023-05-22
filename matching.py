import time

import cv2
import numpy as np
from PIL import ImageGrab


def capture(roi):
    img = np.array(ImageGrab.grab(bbox=(roi)))
    return img


def match(img_rgb, template, threshold=0.8):
    found = False
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    w, h = template.shape[::-1]
    loc = np.where(res >= threshold)
    found_loc = set()
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        found_loc.add(pt)
        found = True
    points_to_remove = set()
    # remove points that are very close
    for x1, y1 in found_loc:
        for x2, y2 in found_loc:
            if x1 == x2 and y1 == y2:
                continue
            if (x2 - x1) ** 2 + (y2 - y1) ** 2 < 25:
                if res[x1][y1] > res[x2][y2]:
                    points_to_remove.add((x2, y2))
                else:
                    points_to_remove.add((x1, y1))
    found_loc -= points_to_remove
    return found, found_loc


def match_pixel(img_rgb, px_loc, saturation, threshold):
    pixel = img_rgb[px_loc[1]:px_loc[1] + 1, px_loc[0]:px_loc[0] + 1]
    pixel_hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
    lower = int(saturation - threshold / 2)
    upper = int(saturation + threshold / 2)
    if lower <= pixel_hsv[0][0][1] <= upper:
        return True, pixel_hsv[0][0][1]
    else:
        return False, pixel_hsv[0][0][1]


def wait_for(img, template, timeout=10):
    found = False
    location = None
    starttime = time.time()
    while not found:
        found, location = match(img, template)
        if found:
            break
        if time.time() > starttime + timeout:
            print("timeout!")
            break
    return found, location


def wait_for_pixel(img, px_loc, saturation, timeout):
    found = False
    starttime = time.time()
    while not found:
        found, location = match_pixel(img, px_loc, saturation, threshold=10)
        if found:
            break
        if time.time() > starttime + timeout:
            print("timeout!")
            break
    return found, location
