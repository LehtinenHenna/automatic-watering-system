# Project Plan

## General
The project is about creating an automatic plant watering system that runs on Raspberry Pi. It reads a digital moisture sensor and when the soil is dry it starts a water pump for n seconds. It saves the timestamp information to MongoDB database of when the pump was turned on. The web server is accessed via tailscaled.  

## Django web server
Web interface from which the user can control:  
- toggling the system on or off
- how many liters of water gets pumped each time the pump is turned on  
- how often the moisture sensor is read 

## MongoDB database
- water pump table that has columns:  
  - timestamp of when the pump was turned on  
  - timestamp of when the pump was turned off  
- variables table that has columns:
  - how many hours in between sensor readings
  - system enable variable (true or false) that defines if the moisture sensor gets read or not (and therefore if the water pump gets turned on or not)
  - how many seconds the water pump is turned on for (django converts liters to seconds)  

## Raspberry Pi
Docker Containers:  
  - MQTT (Mosquitto)  

Software:  
  - Tailscale SDWAN VPN  
  
## Components  

### Motor
https://www.velleman.eu/products/view/?id=459186  

### Water sensor
https://components101.com/modules/soil-moisture-sensor-module  

### Water pump
hexagon is input, circle is output  

## Extra
Ideas to develop the system in case we have extra time
- having a manual setting in the plant watering system, so that instead of the watering time being determined through the moisture sensor, user can determine using the web interface how often the water pump is turned on and for how many seconds each time  
- a sensor to track the water level in the water container, if the water level gets too low sends a warning message and shuts down water pump

