import logging
import random
_log = logging.getLogger('sysc3010')

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



