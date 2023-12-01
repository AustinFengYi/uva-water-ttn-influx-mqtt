# uva-water-ttn-influx-mqtt
The goal of this project is to help get water sensor data on TTN to store in linklab influx DB. For now, the water sensor data [Pressure Sensors](https://nam1.cloud.thethings.network/console/applications/dl-pr-26) is used as an example that the final goal is to get the sensor data into the linklab influxDB.

Currently, some works have been done from Brad's team to help with converting water sensor to influx. This is [the code: http-ttn-mqtt.js](https://github.com/lab11/gateway/blob/master/software/http-ttn-mqtt/http-ttn-mqtt.js) they are using today to move data from TTN to influx. The program is implemented through the JavaScript programming language.

Below is the difference of data format on TTN between linklab registered TTN sensor and water sensor. Therefore, the main issues we have and already addressed are
1. Data names, refer to [link lab cloud](https://infrastructure.linklab.virginia.edu/linklabcloud/index.html) for more details 
    - It includes the naming definition (volatge_V v.s Battery voltage) and unit of the measuremant (hpa v.s bar)
2. [Data format on TTN](https://github.com/AustinFengYi/uva-water-ttn-influx-mqtt/blob/main/python/learn_json_water_payload_adaption/Comparison_TTN_JSON_format.png)
    - The main difference is the decoded_payload on TTN between linklab registered sensor and water sensor

Therefore, the high-level description of the implementation is to add a script between water sensor on TTN and [http-ttn-mqtt.js](https://github.com/lab11/gateway/blob/master/software/http-ttn-mqtt/http-ttn-mqtt.js) to make water sensor's decoded_payload match the linklab registered TTN sensors decoded_payload format, and then we can use [http-ttn-mqtt.js](https://github.com/lab11/gateway/blob/master/software/http-ttn-mqtt/http-ttn-mqtt.js) to pull data of water sensor from TTN and push it to InfluxDB. 

Here is to the [data visualization on Grafana](https://grafana.linklab.virginia.edu/d/_fXws54nk/austins-dashboard?orgId=1) to demo the work. With the help of the [script](https://github.com/AustinFengYi/uva-water-ttn-influx-mqtt/blob/main/python/jon_write_water_ttn_influx.py) for TTN decode_payload adpatation (in Python), for now we are getting water sensor data into linklab.influxDB using the datasource "link-users" (testing)
## 
Subsequently, this has two issues:
- It really only supports a single TTN application and API key
- It is manually configured and each new TTN application requires a sysadmin (ie Brad) to configure a new connection.
- We need a more scalable solution. This would include:
    - Support for multiple TTN applications and API keys
    - Users can add their applications automatically somehow

## 
What’s next: (it will be adjusted after the discussion)
1. Implement the script of the adaption for TTN data payload from water sensor to Brad’s ttn-influx **using a Javascript version**
2. A scalable solution as mentioned in the notes to support for multiple TTN applications and API keys
3. See how it works so we can get the water sensor into the linklab formal influx DB (“uva-generic-gateway”)
## 
### How to run the program
1. Go to the directory [Python](https://github.com/AustinFengYi/uva-water-ttn-influx-mqtt/tree/main/python), and the run Python jon_write_water_ttn_influx.py
```
python3 jon_write_water_ttn_influx.py
```
2. With the help of script [water_payload_adaptation.py](water_payload_adaptation.py) and [write_to_influx.py
](https://github.com/AustinFengYi/uva-water-ttn-influx-mqtt/blob/main/python/service/write_to_influx.py) in directory [service](https://github.com/AustinFengYi/uva-water-ttn-influx-mqtt/tree/main/python/service), we'are getting water sensor data into linklab.influxDB and visualize it through the linklab.Grafana dashboard. 

![截圖 2023-12-01 上午11.51.41](https://hackmd.io/_uploads/Syhdy5wS6.png)
