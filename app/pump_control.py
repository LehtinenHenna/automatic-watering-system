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
from datetime import datetime, timedelta
from time import sleep
import paho.mqtt.client as mqtt
from socket import gethostname
import json
from traceback import format_exc


class GracefulShutdown:
    """
	Override termination signals behaviour to
	clean gpio pin setup on program exit.
	"""
    def __init__(self):
        self.shutdown_now = False
        signal.signal(signal.SIGINT, self.shutdown())
        signal.signal(signal.SIGTERM, self.shutdown())

    def shutdown(self, signum, frame):
        self.shutdown_now = True


def setup_pins():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.IN)  # Sensor input
	GPIO.setup(27, GPIO.OUT) # Sensor VCC
	GPIO.setup(26, GPIO.OUT) # Pump relay channel 1
	GPIO.setup(20, GPIO.OUT) # Pump relay channel 2


def read_sensor(seconds_to_pump):
	global client
	try:
		GPIO.output(27, 1) # set sensor vcc on
		sleep(1)
		moisture = GPIO.input(17)
		print(f"Moisture: {moisture}")
		if moisture == 0:
			print("ITS MOIST BABY")
		elif moisture == 1:
			print("DRY AS A DESERT")
			activate_pump(seconds_to_pump)
		GPIO.output(27, 0) # set sensor vcc off

	except:
		client.publish(topic=host+'/database/write', payload=
			json.dumps({
			"table": "water_world_event",
			"insert_dict": {
				"message": "pump control failed at read_sensor: " + format_exc(),
				"event_type": "Warning",
				"event_time": datetime.now().isoformat()
		}}))
		GPIO.output(20, 1) # set relays off
		GPIO.output(26, 1)


def activate_pump(seconds_to_pump):
	global client
	try:

		GPIO.output(20, 0) # set relays on
		GPIO.output(26, 0)
		pump_activated = datetime.now().isoformat()
		print(f"Pump started: {pump_activated}")
		print("WATEEEEEEEEEEEERRRR")
		sleep(seconds_to_pump)
		GPIO.output(20, 1) # set relays off
		GPIO.output(26, 1)
		pump_stopped = datetime.now().isoformat()
		print(f"Pump stopped: {pump_stopped}")

		client.publish(topic=host+'/database/write', payload=
			json.dumps({
			"table": "water_world_waterpump",
			"insert_dict": {
				"pump_activated": pump_activated,
				"pump_stopped": pump_stopped,
		}}))
	except:
		client.publish(topic=host+'/database/write', payload=
			json.dumps({
			"table": "water_world_event",
			"insert_dict": {
				"message": "pump control failed at activate_pump: " + format_exc(),
				"event_type": "Warning",
				"event_time": datetime.now().isoformat()
		}}))
		GPIO.output(20, 1) # set relays off
		GPIO.output(26, 1)
		

