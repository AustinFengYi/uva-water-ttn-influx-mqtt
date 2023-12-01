from decouple import config
from influxdb import InfluxDBClient

class Influx():
    def __init__(self):
        self.user = config('INFLUXDB_USERNAME')
        self.password = config('INFLUXDB_PASSWORD')
        self.host = config('INFLUX_HOST')
        self.dbname = 'linklab-users'  # 'linklab-users'
        self.port = 443
        self.ssl = True
        self.client = self.get_client()

    def get_client(self, dbname='linklab-users'):
        client = InfluxDBClient(host=self.host, port=self.port, username=self.user,
                                password=self.password, database=self.dbname, ssl=self.ssl)
#         print('Retrieving client for: %s' % dbname)
        self.client = client
        return client
    
    def write_data_append_field(self,device_id, measurement, value, received_at):
        return write_influx_sensor_data(device_id, measurement, value, received_at)

def write_influx_sensor_data(device_id, measurement, value, received_at):
    x = Influx()
    value = float(value)
    client = x.get_client()

    # influx ver-1.8
    # Can consider appending more meta-data information here
    client.write_points(
        [
            {
                "measurement": measurement,
                "tags": {
                    # "location_general":
                    # "location_specific":
                    "device_id": device_id,
                },
                "fields": {
                    "value": value,
                },
                "time": received_at,
            }
        ]
    )