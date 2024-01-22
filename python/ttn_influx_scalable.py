""" Connect to MQTT Server and receive uplink messages using the Paho MQTT Python client library
"""
#
import sys, logging, json, random, time, os
import paho.mqtt.client as mqtt
from datetime import datetime
from decouple import config
from service import write_to_influx
# // Read in the config file to get the parameters.
# // Login to The Things Stack Community Edition console to get the
#   1.USER 2.PASSWORD 3.PUBLIC_TLS_ADDRESS 4.PUBLIC_TLS_ADDRESS_PORT
"""
USER = "dl-pr-26@ttn"
PASSWORD = "NNSXS.IF6ELACAVFLY3N24ZF6JUNNBPAS2TBSJEHWSOIA.JYOVWJAHIOOULUQZZIMUX6O3LXGPPB5SLZCP4L32UYUFX6HTUI5Q"
"""
PUBLIC_TLS_ADDRESS = config("TTN_PUBLIC_TLS_ADDRESS")
#
PUBLIC_TLS_ADDRESS_PORT = 8883
"""
DEVICE_IDs = ["eui-70b3d57ba000154e","eui-70b3d57ba0001551","eui-70b3d57ba0001550"]
"""
ALL_DEVICES = False


# Meaning Quality of Service (QoS), QoS = 0 - at most once
# The client publishes the message, and there is no acknowledgement by the broker.
QOS = 0
DEBUG = True


Normal_connections=3

def on_log(client, userdata, level, buf):
    print("\nLog: " + buf)
    logging_level = client.LOGGING_LEVEL[level]
    logging.log(logging_level, buf)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    print(
        "\nMessage received on topic '"
        + message.topic
        + "' with QoS = "
        + str(message.qos)
    )

    parsed_json = json.loads(message.payload)

    if DEBUG:
        print("Payload: \n" + json.dumps(parsed_json, indent=2))

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\nConnected successfully to MQTT broker")
    else:
        print("\nFailed to connect, return code = " + str(rc))
        client.loop_stop()  

def on_disconnect(client, userdata, rc):
    print("\nDisconnected with result code = " + str(rc))

def stop(client):
    client.disconnect()
    print("\nExit")
    sys.exit(0)

def on_subscribe(client, userdata, mid, granted_qos):
    print(
        "Subscribed with message id (mid) = "
        + str(mid)
        + " and QoS = "
        + str(granted_qos)
    )

# Write uplink to tab file
def save_to_file(message_topic, some_json):
    if 'uplink_message' in some_json:
        path_n_file = message_topic + ".txt"
        print(path_n_file)
        if not os.path.isfile(path_n_file):
            with open(path_n_file,  'a', encoding='utf-8') as f:
                json.dump(some_json,f ,ensure_ascii=False, indent=4)

        with open(path_n_file,  'a', encoding='utf-8') as f:
            json.dump(some_json,f ,ensure_ascii=False, indent=4)


def Create_connections(nclients):
       for i in range(nclients):
            # Generate client ID with pub prefix randomly
            client_id = f"python-mqtt-{random.randint(0, 1000)}"
            print("Create new mqtt client instance")
            mqttc = mqtt.Client(client_id) #create new instance

            # Setup authentication from settings above
            if i == 0:
                USER = "dl-pr-26@ttn"
                mqttc.username_pw_set(USER, "NNSXS.IF6ELACAVFLY3N24ZF6JUNNBPAS2TBSJEHWSOIA.JYOVWJAHIOOULUQZZIMUX6O3LXGPPB5SLZCP4L32UYUFX6HTUI5Q")
                DEVICE_IDs = ["eui-70b3d57ba000154e","eui-70b3d57ba0001551"]
            if i == 1:
                USER = "dl-mbx@ttn"
                mqttc.username_pw_set(USER, "NNSXS.IVSEC7Q4QUSYHRV55EOCFUXLFNAOJNR5I4KLI6Y.BW2E35PKPXU3MHUKR67WMG4XRN6DHTX4KPRTM6QEQRKPDOSWIYDQ")
                DEVICE_IDs = ["eui-70b3d57ba000154c"]
            if i ==2:
                USER = "uva-engineers-way-sensors@ttn"
                mqttc.username_pw_set(USER, "NNSXS.CADCG4QOLUCBGSJHD6THIZ5WNQWI74GFHIWOFII.2KIBPZS5JGDK3YCIDJTTVSZLKYI2WFDEPTIPJQJCHWQV52FO7QNA")
                DEVICE_IDs = ["eui-24e124136d324618"]
            # default certification authority of the system
            mqttc.tls_set()  

            print("Assign callback functions")
            mqttc.on_connect = on_connect           #establish connection
            mqttc.on_subscribe = on_subscribe
            mqttc.on_message = on_message
            mqttc.on_disconnect = on_disconnect

            print(
                "Connecting to broker: " + PUBLIC_TLS_ADDRESS + ":" + str(PUBLIC_TLS_ADDRESS_PORT)
            )
            mqttc.connect(PUBLIC_TLS_ADDRESS, PUBLIC_TLS_ADDRESS_PORT, 60)
            
            clients.append(mqttc)

 
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

            
            mqttc.loop_start()
            
            # while not mqttc.connected_flag:
            #     time.sleep(0.05)



"""THE PROGRAM STARTS HERE!!"""
clients=[]
# print("current threads =",no_threads)
print("Creating Normal Connections ",Normal_connections," clients")
Create_connections(Normal_connections)

print("All clients connected, and run forever ")
try:
    run = True
    while run:
        time.sleep(5) # seconds timeout / blocking time
        print(
            ".", end="", flush=True
        )  # feedback to the user that something is actually happening
except KeyboardInterrupt:
   time.sleep(5)

#client.loop_stop() #stop loop
for client in clients:
   client.disconnect()
   client.loop_stop()
#allow time for allthreads to stop before existing
time.sleep(10)








