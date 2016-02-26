#!/usr/bin/python

# Import the needed libraries
import uinput
import time
import RPi.GPIO as GPIO

# This dictionary contains the map for the operative system events, the inputs in
# the GPIO interface for the Raspberry PI 2 and the function state in the arcade machine
#   [FUNCTION] = [PIN, GPIO, STATE, EVENT, IS_AXIS]
# When a input signal in the GPIO interface is set to HIGH, the corresponding event is send
# to the operative system and the state is set to true in runtime until the signal is in LOW
interface = {
    "P1_UP": [3, 2, False, uinput.KEY_0],
    "P1_DOWN": [5, 3, False, uinput.KEY_1],
    "P1_LEFT": [7, 4, False, uinput.KEY_2],
    "P1_RIGHT": [11, 17, False, uinput.KEY_3],
    "P1_A": [13, 27, False, uinput.KEY_4],
    "P1_B": [15, 22, False, uinput.KEY_5],
    "P1_C": [21, 9, False, uinput.KEY_6],
    "P1_D": [23, 11, False, uinput.KEY_7],
    "P1_X": [29, 5, False, uinput.KEY_8],
    "P1_Y": [31, 6, False, uinput.KEY_9],
    "P1_SELECT": [33, 13, False, uinput.KEY_M],
    "P1_START": [35, 19, False, uinput.KEY_N],
    "P2_UP": [37, 26, False, uinput.KEY_A],
    "P2_DOWN": [8, 14, False, uinput.KEY_B],
    "P2_LEFT": [10, 15, False, uinput.KEY_C],
    "P2_RIGHT": [12, 18, False, uinput.KEY_D],
    "P2_A": [18, 24, False, uinput.KEY_E],
    "P2_B": [22, 25, False, uinput.KEY_F],
    "P2_C": [24, 8, False, uinput.KEY_G],
    "P2_D": [26, 7, False, uinput.KEY_H],
    "P2_X": [32, 12, False, uinput.KEY_I],
    "P2_Y": [36, 16, False, uinput.KEY_J],
    "P2_SELECT": [19, 10, False, uinput.KEY_K],
    "P2_START": [40, 21, False, uinput.KEY_L]
}


# Get all events in the interface
def get_events(item_list): return item_list[3]


# Set the GPIO pin as input with a pull up resistor
def input_setup(item_list):
    GPIO.setup(item_list[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print "SETUP GPIO {}".format(item_list[0])
    return


# Read the value configured in the interface and emit the corresponding event
def input_read(key, item_list):
    if (not item_list[2]) and (not GPIO.input(item_list[0])):
        item_list[2] = True
        device.emit(item_list[3], 1)
        print "KEY {} PRESS".format(key)
    if item_list[2] and GPIO.input(item_list[0]):
        item_list[2] = False
        device.emit(item_list[3], 0)
        print "KEY {} RELEASE".format(key)
    return


# Set the GPIO to use board pin mode
GPIO.setmode(GPIO.BOARD)

# Set all the used GPIO as inputs with pull up resistor
map(input_setup, interface.values())

# Define input events to associate with the device
events = set(map(get_events, interface.values()))
device = uinput.Device(events)

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
