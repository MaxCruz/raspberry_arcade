import uinput
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)

events = (uinput.BTN_JOYSTICK, uinput.ABS_X + (0, 255, 0, 0), uinput.ABS_Y + (0, 255, 0, 0))

device = uinput.Device(events)

pin7 = False
pin8 = False

device.emit(uinput.ABS_X, 128, syn=False)
device.emit(uinput.ABS_Y, 128)

while True:
	if (not pin7) and (not GPIO.input(7)):
		pin7 = True
		device.emit(uinput.BTN_JOYSTICK, 1)
		print "PIN 7 PRESSED"
	if pin7 and GPIO.input(7):
		pin7 = False
		device.emit(uinput.BTN_JOYSTICK, 0)
		print "PIN 7 RELEASE"
	if (not pin8) and (not GPIO.input(8)):
		pin8 = True
		device.emit(uinput.ABS_Y, 0)
		print "PIN 8 PRESSED"
	if pin8 and GPIO.input(8):
		pin8 = False
		device.emit(uinput.ABS_Y, 128)
		print "PIN 8 RELEASE"
	time.sleep(0.2)
