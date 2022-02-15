from flask import Flask
from datetime import datetime
import re
import subprocess
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

@app.route("/api/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

@app.route("/api/btrfs_stats/<name>")
def btrfs_stats(name):
    now = datetime.now()
    formatted_now = now.strftime("%d/%m/%Y %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z\_]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = 'none'

    # Read BTRFS STATS command output
    if clean_name == 'cache':
        device_path = '/mnt/cache'
    elif clean_name == 'vm_pool':
        device_path = '/mnt/vm_pool'
    else:
        return "Invalid name"

    process = subprocess.Popen(['btrfs', 'device', 'stats', device_path], 
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    content = []
    v_dev_old = ''
    j_dev = {}
    for output in process.stdout.readlines():
        if output.strip():
            raw_str = output.strip()
            match_parts = re.split('[. ]', raw_str)
            v_dev = ''
            v_att = ''
            v_val = ''
            if match_parts:
                for index, item in enumerate(match_parts):
                    if item:
                        if index == 0:
                            v_dev = match_parts[index].replace('[', '').replace(']', '')
                        elif index == 1:
                            v_att = match_parts[index]
                        else:
                            v_val = match_parts[index]
            if not v_dev_old or v_dev_old != v_dev:
                if v_dev_old:
                    content.append({v_dev_old: j_dev})
                j_dev = {}
                v_dev_old = v_dev
            j_dev[v_att] = v_val

    content.append({v_dev_old: j_dev})
    content.append({"update_time": formatted_now})

    return json.dumps(content, indent=4)