from sysc3010utils import _log, sense
import sys
import socket
import json

_log.debug("Start listening.")

UDP_IP = ""
UDP_PORT = 6874

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    _log.debug(f"Message from {addr}: {data}")
    try:
        jdata = json.loads(data)
        sense.show_message(f"T: {jdata['temperature']:.2f}, H: {jdata['humidity']:.2f}")
    except ValueError:
        _log.warning("Invalid json format")
    except Exception as e:
        _log.error(e)
        sys.exit()
