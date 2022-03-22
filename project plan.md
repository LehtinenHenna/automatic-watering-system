# Project Plan

## General
The project is about creating an automatic plant watering system that runs on Raspberry Pi.  
It has a web interface from which the user can control:  
- toggling the system on or off
- how many liters of water gets pumped each time the pump is turned on  
- how often the moisture sensor is read
The web interface should also have a login functionality, especially if it uses HTTPS protocol
The system also has a database that has time series data about when the water pump was turned on  

## Raspberry Pi
Docker Containers:  
  - MQTT (Mosquitto)  

Software:  
  - Tailscale SDWAN VPN  

## Motor
https://www.velleman.eu/products/view/?id=459186  

## Water sensor
https://components101.com/modules/soil-moisture-sensor-module  


## Extra
Ideas to develop the system in case we have extra time
- having a manual setting in the plant watering system, so that instead of the watering time being determined through the moisture sensor, user can determine using the web interface how often the water pump is turned on and for how many seconds each time  
- a sensor to track the water level in the water container, if the water level gets too low sends a warning message and shuts down water pump

