/*
import json

def water_format_adaption(parsed_json):
    # Convert TTN water sensor data to Link Lab TTN-influx format
    """ Step 1: Extract decoded_payload from water sensor payload """
    message_payload = parsed_json
    # print(json.dumps(message_payload, indent = 4 sort_keys=True))
    water_decoded_payload = message_payload["uplink_message"].pop('decoded_payload')
    # print(json.dumps(water_decoded_payload, indent = 2, sort_keys=True))

    """Step 2: Convert water sensor decoded_payload to Link Lab TTN-influx decoded_payload format"""
    decoded_payload = {}
    mapping = { 
        ## unit -> 'water': 'linklab_influx' ##
        'temperature': 'Temperature_°C',
        'battery_voltage': 'voltage_v',
        'pressure': 'pressure_hPa', # hPa value = bar value x 1000      
    }

    # remove 'device_id' & 'protocol_version' here because it is only used for cloud.thethings.network
    if 'device_id' in water_decoded_payload:
        water_decoded_payload.pop('device_id')
    if 'protocol_version' in water_decoded_payload:
        water_decoded_payload.pop('protocol_version')

    for measurement, nested in water_decoded_payload.items():
        decoded_payload[mapping[measurement]] = nested["value"]
        if measurement == "pressure":
            decoded_payload[mapping[measurement]] = nested["value"] * 1000
    # print(decoded_payload)

    """Step 3: Ingestion of decoded_payload into message_payload"""
    message_payload["uplink_message"]["decoded_payload"]  = decoded_payload
    # print(json.dumps(message_payload, indent = 4, sort_keys=True))

    """Step 4: return parsed json of water JSON after format adaption"""
    parsed_json = message_payload

    return parsed_json
*/

function get_awair_ip_addresses() {

};