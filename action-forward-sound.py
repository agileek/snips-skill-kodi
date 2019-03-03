#!/usr/bin/env python3
import socket
import subprocess
import time
import configparser
from kodijson import Kodi
import paho.mqtt.client as mqtt

config = configparser.ConfigParser()
config.read("config.ini")

upnp_address = config["secret"]["upnp_address"]
mqtt_host = config["secret"]["mqtt_host"]
mqtt_port = config["secret"].getint("mqtt_port")
site_id = config["secret"]["site_id"]

SOUND_DEVICE_SETTINGS = " --input-slave=pulse://" + subprocess.getoutput("pacmd list-sources | grep name: | grep monitor | grep -oP '(?<=<).*(?=>)'")
SERVER_IP = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1],
                         [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
cast_cmd = "cvlc --qt-start-minimized screen:// :screen-fps=34 :screen-caching=80 --sout '#transcode{vcodec=mp4v,vb=4096,acodec=mpga,ab=128,sca=Auto,width=1024,height=768}:http{mux=ts,dst=:8089/" + socket.gethostname(
) + "}' --no-video --no-sout-video" + SOUND_DEVICE_SETTINGS
disable_local_audio_cmd = "pacmd set-sink-volume " + subprocess.getoutput("pacmd list-sink-inputs | grep sink | grep -oP '(?<=<).*(?=>)'") + " 100"
KODI_URL = upnp_address
kodi = Kodi(KODI_URL, "kodi", "")
current_cast = {}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(f"hermes/hotword/{site_id}/detected")
    # client.subscribe(f"hermes/audioServer/{site_id}/audioFrame")
    client.subscribe("hermes/dialogueManager/sessionEnded")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic)
    if msg.topic == "hermes/hotword/default/detected":
        kodi.GUI.ShowNotification(title=socket.gethostname(), message="Playing sound from snips")
        time.sleep(.500)
        kodi.Player.Open({"item": {"file": "http://" + SERVER_IP + ":8089/" + socket.gethostname() + "?action=play_video"}})
        print("forwarding sound")
        if "reference" not in current_cast:
            current_cast["reference"] = subprocess.Popen(cast_cmd, shell=True)
    if msg.topic == "hermes/dialogueManager/sessionEnded":
        print(f"stopping sound forward")
        print(f"stopping sound forward {current_cast}")
        if "reference" in current_cast:
            current_cast["reference"].terminate()
            del(current_cast["reference"])


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_host, mqtt_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

# subprocess.Popen(disable_local_audio_cmd, shell=True)

# print(kodi.Player.getItem({"properties": [ "title", "thumbnail", "file"], "playerid": 1}, id="VideoGetItem"))
