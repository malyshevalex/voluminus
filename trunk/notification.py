
import sys
import pynotify

class NotificationControl:
    def __init__(self):
        pynotify.init('Voluminus')
        self.__info = pynotify.get_server_info()
        self.__initCapabilities()

    def __initCapabilities(self):
        self.caps = {};
        caps = pynotify.get_server_caps()
        for cap in caps:
            self.caps[cap] = True

    def showNotify(self, volume, muted):
        icon = ''
        if ((volume == 0) or (muted)):
            icon = 'notification-audio-volume-muted'
        elif (volume <= 33):
            icon = 'notification-audio-volume-low'
        elif (volume <= 66):
            icon = 'notification-audio-volume-medium'
        else:
            icon = 'notification-audio-volume-high'

        if ((not self.caps['private-synchronous']) and (not self.caps['x-canonical-private-synchronous']) and (self.__n)):
            self.__n.hide()

        string = 'is now at ' + str(volume) + '%'
        if (muted):
            string = 'is now muted'
        if ((self.caps['x-canonical-private-icon-only']) or (self.caps['private-icon-only'])):
            string = ''

        self.__n = pynotify.Notification('Volume', string, icon)
        self.__n.set_hint_int32('value', volume)
        if (self.caps['x-canonical-private-synchronous']):
            self.__n.set_hint_string('x-canonical-private-synchronous', '')
        elif (self.caps['private-synchronous']):
            self.__n.set_hint_string('private-synchronous', '')
        self.__n.show()
