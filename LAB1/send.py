from sysc3010utils import _log, sense


import socket
import json
import time

UDP_IP = "192.168.0.56"
UDP_PORT = 6874

_log.debug("UDP target IP: %s" % UDP_IP)
_log.debug("UDP target port: %s" % UDP_PORT)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
while True:
    MESSAGE = json.dumps(
        dict(temperature=sense.get_temperature(),
             humidity=sense.get_humidity()) ).encode()
    _log.debug("Sending message: %s" % MESSAGE)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(5)