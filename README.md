# SpotLock Senior Design Project

Created by: Paul-Wilson Kimloy Chang Fatt and Nicholas White

The design team set out to create a solution that could make finding parking more efficient. The solution created is a prototyped process flow to relay information on parking spots to a web application that drivers can use to inform themselves on parking spot availability before reaching their destination. 

===========================

This repository contains the code that runs on the parking spot monitoring hardware.

Hardware:

Raspberry Pi 4
1 Infared Sensor
3 Ultrasonic Sensors

Software Flow (Python):

1. Initalize all connections and sensors
2. Gather data from sensors to identify if a parking spot is taken
3. Send parking spot data to MongoDB database when there is a change in parking spot availability, via WIFI connection


===========================


