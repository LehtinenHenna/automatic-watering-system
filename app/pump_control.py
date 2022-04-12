import signal
import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep


def setup_pins():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.IN)  # Sensor input
	GPIO.setup(27, GPIO.OUT) # Sensor VCC
	GPIO.setup(26, GPIO.OUT) # Pump relay channel 1
	GPIO.setup(20, GPIO.OUT) # Pump relay channel 2

def read_sensor():
	GPIO.output(27, 1) # set sensor vcc on
	sleep(1)
	moisture = GPIO.input(17)
	print(f"Moisture: {moisture}")
	if moisture == 0:
		print("ITS MOIST BABY")
	elif moisture == 1:
		print("DRY AS A DESERT")
		print(f"Pump started: {datetime.now()}")
		activate_pump()
		print(f"Pump stopped: {datetime.now()}")
	GPIO.output(27, 0) # set sensor vcc off

def activate_pump():
	GPIO.output(20, 0) # set relays on
	GPIO.output(26, 0)
	print("WATEEEEEEEEEEEERRRR")
	sleep(5)
	GPIO.output(20, 1) # set relays off
	GPIO.output(26, 1)

def main():
	setup_pins()
	
	while True:
		sleep(10)
		read_sensor()
		
if __name__ == "__main__":
	main()
