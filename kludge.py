#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3Packages.requests -p xdotool
import requests, json
import subprocess

def transition(source, old, new):
    # vim kludge
    if source == "sensor-rechts":
        if old is None:
            return
        if old == 0  and new > 0.1:
            print("[vim] Insert")
            subprocess.run("xdotool key 'i'", shell=True)
        elif old > 0  and new == 0:
            print("[vim] Exit")
            subprocess.run("xdotool key 'Escape'", shell=True)
    if source == "sensor-midden":
        if old is None:
            return
        pass
        # TODO
    # push to talk 
    if source == "sensor-links":
        if old is None:
            return
        if old == 0  and new > 0.1:
            print("[mic] Unmuting")
            subproces.run("pacmd suspend-source alsa_input.usb-Blue_Microphones_Yeti_Stereo_Microphone_REV8-00.analog-stereo 0", shell=True)
        elif old > 0  and new == 0:
            print("[mic] Muting")
            subproces.run("pacmd suspend-source alsa_input.usb-Blue_Microphones_Yeti_Stereo_Microphone_REV8-00.analog-stereo 1", shell=True)

url = "http://192.168.100.109/events"
headers = {"Accept": "text/event-stream"}
r = requests.get(url, headers=headers, stream=True)

cmd = None
raw_data = None
states = {}

for line in r.iter_lines():
    line = line.decode("utf8")
    if line == '':
        continue

    last_cmd = cmd
    last_raw_data = raw_data
    cmd, raw_data = line.split(":",1)
    raw_data = raw_data.strip()
    if last_cmd == "event" and last_raw_data == "state" and cmd == "data":
        message = json.loads(raw_data)
        source = message["id"]
        state = message["value"]
        old_state = states.get(message["id"], None)
        if old_state != state:
            transition(source, old_state, state)
        states[source] = state
