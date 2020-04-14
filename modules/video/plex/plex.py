import time
import copy
import json

from plexapi.myplex import MyPlexAccount
from mqtthandler import MQTTHandler

INIT_STATUS={
    "video": {
        "title": None,
        "series_title": None,
        "season": None,
        "episode": None
    },
    "time": None,
    "total_time": None,
    "playing": None
}


class PlexHandler:
    prev_statuses = []

    def __init__(self, plex_server_name, username, password, mqtt, update_freq):
        account = MyPlexAccount(username,password)
        print("PLEX: Connecting to server ", plex_server_name)
        self.plex = account.resource(plex_server_name).connect()  # returns a PlexServer instance       
        print("PLEX: Connected!")
        self.mqtt = mqtt
        self.update_freq = int(update_freq)

    def update(self):
        updated_status = False
        statuses = self.getStatuses()

        if len(statuses) == 0:
            return
        
        if len(self.prev_statuses) > 0:
            for status in statuses:
                for prev_status in self.prev_statuses:
                    same_video = status["video"]["title"] == prev_status["video"]["title"]
                    sync_time = status["time"] >= (prev_status["time"] + self.update_freq)
                    diff_state = status["playing"] != prev_status["playing"]

                    if not same_video:
                        continue

                    if sync_time or diff_state:
                        self.sendMessage(status)
                        updated_status = True
        else:
            for status in statuses:
                self.sendMessage(status)
            updated_status = True

        if updated_status:
            self.prev_statuses = copy.deepcopy(statuses)

    def getStatuses(self):
        global INIT_STATUS
        sessions = self.plex.sessions()
        #isPlayingMedia
        statuses=[]
        for media in sessions:
            status = INIT_STATUS
            status["video"]["title"] = media.title
            status["time"] = int(media.viewOffset / 1000)
            status["total_time"] = media.duration

            # 0 == paused, 1 == playing
            if media.players[0].state == 'playing':
                status["playing"] = 1
            else:
                status["playing"] = 0

            statuses.append(status)
        return statuses


    def sendMessage(self, msg): 
        self.mqtt.send(msg)
        message = json.dumps(msg)
        print("PLEX: " + message)
        return message

    def isDone(self):
        return True