import socket
import asyncio
import netifaces as ni
import coloredlogs


try:
    from sense_hat import SenseHat
    SENSEHAT = True
    sh = SenseHat()
except:
    SENSEHAT = False

import logging

# logging.basicConfig()
_log = logging.getLogger("showip")
_log.propagate = False
# _log.setLevel(logging.DEBUG)
coloredlogs.install(level='DEBUG',logger=_log)


STARTUP_MESSAGE = "SYSC3010 - LAB1"
interval_checkinterface = 1  # seconds

defaultmessages = dict(nointernet="No internet access")
colors = dict(red=[255, 0, 0],
              white=[255, 255, 255],
              green=[0, 255, 0],
              blue=[0, 0, 255],
              black=[0, 0, 0],
              gray=[10, 10, 10],
              yellow=[255, 255, 0])


class IPV4interface:
    def __init__(self, name, ip, netmask, broadcast):
        self._name = name
        self._ip = ip
        self._netmask = netmask
        self._broadcast = broadcast

    def __eq__(self, other):
        if ((self._name == other._name) and
                (self._ip == other._ip) and
                (self._netmask == other._netmask) and
                (self._broadcast == other._broadcast)):
            return True
        else:
            return False

    def show(self, show_ip=True, text_color=colors['blue'], back_color=colors['black'], onsensehat=True):
        message = f"{self._name}" + (f": {self._ip}{self.shortnetmask()}" if show_ip else "")
        if text_color == colors['yellow']:
            _log.warning(message)
        else:
            _log.debug(f"{message}, broadcast: {self._broadcast}")
        try:
            if SENSEHAT and onsensehat:
                sh.show_message(message,
                                text_colour=text_color,
                                back_colour=back_color)
        except Exception as e:
            _log.debug(e)

    def shortnetmask(self):
        netmask = [int(i) for i in self._netmask.split('.')]
        n = 0
        for i, netmaskbyte in enumerate(netmask):
            n = netmaskbyte << (3 - i) * 8 | n
        return f"/{bin(n).count('1')}"


class IPV4interfaces:
    def __init__(self):
        self._ipv4 = []
        self.getInterfaces()
        self.summary()

    def __contains__(self, item):
        for ipv4interface in self._ipv4:
            if ipv4interface._name == item._name:
                return True
        return False

    def interface_index(self, interfacename):
        for idx,ipv4interface in enumerate(self._ipv4):
            if ipv4interface._name == interfacename:
                return idx

    def getInterfaces(self):
        interfacenames = ni.interfaces()
        _log.debug(f"interfaces: {interfacenames}")
        for interfacename in interfacenames:
            interfacedata = ni.ifaddresses(interfacename)
            if 2 in interfacedata.keys():
                if all([key in interfacedata[2][0].keys() for key in ['addr','netmask','broadcast']] ):
                    newIPV4interface = IPV4interface(interfacename,
                                                     interfacedata[2][0]['addr'],
                                                     interfacedata[2][0]['netmask'],
                                                     interfacedata[2][0]['broadcast'])

                    if newIPV4interface in self._ipv4:
                        _log.debug(f"Interface: {newIPV4interface._name} already listed")
                    else:
                        self._ipv4.append(newIPV4interface)
        return self._ipv4
    
    def checkInterfaces(self):
        interfacenames = ni.interfaces()
        for interfacename in interfacenames:
            interfacedata = ni.ifaddresses(interfacename)
            if 2 in interfacedata.keys(): # it has a valid ipv4
                if all([key in interfacedata[2][0].keys() for key in ['addr', 'netmask']]):
                    newIPV4interface = IPV4interface(interfacename,
                                                     interfacedata[2][0]['addr'],
                                                     interfacedata[2][0]['netmask'],
                                                     interfacedata[2][0]['broadcast'] if 'broadcast' in interfacedata[2][0].keys() else None)
                    if newIPV4interface in self:
                        old_interface = self._ipv4[self.interface_index(newIPV4interface._name)]
                        if old_interface == newIPV4interface:
                            _log.debug(f"interface {old_interface._name} ({old_interface._ip}{old_interface.shortnetmask()}) remains unchanged")
                        else:
                            _log.warning(f"interface {old_interface._name} changed.")
                            self.update_interface(newIPV4interface)
                            newIPV4interface.show(text_color=colors['yellow'])
                    else:
                        _log.debug(f"Adding new interface")
                        newIPV4interface.show(text_color=colors['blue'])
                        self._ipv4.append(newIPV4interface)
            else: #not a valid ipv4
                for ipv4if in self._ipv4:
                    if ipv4if._name == interfacename:
                        _log.warning(f"Interface {ipv4if._name} does not have a valid ipv4. Removing it.")
                        ipv4if.show(text_color=colors['red'],show_ip=False)
                        self._ipv4.remove(ipv4if)


    def update_interface(self, interface):
        for i, oldinterface in enumerate(self._ipv4):
            if oldinterface._name == interface._name:
                self._ipv4[i]=interface
            
    def summary(self):
        for ipv4interface in self._ipv4:
            ipv4interface.show()


class ShowIP():
    def __init__(self):
        _log.debug("Initializing ShowIP class.")
        if SENSEHAT:
            sh.show_message(STARTUP_MESSAGE, text_colour=colors['red'])
        self._interfaces = IPV4interfaces()


    async def checkInterfaces(self):
        count = 0
        while True:
            _log.debug(count)
            # self.show_interfaces(onsensehat=False)
            count += 1
            self._interfaces.checkInterfaces()
            await asyncio.sleep(interval_checkinterface)

    async def listenForStick(self):
        count = 0
#         while True:
#             if SENSEHAT:
#                 if sh.stick.
#             _log.debug(count)
#             count += 1
#             self._interfaces.checkInterfaces()
#             await asyncio.sleep(4)

    def show_interfaces(self, text_color=colors['blue'], back_color=colors['black'],onsensehat=True):
        for interface in self._interfaces._ipv4:
            interface.show(text_color=text_color,
                           back_color=back_color,
                           onsensehat=onsensehat)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(loop.create_task(self.checkInterfaces()))


if __name__ == "__main__":
    showip = ShowIP()
    showip.run()