def main():
	try:
		global host, client, enable_system, system_mode, seconds_to_pump, sensor_read_interval_hours, watering_interval_hours, config_updated
		setup_pins()
		GPIO.output(20, 1) # set relays off
		GPIO.output(26, 1)

		sensor_mode = 1
		timer_mode = 2
		# initializing watering time to 72h from this moment and sensor reading to 1h from this moment
		watering_timestamp = datetime.now() + timedelta(hours=72)
		sensor_reading_timestamp = datetime.now() + timedelta(hours=1)
		previous_watering_interval = 0
		previous_sensor_interval = 0

		shutdown_handler = GracefulShutdown()

		while True:
			if shutdown_handler.shutdown_now:
				print("Shutting down gracefully...")
				GPIO.cleanup()
				print("GPIO pin setups cleaned")
				break

			# make a query to get data from table water_world_config and wait for the results
			client.publish(topic=host+'/database/query', payload=json.dumps({"table": "water_world_config"}))
			sleep(3)

			if config_updated == True: # if the query data came through
				print('config_updated true')
				if enable_system == True: # if system is turned on
					print('enable_system true')
					if system_mode == sensor_mode: # if watering happens according to sensor reading
						print('system_mode == sensor_mode')
						if previous_sensor_interval != sensor_read_interval_hours:
							# set new future moment for sensor reading
							time = datetime.now()
							sensor_reading_timestamp = time + timedelta(hours=sensor_read_interval_hours)
							previous_sensor_interval = sensor_read_interval_hours
						if datetime.now() >= sensor_reading_timestamp:
							print("it's time to read the sensor")
							# it's time to read the sensor
							read_sensor(seconds_to_pump)
							# set new future moment for sensor reading
							time = datetime.now()
							sensor_reading_timestamp = time + timedelta(hours=sensor_read_interval_hours)
						print('sensor_reading_timestamp', sensor_reading_timestamp)
						
					elif system_mode == timer_mode: # if watering happens according to time interval
						print('system_mode == timer_mode')
						if previous_watering_interval != watering_interval_hours:
							# set new future moment for watering
							time = datetime.now()
							watering_timestamp = time + timedelta(hours=watering_interval_hours)
							previous_watering_interval = watering_interval_hours
						if datetime.now() >= watering_timestamp:
							print("it's watering time") 
							# it's watering time
							activate_pump(seconds_to_pump)
							# set new future moment for watering
							time = datetime.now()
							watering_timestamp = time + timedelta(hours=sensor_read_interval_hours)
						print('watering_timestamp', watering_timestamp)

				else: # system is turned off
					# publish success event that system is off and sensor wasn't read
					client.publish(topic=host+'/database/write', payload=
						json.dumps({
						"table": "water_world_event",
						"insert_dict": {
							"message": "System is turned off",
							"event_type": "Success",
							"event_time": datetime.now().isoformat()
						}}))
				config_updated = False
				sleep(10) # sleep 10 sec
				print('***AT THE END OF THE LOOP***')
	except:
		client.publish(topic=host+'/database/write', payload=
			json.dumps({
			"table": "water_world_event",
			"insert_dict": {
				"message": "pump control failed at main: " + format_exc(),
				"event_type": "Warning",
				"event_time": datetime.now().isoformat()
		}}))
		GPIO.output(20, 1) # set relays off
		GPIO.output(26, 1)

def on_connect(client, userdata, flags, rc):
	global subscribeTopic
	print("Connected to MQTT with result code " + str(rc))
	client.subscribe(subscribeTopic)


def on_message(client, userdata, msg):
	global enable_system, system_mode, seconds_to_pump, sensor_read_interval_hours, enable_sensor, watering_interval_hours, config_updated
	try:
		# received data from database
		data = json.loads(msg.payload.decode())
		print('data:', data)

		enable_system = data['enable_system']
		system_mode = data['system_mode']
		seconds_to_pump = data['seconds_to_pump']
		sensor_read_interval_hours = data['sensor_read_interval_hours']
		watering_interval_hours = data['watering_interval_hours']

		config_updated = True
	except:
		client.publish(topic=host+'/database/write', payload=
			json.dumps({
			"table": "water_world_event",
			"insert_dict": {
				"message": "pump control failed at on_message: " + format_exc(),
				"event_type": "Warning",
				"event_time": datetime.now().isoformat()
		}}))
		GPIO.output(20, 1) # set relays off
		GPIO.output(26, 1)


if __name__ == "__main__":

	# initializing the MQTT client
	host = gethostname()
	print('host: ', host)
	subscribeTopic = host + '/store/#'
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect('mqtt', 1883, 60)

	config_updated = False

	# initializing config variables
	enable_system = False
	system_mode = 1
	seconds_to_pump = 3
	sensor_read_interval_hours = 1
	watering_interval_hours = 72

	# starts looping callback functions in a separate thread
	client.loop_start()
	main()