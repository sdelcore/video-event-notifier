import time
import srt
import re
import datetime
from mqtthandler import MQTTHandler

INIT_STATUS={
    "video": {
        "title": None,
        "series_title": None,
        "season": None,
        "episode": None
    },
    "time": None,
    "events": None
}


class SubtitleHandler:
    subtitles = []
    phrases = []
    def __init__(self, broker):     
        self.mqtt = MQTTHandler(broker)

    def parseSRT(self, srt_filename):
        f=open(srt_filename, "r")
        subtitle_generate = srt.parse(f.read())
        f.close()

        self.subtitles = list(subtitle_generate)
        return self.subtitles
    
    def parsePhrases(self, phrase_filename):
        f=open(phrase_filename, "r")
        lines = f.readlines()
        for line in lines:
            phrase = line.rstrip("\n\r").split("/")
            self.phrases.append(phrase)

        return self.phrases

    def isPhraseInLine(self,phrase, sub, content):
        sub_line = re.sub('[^A-Za-z0-9\s]+', '', str(content)).lower()
        phrase = re.sub('[^A-Za-z0-9\s]+', '', str(phrase)).lower()
        count = 0
        while bool(re.search(phrase, sub_line)):
            count += 1
            sub_line = sub_line.replace(phrase, '', 1)
        return count

    def getEventTime(self,sub):
        middle = sub.end - sub.start
        between_sec = datetime.timedelta.total_seconds(middle) / 2
        sec = between_sec + datetime.timedelta.total_seconds(sub.start)
        return int(sec)

    def matchEventToMovie(self, movie, subtitles, phrases, time_offset):
        global INIT_STATUS          
        status = INIT_STATUS
        status["video"]["title"] = movie    

        #TODO determine how to set up phrase data
        for sub in subtitles:
            c = sub.content.replace('\n', ' ')
            c = c.split(" ")
            firstpart, secondpart = " ".join(c[:len(c)//2]), " ".join(c[len(c)//2:])
            mult = 0

            for phrase in phrases:
                line = phrase[0]
                events = phrase[1]
                mult += self.isPhraseInLine(line,sub,sub.content)
                #f = self.isPhraseInLine(line,sub, firstpart)
                #s =  self.isPhraseInLine(line,sub, secondpart)
                #if f + s == 0:
                #    mult += self.isPhraseInLine(line,sub,sub.content )
                #else: 
                #    mult += f+s

            ## DEAR LESS DRUNK SELF
            # this currently adds the number of events over the entire subtitle
            # what you need to do if you wish to accept it, is to split each subtitle into to two parts
            # the first part will the the half that has the first bit of text, which will have the correct time to event for the work
            # the second half will have the correct time to event gfor the second half
            # you could have three if statements that check and each toher them reach a send.message()

            if mult > 0: # wotn work properly if events is greater than 1
                status["time"] = self.getEventTime(sub) + time_offset
                status["events"] = int(events) * mult
                self.sendMessage(status)
                #print(sub.content)

    def sendMessage(self, msg):        
        self.mqtt.send(msg)
        print(msg)
        return msg

    def isDone(self):
        return True