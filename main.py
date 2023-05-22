import threading
import time
from time import sleep

import cv2
import numpy as np
from PIL import ImageGrab

import controller
import matching

roi = (1080, 480, 1480, 880)
img = None
template = cv2.imread('!.png', 0)
cast_template = cv2.imread('cast.png', 0)
bite = 1

cast_time = time.time()
bite_time = time.time()
found_fish = False
catching = False
castable = False
patience = True
mooching = False
collectable = True
use_makeshift_bait = False
patience_timer = time.time()
cordial_timer = time.time()
max_fish_time = 8
catches = 0

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
cordial = controller.left_trigger.btn_down
makeshift_bait = controller.left_trigger.btn_up
prize_catch = controller.left_trigger.btn_b


def pre_cast():
    global cast_time, patience_timer, cordial_timer, use_makeshift_bait, castable

    if collectable:
        sleep(1)
        controller.button(0x1000)
        controller.button(0x1000)
    else:
        wait_until_castable()

    if time.time() - cordial_timer > float(180):
        print("Using cordial")
        cordial()
        cordial_timer = time.time()

    if patience and time.time() - patience_timer > float(145):
        sleep(1)
        print("Casting Patience II")
        patience_ii()
        patience_timer = time.time()

    # chum()
    # sleep(0.33)

    if catches % 3 == 0:
        t_favour()

    cast()
    cast_time = time.time()


def catch_fish():
    global cast_time, bite_time, found_fish, patience, catches, bite, max_fish_time, catching
    while True:
        if found_fish:
            found_fish = False
            catching = True
            sleep(0.1)
            bite_time = time.time()
            bite_delay = bite
            print(bite_delay)
            if bite_time - cast_time > max_fish_time:
                print(bite_time)
                print("Bite was longer than %s seconds" % max_fish_time)
                bite = 0
            elif bite == 1:
                precision_hookset()
                hook()
            elif bite == 2:
                hook()
            else:
                big_hookset()
                hook()

            if collectable:
                sleep(4.5 + (bite_delay * 3))
            catches += 1
            bite = 1
            print("catch done")
            pre_cast()
            catching = False


def able_to_cast():
    global img, castable
    px_loc = (44, 362)
    saturation = 236
    castable = matching.match_pixel(img, px_loc, saturation, 10)


def wait_until_castable():
    global img, castable
    px_loc = (44, 362)
    saturation = 236
    castable = matching.wait_for_pixel(img, px_loc, saturation, 10)


def main():
    global img, cast_time, found_fish, bite, castable, max_fish_time, catching
    pre_cast()
    while True:
        img = np.array(ImageGrab.grab(bbox=(roi)))
        found_fish, locations = matching.match(img, template, threshold=0.8)
        if len(locations) > bite:
            bite = len(locations)
        #        if len(locations) > 0:
        #            print(locations)
        cv2.putText(img, "!" * len(locations), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.imshow('Fishing', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if time.time() - cast_time > float(max_fish_time) and not catching:
            print("longer than %s recasting" % max_fish_time)
            hook()
            sleep(1.5)
            pre_cast()

        if time.time() - cast_time > float(50):
            print("should have had a bite by now")
            hook()
            sleep(1.5)
            pre_cast()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            controller.reset()
            cv2.destroyAllWindows()
            exit(0)


x = threading.Thread(target=catch_fish, daemon=True)
x.start()

if __name__ == '__main__':
    main()
