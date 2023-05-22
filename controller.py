from time import sleep

import vgamepad as vg

gamepad = vg.VX360Gamepad()


class Trigger:
    def __init__(self, trigger) -> None:
        self.trigger = trigger

    def btn_a(self):
        self.trigger(0x1000)

    def btn_b(self):
        self.trigger(0x2000)

    def btn_x(self):
        self.trigger(0x4000)

    def btn_y(self):
        self.trigger(0x8000)

    def btn_up(self):
        self.trigger(0x0001)

    def btn_down(self):
        self.trigger(0x0002)

    def btn_left(self):
        self.trigger(0x0004)

    def btn_right(self):
        self.trigger(0x0008)


def reset():
    gamepad.reset()
    gamepad.update()
    sleep(0.1)


def button(button):
    gamepad.press_button(button)
    gamepad.update()
    sleep(0.05)
    gamepad.release_button(button)
    gamepad.update()
    sleep(0.05)


def _rt_button(button):
    gamepad.right_trigger(value=255)
    gamepad.update()
    sleep(0.25)
    gamepad.press_button(button)
    gamepad.update()
    sleep(0.25)
    gamepad.right_trigger(value=0)
    gamepad.update()
    sleep(0.1)
    gamepad.release_button(button)
    gamepad.update()
    sleep(0.25)


def _lt_button(button):
    gamepad.left_trigger(value=255)
    gamepad.update()
    sleep(0.1)
    gamepad.press_button(button)
    gamepad.update()
    sleep(0.25)
    gamepad.left_trigger(value=0)
    gamepad.update()
    sleep(0.1)
    gamepad.release_button(button)
    gamepad.update()
    sleep(0.25)


left_trigger = Trigger(_lt_button)
right_trigger = Trigger(_rt_button)
