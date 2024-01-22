'use strict';

var ttn = require('ttn');

var appEUI = 'dl-pr-26@ttn';
var accessKey = 'NNSXS.IF6ELACAVFLY3N24ZF6JUNNBPAS2TBSJEHWSOIA.JYOVWJAHIOOULUQZZIMUX6O3LXGPPB5SLZCP4L32UYUFX6HTUI5Q';

var client = new ttn.Client('nam1.cloud.thethings.network', appEUI, accessKey);

client.on('connect', function () {
	console.log('Connected to Water TTN');
});

client.on('error', function (err) {
	console.error('[ERROR]', err.message);
});


client.on('uplink', function (msg) {
	console.info('[INFO] ', 'Uplink: ' + JSON.stringify(msg, null, 2));
});

client.on('uplinkJonTTN', function (msg) {
	console.info('[INFO] ', 'Uplink: ' + JSON.stringify(msg, null, 2));
});
