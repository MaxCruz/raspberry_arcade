#!/usr/bin/python

# Import the needed libraries
import uinput
import time
import RPi.GPIO as GPIO

# This dictionary contains the map for the operative system events, the inputs in
# the GPIO interface for the Raspberry PI 2 and the function state in the arcade machine
#   [FUNCTION] = [PIN, GPIO, STATE, EVENT]
# When a input signal in the GPIO interface is set to HIGH, the corresponding event is send
# to the operative system and the state is set to true in runtime until the signal is in LOW
interface = {
    "P1_UP": [3, 2, False, uinput.KEY_UP],
    "P1_DOWN": [5, 3, False, uinput.KEY_DOWN],
    "P1_LEFT": [7, 4, False, uinput.KEY_LEFT],
    "P1_RIGHT": [11, 17, False, uinput.KEY_RIGHT],
    "P1_A": [13, 27, False, uinput.KEY_0],
    "P1_B": [15, 22, False, uinput.KEY_2],
    "P1_C": [21, 9, False, uinput.KEY_3],
    "P1_D": [23, 11, False, uinput.KEY_4],
    "P1_X": [29, 5, False, uinput.KEY_5],
    "P1_Y": [31, 6, False, uinput.KEY_6],
    "P1_SELECT": [33, 13, False, uinput.KEY_7],
    "P1_START": [35, 19, False, uinput.KEY_8],
    "P2_UP": [37, 26, False, uinput.KEY_HOME],
    "P2_DOWN": [8, 14, False, uinput.KEY_END],
    "P2_LEFT": [10, 15, False, uinput.KEY_DELETE],
    "P2_RIGHT": [12, 18, False, uinput.KEY_PAGEDOWN],
    "P2_A": [18, 24, False, uinput.KEY_A],
    "P2_B": [22, 25, False, uinput.KEY_Z],
    "P2_C": [24, 8, False, uinput.KEY_S],
    "P2_D": [26, 7, False, uinput.KEY_X],
    "P2_X": [32, 12, False, uinput.KEY_D],
    "P2_Y": [36, 16, False, uinput.KEY_C],
    "P2_SELECT": [38, 20, False, uinput.KEY_F],
    "P2_START": [40, 21, False, uinput.KEY_V]
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
    if GPIO.input(item_list[0]):
        device.emit_click(item_list[3])
        print "KEY {} PRESS".format(key)
    # if (not item_list[2]) and (not GPIO.input(item_list[0])):
    #    item_list[2] = True
    #    device.emit(item_list[3], 1)
    #    print "KEY {} PRESS".format(key
    # if item_list[2] and GPIO.input(item_list[0]):
    #    item_list[2] = False
    #    device.emit(item_list[3], 0)
    #    print "KEY {} PRESS".format(key)
    return


# Set the GPIO to use board pin mode
GPIO.setmode(GPIO.BOARD)

# Set all the used GPIO as inputs with pull up resistor
map(input_setup, interface.values())

# Define input events to associate with the device
events = map(get_events, interface.values())
device = uinput.Device(events)

# Start main infinite thread for read the inputs and emit the events
try:
    while True:
        for k, v in interface.iteritems():
            input_read(k, v)
        time.sleep(0.2)
except KeyboardInterrupt:
    print "BYE"
finally:
    GPIO.cleanup()
