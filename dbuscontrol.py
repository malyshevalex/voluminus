
import dbus, dbus.service

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)



class DBusObject(dbus.service.Object):
    def __init__(self, mixer):
        self.mixer = mixer
        dbus.service.Object.__init__(self, dbus.service.BusName('com.voluminus.dbus', dbus.SessionBus()), '/com/voluminus/dbus')

    @dbus.service.method(dbus_interface='com.voluminus.dbus',
                         in_signature='', out_signature='n')
    def raiseVolume(self):
        return self.mixer.raiseVolume(True)

    @dbus.service.method(dbus_interface='com.voluminus.dbus',
                         in_signature='', out_signature='n')
    def lowerVolume(self):
        return self.mixer.lowerVolume(True)

    @dbus.service.method(dbus_interface='com.voluminus.dbus',
                         in_signature='n', out_signature='n')
    def setVolume(self, volume):
        return self.mixer.setVolume(volume, True)

    @dbus.service.method(dbus_interface='com.voluminus.dbus',
                         in_signature='', out_signature='b')
    def toggleMute(self):
        return self.mixer.toggleMute(True)
