# How to run the experiment on your machine
The Things Network Application MQTT-to-Python3 starter <br>
[Code example reference](https://github.com/descartes/TheThingsStack-Integration-Starters/blob/main/MQTT-to-Tab-Python3/TTS.MQTT.Tab.py)
##
Setup up local environment
## 
At the root of the this derectory Python, duplicate the .env_tmp file and rename it into .env. You might need to enable the view of hidden files
```
cp .env_tmp .env
```
And then run the following to write water sensor data into linklab influxDB
```
Python3 jon_write_water_ttn_influx.py
```

## 
### Versioning
The dependency of this project is as below
- python==3.8.5
- influxDB==1.8.4
