import yaml

from chromecast import ChromecastHandler
from mqtthandler import MQTTHandler

CONFIG="../../config.yml"

if __name__ == "__main__":
    # Parse configuration
    config = None
    with open(CONFIG, 'r') as f:
        config = yaml.load(f)
    
    cc_config = config["Chromecast"]
    mqtt_config = config["MQTT"]
    cc_name = cc_config["name"]

    
    MQTT_BROKER = mqtt_config["url"]
    topic = mqtt_config["Topics"]["now playing"]
    update_freq = int(cc_config["update frequency"])

    mqtt = MQTTHandler("chromecast-client", MQTT_BROKER, topic)
    cc = ChromecastHandler(cc_name, mqtt, update_freq)

    while True:
        pass
