from sysc3010utils import _log, sense, get_key
import socket
import json
import time

UDP_IP = "192.168.0.1"
UDP_PORT = 6874

_log.debug("UDP target IP: %s" % UDP_IP)
_log.debug("UDP target port: %s" % UDP_PORT)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
while True:
    data = dict(temperature=sense.get_temperature(),
               humidity=sense.get_humidity())
    MESSAGE = json.dumps(data).encode()
    sense.show_message(f"T: {data['temperature']:.1f}, H: {data['humidity']:.1f}")
    _log.debug(f"Sending message to {UDP_IP}:{UDP_PORT}: {MESSAGE}")
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(5)