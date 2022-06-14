import vgamepad as vg
from time import sleep

gamepad = vg.VX360Gamepad()


def reset():
    gamepad.reset()
    gamepad.update()
    sleep(1)


def rt_button(button):
    gamepad.right_trigger(value=255)
    gamepad.update()
    sleep(0.3)
    gamepad.press_button(button)
    gamepad.update()
    sleep(0.3)
    gamepad.right_trigger(value=0)
    gamepad.update()
    sleep(0.3)
    gamepad.release_button(button)
    gamepad.update()
    sleep(0.3)


def lt_button(button):
    gamepad.left_trigger(value=255)
    gamepad.update()
    sleep(0.3)
    gamepad.press_button(button)
    gamepad.update()
    sleep(0.3)
    gamepad.left_trigger(value=0)
    gamepad.update()
    sleep(0.3)
    gamepad.release_button(button)
    gamepad.update()
    sleep(0.3)


def cast():
    rt_button(0x1000)


def hook():
    rt_button(0x2000)


def chum():
    rt_button(0x4000)


def thaliaks_favour():
    rt_button(0x8000)


def double_hook():
    return


def triple_hook():
    rt_button(0x0008)
