#!/usr/bin/python

# Import the needed libraries
import uinput
import time
import RPi.GPIO as GPIO
from evdev import UInput, ecodes as e

# This dictionary contains the map for the operative system events, the inputs in
# the GPIO interface for the Raspberry PI 2 and the function state in the arcade machine
#   [FUNCTION] = [PIN, STATE, EVENT]
# When a input signal in the GPIO interface is set to HIGH, the corresponding event is send
# to the operative system and the state is set to true in runtime until the signal is in LOW
interface = {
    "P1_UP": [29, False, e.KEY_W],
    "P1_DOWN": [35, False, e.KEY_S],
    "P1_LEFT": [33, False, e.KEY_A],
    "P1_RIGHT": [31, False, e.KEY_D],
    "P1_A": [23, False, e.KEY_K],
    "P1_B": [10, False, e.KEY_L],
    "P1_C": [7, False, e.KEY_Y],
    "P1_D": [11, False, e.KEY_U],
    "P1_X": [3, False, e.KEY_I],
    "P1_Y": [13, False, e.KEY_O],
    "P1_SELECT": [12, False, e.KEY_H],
    "P1_START": [15, False, e.KEY_G]
}


# Get all events in the interface
def get_events(item_list): return item_list[2]


# Set the GPIO pin as input with a pull up resistor
def input_setup(item_list):
    GPIO.setup(item_list[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print "SETUP GPIO {}".format(item_list[0])
    return


# Read the value configured in the interface and emit the corresponding event
def input_read(key, item_list):
    if (not item_list[1]) and (not GPIO.input(item_list[0])):
        item_list[1] = True
        with UInput() as ui:
            ui.write(e.EV_KEY, item_list[2], 2)
            ui.syn()
        print "KEY {} PRESS".format(key)
    if item_list[1] and GPIO.input(item_list[0]):
        item_list[1] = False
        with UInput() as ui:
            ui.write(e.EV_KEY, item_list[2], 0)
            ui.syn()
        print "KEY {} RELEASE".format(key)
    return


# Set the GPIO to use board pin mode
GPIO.setmode(GPIO.BOARD)

# Set all the used GPIO as inputs with pull up resistor
map(input_setup, interface.values())

# Start main infinite thread for read the inputs and emit the events
try:
    while True:
        for k, v in interface.iteritems():
            input_read(k, v)
        time.sleep(0.04)
except KeyboardInterrupt:
    print "BYE"
finally:
    GPIO.cleanup()
