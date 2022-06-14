import vgamepad as vg
from time import sleep

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


def _reset():
    gamepad.reset()
    gamepad.update()
    sleep(1)


def _rt_button(button):
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


def _lt_button(button):
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


left_trigger = Trigger(_lt_button)
right_trigger = Trigger(_rt_button)

