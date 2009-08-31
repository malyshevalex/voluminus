import sys

try:
    import alsaaudio
except:
    print "alsaaudio python module required"
    sys.exit(1)

try:
    import gtk
except:
    print "PyGTK module required"
    exit(1)

DBUS_AVAILABLE = 1
try:
    from dbuscontrol import DBusObject
except:
    DBUS_AVAILABLE = 0
    print "Running without D-Bus module"

NOTIFICATIONS_AVAILABLE = 1
#try:
from notification import NotificationControl
#except:
 #   NOTIFICATIONS_AVAILABLE = 0
  #  print "Runnig without notifications"

from statusicon import StatusIcon
from scalewindow import ScaleWindow

class Voluminus:
    def __init__(self, mixerControl_, volumeStep_):
        self.mixerControl = mixerControl_
        self.volumeStep = volumeStep_
        self.mixer = alsaaudio.Mixer(self.mixerControl)
        self.getVolume()
        self.statusIcon = StatusIcon(self)
        self.scaleWindowShown = False
        self.scaleWindow = ScaleWindow(self)
        if (NOTIFICATIONS_AVAILABLE):
            self.notifications = NotificationControl()
        self.updateGUI()
        if (DBUS_AVAILABLE):
            self.dbusObject = DBusObject(self)

    def getVolume(self):
        self.muted = self.mixer.getmute()[0];
        self.volume = self.mixer.getvolume()[0];

    def setVolume(self, volume, showNotify=False):
        self.volume = volume
        if (self.volume > 100):
            self.volume = 100
        elif (self.volume < 0):
            self.volume = 0
        self.mixer.setvolume(self.volume)
        self.updateGUI(showNotify)
        return self.volume

    def toggleMute(self, showNotify=False):
        return self.setMute(not self.muted, showNotify)

    def setMute(self, muted, showNotify=False):
        self.muted = muted
        self.mixer.setmute(self.muted)
        self.updateGUI(showNotify)
        return self.muted

    def raiseVolume(self, showNotify=False):
        return self.setVolume(self.volume + self.volumeStep, showNotify)

    def lowerVolume(self, showNotify=False):
        return self.setVolume(self.volume - self.volumeStep, showNotify)

    def updateGUI(self, showNotify=False):
        if (self.scaleWindowShown):
            self.scaleWindow.update()
        self.statusIcon.update()
        if ((NOTIFICATIONS_AVAILABLE) and (showNotify)):
            self.notifications.showNotify(self.volume, self.muted)

    def toggleScaleWindow(self):
        if (self.scaleWindowShown):
            self.scaleWindow.hide()
        else:
            self.getVolume()
            self.scaleWindow.show()
        self.scaleWindowShown = not self.scaleWindowShown

    def showAbout(self):
        builder = gtk.Builder()
        builder.add_from_file(sys.path[0] + '/aboutdialog.ui')
        aboutDlg = builder.get_object('aboutDialog')
        aboutDlg.connect('response', lambda w, e: aboutDlg.destroy())
        aboutDlg.show_all()

    def quit(self):
        sys.exit(0)

if __name__ == "__main__":
    voluminus = Voluminus("Master", 3)
    gtk.main()
