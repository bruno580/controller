from flask import Flask, jsonify, request, make_response
import whitelist
import os,subprocess

app = Flask(__name__)

def _get_metadata():
    # Test if os-release file exists to ensure we are on linux
    # if this is a Windows machine it won't get metadata and return an empty json.
    if os.path.isfile("/etc/os-release"):
        osname   = subprocess.getoutput("source /etc/os-release && echo ${PRETTY_NAME}")
        hostname = subprocess.getoutput("hostname -f")
        kernel   = subprocess.getoutput("uname -r")
        uptime   = subprocess.getoutput("uptime")
        metadata = [
            {
                "hostname": hostname, 
                "kernel": kernel, 
                "os-release": osname,
                "uptime" : uptime
            }    
        ]
        return metadata
    else:
        not_linux="Not a linux server."
        return jsonify(418, not_linux)

@app.get("/metadata")
def get_metadata():
    return jsonify(_get_metadata())

def _run_command(command):
    try:
        output = subprocess.getoutput(command)
    except Exception as error:
        output = error
    return output

@app.post("/command")
def run_command():
    command = request.args.get('command')
    if command in whitelist.commands.keys():
        response = make_response(_run_command(whitelist.commands[command]))
        return response
    else:
        return jsonify(401, "This command is not whitelisted.")
