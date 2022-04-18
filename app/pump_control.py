'''
Controls a water pump according to the configuration variables fetched from the database.
Reads a moisture sensor according to a given time interval. If the sensor returns 0, the soil is moist and
nothing is done. If the sensor returns 1, the soil is dry and it the water pump gets turned on for a given
number of seconds. The pump start and stop timestamps get saved to the database.
Saves event data to the database.
Uses store.py to communicate with the database.
'''

import signal
import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep
import paho.mqtt.client as mqtt
from socket import gethostname
import json


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
	global host, client, enable_system, seconds_to_pump, sensor_read_interval_hours, config_updated
	setup_pins()
	
	while True:
		# make a query to get data from table water_world_config
		client.publish(topic=host+'/database/query', payload=json.dumps({"table": "water_world_config"}))
		if config_updated == True: # if the query data came through
			if enable_system == True:
				# make the choice between watering according sensor reading and time interval
				# publish success event that system is on and sensor is being read
				read_sensor()
			else:
				# publish success event that system is off and sensor wasn't read
				client.publish()
			config_updated = False
			sleep(sensor_read_interval_hours)
		sleep(1)


def on_connect(client, userdata, flags, rc):
	global subscribeTopic
	print("Connected to MQTT with result code " + str(rc))
	client.subscribe(subscribeTopic)


def on_message(client, userdata, msg):
	global enable_system, seconds_to_pump, sensor_read_interval_hours, config_updated
	# received data from database
	data = msg.payload.decode()
	print('data should be a list:', data)
	enable_system, seconds_to_pump, sensor_read_interval_hours = data
	config_updated = True


if __name__ == "__main__":
	# initializing the MQTT client
	host = gethostname()
	print('host: ', host)
	subscribeTopic = host + '/store/#'
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect('mqtt', 1883, 60)
	# initializing config variables
	enable_system = False
	seconds_to_pump = 3
	sensor_read_interval_hours = 1

	config_updated = False
	# starts looping callback functions in a separate thread
	client.loop_start()
	main()
