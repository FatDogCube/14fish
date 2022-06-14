import threading
import time
from time import sleep
import cv2 as cv
import numpy as np
from PIL import ImageGrab

import controller

template = cv.imread('!!.png', 0)
w, h = template.shape[::-1]
roi = (1080, 480, 1480, 880)
starttime = time.time()
found_fish = False

cast = controller.right_trigger.btn_a
hook = controller.right_trigger.btn_b
chum = controller.right_trigger.btn_x
t_favour = controller.right_trigger.btn_y
triple_hook = controller.right_trigger.btn_down


def match(img_rgb):
    found = False
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        found = True
    cv.imshow('Fishing', cv.cvtColor(img_rgb, cv.COLOR_BGR2RGB))

    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        exit(0)
    return found


def catch_fish():
    global found_fish
    global starttime
    while True:
        if found_fish:
            # controller.triple_hook()
            hook()
            sleep(8)
            print("catch done")
            chum()
            t_favour()
            cast()
            starttime = time.time()
            found_fish = False


x = threading.Thread(target=(catch_fish), daemon=True)
x.start()

while True:
    img = np.array(ImageGrab.grab(bbox=(roi)))
    if match(img):
        found_fish = True

    if time.time() - starttime > float(40):
        print("should have had a bite by now")
        starttime = time.time()
        found_fish = True
