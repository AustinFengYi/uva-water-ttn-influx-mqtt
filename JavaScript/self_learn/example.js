'use strict';

var ttn = require('ttn');

var appEUI = '';
var accessKey = '';

var client = new ttn.Client('nam1.cloud.thethings.network', appEUI, accessKey);

client.on('connect', function () {
	console.log('[DEBUG]', 'Connected');
});

client.on('error', function (err) {
	console.error('[ERROR]', err.message);
});

client.on('activation', function (e) {
	console.log('[INFO] ', 'Activated: ', e.devEUI);
});

client.on('uplink', function (msg) {
	console.info('[INFO] ', 'Uplink: ' + JSON.stringify(msg, null, 2));
});

client.on('uplinkJonTTN', function (msg) {
	console.info('[INFO] ', 'Uplink: ' + JSON.stringify(msg, null, 2));
});

client.on('uplink', function (msg) {

	// respond to every third message
	if (msg.counter % 3 === 0) {
		console.log('[DEBUG]', 'Downlink');

		var payload = new Buffer('4869', 'hex');
		client.downlink(msg.devEUI, payload);
	}
});