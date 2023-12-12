""" Connect to MQTT Server and receive uplink messages using the Paho MQTT Python client library
#
# Refer to MQTT-to-Python3 starter:
# https://github.com/descartes/TheThingsStack-Integration-Starters/blob/main/MQTT-to-Tab-Python3/TTS.MQTT.Tab.py
#
# The program is writen in Python followed by Brad's http-ttn-mqtt.js format
# https://github.com/lab11/gateway/blob/master/software/http-ttn-mqtt/http-ttn-mqtt.js
#
"""
#
import sys
import logging
import paho.mqtt.client as mqtt
import json
import random
from datetime import datetime
from decouple import config
from service import write_to_influx, water_payload_adaptation

# // Read in the config file to get the parameters. 
# // Login to The Things Stack Community Edition console to get the 
#   1.USER 2.PASSWORD 3.PUBLIC_TLS_ADDRESS 4.PUBLIC_TLS_ADDRESS_PORT
USER = config('TTN_WATER2_USER') 
PASSWORD = config('TTN_WATER2_PASSWORD') 
PUBLIC_TLS_ADDRESS = config('TTN_PUBLIC_TLS_ADDRESS')
#
PUBLIC_TLS_ADDRESS_PORT = 8883
DEVICE_IDs = ["eui-70b3d57ba000154c"]
ALL_DEVICES = False


# Meaning Quality of Service (QoS)
# QoS = 0 - at most once
# The client publishes the message, and there is no acknowledgement by the broker.
QOS = 0
DEBUG = False


def get_value_from_json_object(obj, key):
    try:
        return obj[key]
    except KeyError:
        return "-"


def stop(client):
    client.disconnect()
    print("\nExit")
    sys.exit(0)


def save_to_influxdb(some_json):
    print(some_json)

    end_device_ids = some_json["end_device_ids"]
    device_id = end_device_ids["dev_eui"]
    # application_id = end_device_ids["application_ids"]["application_id"]
    received_at = some_json["received_at"]

    if "uplink_message" in some_json:
        uplink_message = some_json["uplink_message"]
        f_port = get_value_from_json_object(uplink_message, "f_port")

        # check if f_port is found
        if f_port != "-":
            f_cnt = get_value_from_json_object(uplink_message, "f_cnt")
            frm_payload = uplink_message["frm_payload"]

            decoded_payload = uplink_message["decoded_payload"]
            print(type(decoded_payload))

            latitude = uplink_message["rx_metadata"][0]["location"]["latitude"]
            longitude = uplink_message["rx_metadata"][0]["location"]["longitude"]
            altitude = uplink_message["rx_metadata"][0]["location"]["altitude"]
            # rssi = get_value_from_json_object(uplink_message["rx_metadata"][0], "rssi")
            # snr = get_value_from_json_object(uplink_message["rx_metadata"][0], "snr")
            # data_rate_index = get_value_from_json_object(uplink_message["settings"], "data_rate_index")
            # consumed_airtime = get_value_from_json_object(uplink_message, "consumed_airtime")

            # Daily log of uplinks
            now = datetime.now()

            print(decoded_payload)
            print(latitude, longitude, altitude)

            for measurement, value in decoded_payload.items():
                write_to_influx.write_influx_sensor_data(device_id, measurement, value, received_at)
                

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\nConnected successfully to MQTT broker")
    else:
        print("\nFailed to connect, return code = " + str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    print(
        "\nMessage received on topic '"
        + message.topic
        + "' with QoS = "
        + str(message.qos)
    )

    parsed_json = json.loads(message.payload)
    adaption_parsed_json = water_payload_adaptation.water_format_adaption(parsed_json)

    if DEBUG:
        print("Payload (Collapsed): " + str(message.payload))
        print("Payload (Expanded): \n" + json.dumps(parsed_json, indent=4))

    # save to file
    save_to_influxdb(adaption_parsed_json)


# mid = message ID
# It is an integer that is a unique message identifier assigned by the client.
# If you use QoS levels 1 or 2 then the client loop will use the mid to identify messages that have not been sent.
def on_subscribe(client, userdata, mid, granted_qos):
    print(
        "\nSubscribed with message id (mid) = "
        + str(mid)
        + " and QoS = "
        + str(granted_qos)
    )


def on_disconnect(client, userdata, rc):
    print("\nDisconnected with result code = " + str(rc))


def on_log(client, userdata, level, buf):
    print("\nLog: " + buf)
    logging_level = client.LOGGING_LEVEL[level]
    logging.log(logging_level, buf)


# Generate client ID with pub prefix randomly
client_id = f"python-mqtt-{random.randint(0, 1000)}"

print("Create new mqtt client instance")
mqttc = mqtt.Client(client_id)

print("Assign callback functions")
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
mqttc.on_disconnect = on_disconnect

# Setup authentication from settings above
mqttc.username_pw_set(USER, PASSWORD)

# IMPORTANT - this enables the encryption of messages
mqttc.tls_set()  # default certification authority of the system

# mqttc.tls_set(ca_certs="mqtt-ca.pem") # Use this if you get security errors
# It loads the TTI security certificate. Download it from their website from this page:
# https://www.thethingsnetwork.org/docs/applications/mqtt/api/index.html
# This is normally required if you are running the script on Windows

print(
    "Connecting to broker: " + PUBLIC_TLS_ADDRESS + ":" + str(PUBLIC_TLS_ADDRESS_PORT)
)
mqttc.connect(PUBLIC_TLS_ADDRESS, PUBLIC_TLS_ADDRESS_PORT, 60)


if ALL_DEVICES:
    print("Subscribe to all topics (#) with QoS = " + str(QOS))
    mqttc.subscribe("#", QOS)
elif len(DEVICE_IDs) != 0:
    topics = []
    for DEVICE_ID in DEVICE_IDs:
        topic = "v3/" + USER + "/devices/" + DEVICE_ID + "/up"
        print("Subscribe to topic " + topic + " with QoS = " + str(QOS))
        topics.append((topic, QOS))
    mqttc.subscribe(topics)
else:
    print("Can not subscribe to any topic")
    stop(mqttc)


print("And run forever")
try:
    run = True
    while run:
        mqttc.loop(10)  # seconds timeout / blocking time
        print(
            ".", end="", flush=True
        )  # feedback to the user that something is actually happening
except KeyboardInterrupt:
    stop(mqttc)
