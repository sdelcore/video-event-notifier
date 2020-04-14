import time
import yaml

from plex import PlexHandler
from mqtthandler import MQTTHandler

CONFIG="../../config.yml"

PLEX_SERVER="media-server"
PLEX_USERNAME=""
PLEX_PASSWORD=""

#issue with plexapi is that the current_time of the video is only updated every 10 seconds
#so if the time isnt updated and we arent paused we need to emulate the status message
# copy prev message and update the current time

if __name__ == "__main__":
    # Parse configuration
    config = None
    with open(CONFIG, 'r') as f:
        config = yaml.load(f)

    plex_config = config['PleX']
    PLEX_SERVER = plex_config["server"]
    PLEX_USERNAME = plex_config["username"]
    PLEX_PASSWORD = plex_config["password"]
    UPDATE_FREQ = plex_config["update frequency"]
    
    mqtt_config = config["MQTT"]
    MQTT_BROKER = mqtt_config["url"]
    TOPIC = mqtt_config["Topics"]["now playing"]

    # Set up communications
    mqtt = MQTTHandler("plex-client", MQTT_BROKER, TOPIC)
    plex_server = PlexHandler(PLEX_SERVER, PLEX_USERNAME, PLEX_PASSWORD, mqtt, UPDATE_FREQ)

    # PLEX SPECIFIC CYCLE CODE
    # Ensures .update() gets ran every second
    t = time.time()
    time_to_wait = 1

    while True:
        if time.time() - t < time_to_wait:
            time_to_wait = 1
            continue
        
        plex_server.update()
        t = time.time()
        