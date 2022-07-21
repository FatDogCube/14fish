import threading
import time
from time import sleep

import cv2
import numpy as np
from PIL import ImageGrab

import controller
import matching

template = cv2.imread('!!.png', 0)
cast = cv2.imread('cast.png', 0)
bite = 1
bite_delay = 1
roi = (1080, 480, 1480, 880)
starttime = time.time()
found_fish = False
patience = True
mooching = False
collectable = True
patience_timer = time.time()

cast = controller.right_trigger.btn_a
hook = controller.right_trigger.btn_b
chum = controller.right_trigger.btn_x
t_favour = controller.right_trigger.btn_y
triple_hook = controller.right_trigger.btn_down

precision_hookset = controller.left_trigger.btn_a
powerful_hookset = controller.left_trigger.btn_y
big_hookset = controller.left_trigger.btn_y
mooch = controller.left_trigger.btn_x
patience_ii = controller.right_trigger.btn_right
state = ["Idle", "Fishing", "Reeling"]


def pre_cast():
    sleep(4.1 + (bite_delay * 3.1))
    global patience_timer
    # image = np.array(ImageGrab.grab(bbox=(roi)))
    # matching.wait_for(image, cast, timeout=15)
    print("catch done")
    if collectable:
        controller.button(0x1000)
        controller.button(0x1000)
    if patience and time.time() - patience_timer > float(145):
        sleep(1)
        print("casting Patience II")
        patience_ii()
        patience_timer = time.time()
    if mooching:
        mooch()
        mooch()
    else:
        chum()
        t_favour()
        cast()
        cast()


def catch_fish():
    global found_fish, starttime, bite_delay
    while True:
        if found_fish:
            sleep(0.1)
            if patience:
                bite_delay = bite
                if bite == 1:
                    precision_hookset()
                elif bite == 2:
                    powerful_hookset()
                else:
                    big_hookset()
            else:
                hook()
            pre_cast()
            starttime = time.time()
            found_fish = False


def find_cast():
    global roi
    image = np.array(ImageGrab.grab(bbox=(roi)))
    f, loc = matching.match(image, cast)
    w, h = cast.shape[::-1]
    if f:
        x1, y1 = roi[0] + loc[0], roi[1] + loc[1]
        cast_loc = (x1, y1, x1 + w, y1 + h)
        print(f"cast location at {cast_loc}")


def main():
    while True:
        global starttime, found_fish, bite
        img = np.array(ImageGrab.grab(bbox=(roi)))
        found_fish, locations = matching.match(img, template)
        bite = len(locations)
        cv2.putText(img, "!" * len(locations), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.imshow('Fishing', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if time.time() - starttime > float(39):
            print("should have had a bite by now")
            starttime = time.time()
            found_fish = True

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit(0)


x = threading.Thread(target=catch_fish, daemon=True)
x.start()

if __name__ == '__main__':
    main()
