import time
import pychromecast
import json
from pychromecast.controllers.media import MediaStatus
from mqtthandler import MQTTHandler

class NewMediaStatus(MediaStatus):
    msg = {}
    mqtt = None
    prev_state = "None"
    prev_time = 0
    update_freq = None

    def __init__(self, mqtt, update_freq):
        MediaStatus.__init__(self)
        self.mqtt = mqtt
        self.update_freq = update_freq

    def generateMessage(self):
        msg = {
            "video": {
                "title": self.title,
                "series_title": self.series_title,
                "season": self.season,
                "episode": self.episode
            },
            "time": self.current_time,
            "total_time": self.duration,
            "playing": 0
        }

        if self.player_is_playing:
            msg["playing"] = 1

        return msg

    def update(self, data):
        MediaStatus.update(self, data)

        if self.title is None:
            return

        if self.prev_state == self.player_state and self.current_time < (self.prev_time + self.update_freq):
            return

        msg = self.generateMessage()
        self.prev_state = self.player_state
        self.prev_time = self.current_time
        self.msg = msg
        self.mqtt.send(msg)
        print("CHROMECAST: " + json.dumps(msg))


class ChromecastHandler:
    mc = None

    def __init__(self, cc_name, mqtt, update_freq):
        print("CHROMECAST: Connecting to Chromecast")
        self.getMediaController(cc_name, mqtt, update_freq)
        print("CHROMECAST: Connected!")

    def getMediaController(self, cc_name, mqtt, update_freq):
        chromecasts = pychromecast.get_chromecasts()
        [cc.device.friendly_name for cc in chromecasts]
        cast = next(cc for cc in chromecasts if cc.device.friendly_name == cc_name)

        # Start worker thread and wait for cast device to be ready
        cast.wait()
        self.mc = cast.media_controller
        self.mc.status = NewMediaStatus(mqtt, update_freq)
    
    def isDone(self):
        return self.mc.status.mqtt.isDone()