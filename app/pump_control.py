'''
Controls a water pump according to the configuration variables fetched from the database.
If sensor_enable == True, reads a moisture sensor according to a given time interval. 
If the sensor returns 0, the soil is moist and nothing happens. 
If the sensor returns 1, the soil is dry and the water pump gets turned on for a given
number of seconds. The pump start and stop timestamps get saved to the database.
If sensor_enable == False, watering happens according to watering_interval_hours
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


def read_sensor(seconds_to_pump):
	global client
	GPIO.output(27, 1) # set sensor vcc on
	sleep(1)
	moisture = GPIO.input(17)
	print(f"Moisture: {moisture}")
	if moisture == 0:
		print("ITS MOIST BABY")
	elif moisture == 1:
		print("DRY AS A DESERT")
		pump_activated = datetime.now()
		print(f"Pump started: {pump_started}")
		activate_pump(seconds_to_pump)
		pump_stopped = datetime.now()
		print(f"Pump stopped: {pump_stopped}")
		client.publish(topic='', payload=
			json.dumps({
			"table": "water_world_waterpump",
			"insert_dict": {
				"pump_activated": pump_activated,
				"pump_stopped": pump_stopped,
			}}))
	GPIO.output(27, 0) # set sensor vcc off


def activate_pump(seconds_to_pump):
	GPIO.output(20, 0) # set relays on
	GPIO.output(26, 0)
	print("WATEEEEEEEEEEEERRRR")
	sleep(seconds_to_pump)
	GPIO.output(20, 1) # set relays off
	GPIO.output(26, 1)
	

def main():
	global host, client, enable_system, seconds_to_pump, sensor_read_interval_hours, enable_sensor, watering_interval_hours, config_updated
	setup_pins()
	# initializing watering time to 72h from this moment and sensor reading to 1h from this moment
	watering_timestamp = datetime.datetime.now() + datetime.timedelta(hours=72)
	sensor_reading_timestamp = datetime.datetime.now() + datetime.timedelta(hours=1)
	previous_watering_interval = 0
	previous_sensor_interval = 0

	while True:
		# make a query to get data from table water_world_config
		client.publish(topic=host+'/database/query', payload=json.dumps({"table": "water_world_config"}))
		sleep(1)
		if config_updated == True: # if the query data came through
			if enable_system == True: # if system is turned on

				if enable_sensor == True: # if watering happens according to sensor reading
					if previous_sensor_interval != sensor_read_interval_hours:
						# update sensor_reading_timestamp
						time = datetime.datetime.now()
						sensor_reading_timestamp = time + datetime.timedelta(hours=sensor_read_interval_hours)
					if datetime.datetime.now() >= sensor_reading_timestamp:
						# it's time to read the sensor
						read_sensor(seconds_to_pump)
					
				else: # if watering happens according to time interval
					if previous_watering_interval != watering_interval_hours:
						# update watering_timestamp
						time = datetime.datetime.now()
						watering_timestamp = time + datetime.timedelta(hours=watering_interval_hours)
					if datetime.datetime.now() >= watering_timestamp: 
						# it's watering time
						activate_pump(seconds_to_pump)

			else: # system is turned off
				# publish success event that system is off and sensor wasn't read
				client.publish(topic='', payload=
					json.dumps({
					"table": "water_world_event",
					"insert_dict": {
						"pump_activated": pump_activated,
						"pump_stopped": pump_stopped,
					}}))
			config_updated = False
			sleep(600) # sleep 10 min


def on_connect(client, userdata, flags, rc):
	global subscribeTopic
	print("Connected to MQTT with result code " + str(rc))
	client.subscribe(subscribeTopic)


def on_message(client, userdata, msg):
	global enable_system, seconds_to_pump, sensor_read_interval_hours, enable_sensor, watering_interval_hours, config_updated
	# received data from database
	data = msg.payload.decode()
	print('data should be a list:', data)
	enable_system, seconds_to_pump, sensor_read_interval_hours, enable_sensor, watering_interval_hours = data
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
	enable_sensor = True
	watering_interval_hours = 72

	config_updated = False
	# starts looping callback functions in a separate thread
	client.loop_start()
	main()
