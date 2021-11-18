import logging
import random
import uuid
import sys

if "send" in sys.argv[0]:
    __logname = "sendLog.log"
elif "listen" in sys.argv[0]:
    __logname = "listenLog.log"
else:
    __logname = "lastLog.log"
_log = logging.getLogger('sysc3010')
__fh = logging.FileHandler(__logname,'w')
__fh.setLevel(logging.DEBUG)
__formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
__fh.setFormatter(__formatter)
_log.addHandler(__fh)
try:
    import coloredlogs
    _log.propagate = False
    coloredlogs.install(level='DEBUG',logger=_log)
except Exception as e:
    _log.setLevel(logging.DEBUG)


try:
    from sense_hat import SenseHat
    __SENSEHAT = True
    sense = SenseHat()
except Exception as e:
    __SENSEHAT = False

    class SenseHat:
        def __init__(self):
            self._humidity = 70
            self._temperature = 22
            self.__increasingh = True
            self.__increasingt = True

        def get_humidity(self):
            if self.__increasingh:
                self._humidity = self._humidity + random.random()
                if self._humidity > 90: self.__increasingh = False
            else:
                self._humidity = self._humidity - random.random()
                if self._humidity < 10: self.__increasingh = True
            return self._humidity

        def get_temperature(self):
            if self.__increasingt:
                self._temperature = self._temperature + random.random()
                if self._temperature > 40: self.__increasingt = False
            else:
                self._temperature = self._temperature - random.random()
                if self._temperature < -30: self.__increasingt = True
            return self._temperature

        def show_message(self,message, **kwargs):
            _log.info(message)
    sense = SenseHat()

colors = dict(red=[255, 0, 0],
              white=[255, 255, 255],
              green=[0, 255, 0],
              blue=[0, 0, 255],
              black=[0, 0, 0],
              gray=[10, 10, 10],
              yellow=[255, 255, 0])

def get_key():
    correct_key = 'SYSC3010'
    wrong_key = str(uuid.uuid4())
    if random.random() > .7:
        return wrong_key
    else:
        return correct_key

