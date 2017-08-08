#!/usr/bin/env python
# coding:utf-8

import sys
import json
import urllib
import time
import datetime
import paho.mqtt.client as mqtt
from HTMLParser import HTMLParser

MQTT_HOST = "MQTT-SERVER"
MQTT_PORT = 1883

class SensorTagParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.sensor = ""
        self.sensors = {}
        self.sensors['time'] = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            attrs = dict(attrs)
            if 'id' in attrs:
                self.sensor = attrs['id']

    def handle_data(self, data):
        if self.sensor:
            sensordata = data.split(' ')
            if self.sensor == 'tmp':
                self.sensors['tmp'] = sensordata[2] 
                self.sensors['irtmp'] = sensordata[3] 
            elif self.sensor == 'opt':
                self.sensors[self.sensor] = sensordata[1] 
            elif self.sensor == 'bar':
                self.sensors[self.sensor] = sensordata[3] 
            elif self.sensor == 'key':
                self.sensors[self.sensor] = sensordata[0] 
            elif self.sensor == 'hum':
                self.sensors[self.sensor] = sensordata[3] 
            elif self.sensor == 'syn':
                self.sensors[self.sensor] = sensordata[0] 
            elif self.sensor == 'gyr':
                self.sensors['gyr_x'] = sensordata[3] 
                self.sensors['gyr_y'] = sensordata[4] 
                self.sensors['gyr_z'] = sensordata[5] 
            elif self.sensor == 'mag':
                self.sensors['mag_x'] = sensordata[3] 
                self.sensors['mag_y'] = sensordata[4] 
                self.sensors['mag_z'] = sensordata[5] 
            elif self.sensor == 'acc':
                self.sensors['acc_x'] = sensordata[3] 
                self.sensors['acc_y'] = sensordata[4] 
                self.sensors['acc_z'] = sensordata[5] 
            self.sensor = ""


if __name__ == "__main__":
    args = sys.argv
    url = "http://" + args[1] + "/param_sensortag_poll.html"
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.connect(MQTT_HOST, port=MQTT_PORT)

    while True:
        try :
            result = urllib.urlopen( url ).read()
            parser = SensorTagParser()
            parser.feed(result)
            client.publish('sensortag/', json.dumps(parser.sensors))
        except ValueError :
            print "fail"
        time.sleep(1)
