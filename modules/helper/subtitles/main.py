import time
import copy
from subtitles import SubtitleHandler

"""
SRT_FILENAME="files/srt/Spiderverse.srt"
PHRASES_FILENAME="files/events/spiderverse-v1.event"
MOVIE="Spider-Man: Into the Spider-Verse"
TIME_OFFSET=-2
"""


SRT_FILENAME="files/srt/Digimon the Movie.srt"
PHRASES_FILENAME="files/events/digimon-v1.event"
MOVIE="Digimon: The Movie"
TIME_OFFSET=0

MQTT_BROKER=""

##movei starts at 88 sec


if __name__ == "__main__":
    sub_handler = SubtitleHandler(MQTT_BROKER)
    subtitles = sub_handler.parseSRT(SRT_FILENAME)
    phrases = sub_handler.parsePhrases(PHRASES_FILENAME)
    sub_handler.matchEventToMovie(MOVIE, subtitles, phrases, TIME_OFFSET)
            
