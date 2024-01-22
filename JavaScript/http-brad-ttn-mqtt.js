'use strict';

/*
 The program is writen in JavaScript followed by Brad's http-ttn-mqtt.js implementation!!
  https://github.com/lab11/gateway/blob/master/software/http-ttn-mqtt/http-ttn-mqtt.js
*/

var ttn = require('ttn');
var appEUI = 'uva-engineers-way-sensors@ttn';
var accessKey = 'NNSXS.CADCG4QOLUCBGSJHD6THIZ5WNQWI74GFHIWOFII.2KIBPZS5JGDK3YCIDJTTVSZLKYI2WFDEPTIPJQJCHWQV52FO7QNA';

var client = new ttn.Client('nam1.cloud.thethings.network', appEUI, accessKey);
client.on('connect', function () {
	console.log('Connected to Brad TTN');

	client.on('uplinkBradTTN', function (message) {
		var payload = message.payload
		var out = {};

		// We definitely want the extracted data if it exists.
		if ('uplink_message' in payload) {
			if ('decoded_payload' in payload.uplink_message) {
				out = payload.uplink_message.decoded_payload;
			}
		}

		Object.keys(out).forEach(function (key) {
			if (out[key] === null) {
				delete out[key];
			}
		});

		// Other fields to plot as data
		out.counter = payload.uplink_message.f_cnt;
		out.confirmed = payload.uplink_message.confirmed;
		out.lorawan_frequency = payload.uplink_message.settings.frequency;
		out.lorawan_bandwidth = payload.uplink_message.settings.data_rate.lora.bandwidth;
		out.lorawan_spreading_factor = payload.uplink_message.settings.data_rate.lora.spreading_factor;
		out.lorawan_airtime = payload.uplink_message.consumed_airtime;
		out.lorawan_coding_rate = payload.uplink_message.settings.coding_rate;
		out.number_receiving_gateways = payload.uplink_message.rx_metadata.length;

		// Find the best RSSI gateway
		var best_rssi = -1000;
		var best_rssi_index = 0;
		for (var i = 0; i < payload.uplink_message.rx_metadata.length; i++) {
			if (payload.uplink_message.rx_metadata[i].rssi > best_rssi) {
				best_rssi_index = i;
			}
		}

		// Extract gateway parameters
		out.rssi = payload.uplink_message.rx_metadata[best_rssi_index].rssi;
		out.snr = payload.uplink_message.rx_metadata[best_rssi_index].snr;

		// Rest is metadata
		out._meta = {
			received_time: payload.uplink_message.received_at,
			device_id: payload.end_device_ids.dev_eui,
			receiver: 'http-ttn-mqtt'
		}
		out._meta.gateway_id = payload.uplink_message.rx_metadata[best_rssi_index].gateway_ids.gateway_id;
		out._meta.ttn_application_id = payload.end_device_ids.application_ids.application_id;

		// Make special measurement for mapping purposes.
		if ('payload' in out && 'geohash' in out.payload && 'rssi' in out) {
			out.rssimap = { rssi: out.rssi, geohash: out.payload.geohash };
		}

		console.info('[INFO] ', 'Uplink: ' + JSON.stringify(out, null, 2));
		// console.log(JSON.stringify(out))

	});


});

client.on('error', function (err) {
	console.error('[ERROR]', err.message);
});

client.on('uplink', function (msg) {
	console.info('[INFO] ', 'Uplink: ' + JSON.stringify(msg, null, 2));
});

/*
client.on('uplinkBradTTN', function (msg) {
	console.info('[INFO] ', 'Uplink: ' + JSON.stringify(msg, null, 2));
});
*/

