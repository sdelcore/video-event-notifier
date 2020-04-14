import time
import paho.mqtt.client as paho
import json

class MQTTHandler():
    topic = ""
    client_name = ""
    done = True

    def __init__(self, client_name, broker, topic):
        try:
            print("MQTT: connecting to broker ", broker)
            self.client=paho.Client(client_name)
            self.client_name = client_name
            self.client.connect(broker)
            self.client.loop_start()
            self.done = False
            self.setTopic(topic)

        except Exception as e:
            print("MQTT: Init failed")
            print (e)
            return None

    def close(self):
        self.done = True
        time.sleep(5)
        self.client.disconnect()
        self.client.loop_stop()
    
    def isDone(self):
        return self.done

    def setTopic(self, topic=''):
        self.topic = topic
        self.client.subscribe(topic)

    def send(self, message):
        if self.done:
            print ("MQTT-" + self.client_name + ": won't send, since done")
            return None
            
        msg = json.dumps(message)
        self.client.publish(self.topic, msg)
        return True