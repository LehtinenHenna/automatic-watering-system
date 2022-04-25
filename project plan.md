# Project Plan

## General
The project is about creating an automatic plant watering system that runs on Raspberry Pi. It has two watering modes, sensor mode and timer mode. In sensor mode it reads a digital moisture sensor and when the soil is dry it starts a water pump for n seconds. In timer mode the watering happens according to a timer interval. It saves the timestamp information to MongoDB database of when the pump was turned on. It has a Django web server that enables the user to make changes to the configuration variables and a view that displays system events and a view that displays the water pump timestamps. The user can access the web server via tailscaled.  

## Django web server
Web interface from which the user can control:  
- toggling the system on or off  
- how many seconds the pump gets turned on for each time  
- how often the moisture sensor is read  
- system mode to choose timer mode or sensor mode  
- watering interval hours for timer mode  

## MongoDB database
- water pump table that has columns:  
  - timestamp of when the pump was turned on  
  - timestamp of when the pump was turned off  
- variables table that has columns:
  - how many hours in between sensor readings
  - system enable variable (true or false) that defines if the moisture sensor gets read or not (and therefore if the water pump gets turned on or not)
  - how many seconds the water pump is turned on for  
  - watering interval hours for timer mode
  - system mode (1 for sensor mode and 2 for timer mode)  

## Raspberry Pi
Docker Containers:  
  - MQTT (Mosquitto)  
  - Django web server
  - App (running store.py that makes queries to the database and pump_control.py to control the water pump)

Software:  
  - Tailscale SDWAN VPN  
  
## Components  

### Motor
https://www.velleman.eu/products/view/?id=459186  

### Water sensor
https://components101.com/modules/soil-moisture-sensor-module  

### Water pump
hexagon is input, circle is output  
blue wire is positive (anode), yellow wire is negative (cathode)

## Extra
Ideas to develop the system in case we have extra time
- a camera to make time lapse videos and improved remote monitoring of plants
- a sensor to track the water level in the water container, if the water level gets too low sends a warning message and shuts down water pump  
- improved water output so that different plants get different amount of water, controlled by valves for example 
- improved UI/UX for the web pages

