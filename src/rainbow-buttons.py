# SPDX-FileCopyrightText: 2021 Sandy Macdonald
#
# SPDX-License-Identifier: MIT

# A simple example of how to set up a keymap and HID keyboard on Keybow 2040.

# You'll need to connect Keybow 2040 to a computer, as you would with a regular
# USB keyboard.

# Drop the keybow2040.py file into your `lib` folder on your `CIRCUITPY` drive.

# NOTE! Requires the adafruit_hid CircuitPython library also!

import board
import time
from keybow2040 import Keybow2040

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

ORANGE = (255, 255, 0)
BLUE = (0, 255, 175)
PINK = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# LED brightness settings
HIGH_BRIGHTNESS = 1.0
MID_BRIGHTNESS = 0.2
LOW_BRIGHTNESS = 0.05


def rgb_with_brightness(r, g, b, brightness=1.0):
    # Allows an RGB value to be altered with a brightness
    # value from 0.0 to 1.0.
    r, g, b = (int(c * brightness) for c in (r, g, b))
    return r, g, b


# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# TODO: not LED sleeping...
# # Enable LED sleep and set a time of 5 seconds before the LEDs turn off.
# # They'll turn back on with a tap of any key!
# keybow.led_sleep_enabled = True
# keybow.led_sleep_time = 5


# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)


# RAINBOW BUTTON SHORTCUTS
rainbow_button_shortcuts = {
    14: ([Keycode.CONTROL, Keycode.SHIFT, Keycode.F17], BLUE),  # blue: F17
    15: ([Keycode.CONTROL, Keycode.SHIFT, Keycode.F14], RED),  # red: F14
    8: ([Keycode.CONTROL, Keycode.SHIFT, Keycode.F18], PINK),  # black: F18
    9: ([Keycode.CONTROL, Keycode.SHIFT, Keycode.F15], YELLOW),  # yellow: F15
    12: ([Keycode.CONTROL, Keycode.SHIFT, Keycode.F19], WHITE),  # white: F19
    13: ([Keycode.CONTROL, Keycode.SHIFT, Keycode.F16], GREEN),  # green: F16
}
##|---------------------------------------
##|     |         |            | red-F14
##|---------------------------------------
##|     |         |            | blue-F17
##|---------------------------------------
##|     |         | yellow-F15 | green-F16
##|---------------------------------------
##|     |         | black-F18 | white-F19
##|---------------------------------------


layers = {
    1: rainbow_button_shortcuts,
}
current_layer = 1

# initial set up of the leds for each key in the current layer
for k in layers[current_layer].keys():
    _, key_colour = layers[current_layer][k]
    keys[k].set_led(*rgb_with_brightness(*key_colour, brightness=MID_BRIGHTNESS))


# To prevent the strings (as opposed to single key presses) that are sent from
# refiring on a single key press, the debounce time for the strings has to be
# longer.
short_debounce = 0.125
long_debounce = 0.20
debounce = 0.125
fired = False


while True:
    # Always remember to call keybow.update()!
    keybow.update()

    for k in layers[current_layer].keys():
        key_press, key_colour = layers[current_layer][k]
        if keys[k].pressed:
            print("            Key {} pressed".format(k))

            if not fired:
                fired = True

                print("****************** Firing key {} ************************".format(k))
                if isinstance(key_press, list):
                    keyboard.send(*key_press)
                else:
                    keyboard.send(key_press)
                keys[k].set_led(*rgb_with_brightness(*key_colour, brightness=HIGH_BRIGHTNESS))

        else:
            # print("Not pressed Key {}".format(k))
            keys[k].set_led(*rgb_with_brightness(*key_colour, brightness=MID_BRIGHTNESS))

    if fired and time.monotonic() - keybow.time_of_last_press > debounce:
        fired = False






