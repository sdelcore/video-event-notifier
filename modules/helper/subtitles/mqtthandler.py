import time
import paho.mqtt.client as paho
import json

class MQTTHandler():
    topic_prefix = "update"
    topic = None
    done = True
    done_command = ":done"

    def __init__(self, broker):

        try:
            self.client= paho.Client("subtitle-helper-client") 
            
            #bind callback
            self.client.on_message=self.on_message
            
            print("MQTT: connecting to broker ", broker)
            self.client.connect(broker)
            self.client.loop_start()
            self.done = False
            self.setTopic()

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
        if self.done:
            print("MQTT: Can't set topic since we're done")
            return None
        if self.topic == self.topic_prefix + topic:
            return            
        if self.topic is not None:
            print("MQTT: Unsub from previous topic")
            self.client.unsubscribe(self.topic)

        self.topic = self.topic_prefix + topic
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        if msg == self.done_command:
            self.close()
        return True

    def send(self, message):
        if self.done:
            print ("MQTT: won't send, since done")
            return None

        msg = json.dumps(message)
        self.client.publish(self.topic, msg)
        return True