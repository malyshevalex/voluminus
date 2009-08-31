import sys
import gtk

class StatusIcon:
    def __init__(self, mixer):
        self.mixer = mixer
        self.icon = gtk.StatusIcon()
        self.icon.connect('activate', self.on_activate)
        self.icon.connect('popup-menu', self.on_right_click)
        self.icon.connect('scroll-event', self.on_scroll)
        self.constructMenu()

    def constructMenu(self):
        separator = gtk.SeparatorMenuItem()
        self.menu = gtk.Menu()
        muteItem = gtk.CheckMenuItem('Mute');
        muteItem.set_active(self.mixer.muted);
        muteItem.connect('toggled', self.on_mute_toggled)
        self.menu.add(muteItem)
        self.menu.add(separator)
        aboutItem = gtk.ImageMenuItem('gtk-about')
        aboutItem.connect('activate', self.on_about)
        self.menu.add(aboutItem);
        quitItem = gtk.ImageMenuItem('gtk-quit')
        quitItem.connect('activate', self.on_quit)
        self.menu.add(quitItem)
        self.menu.show_all()

    def update(self):
        self.icon.set_tooltip(self.mixer.mixerControl + ": " + str(self.mixer.volume) + "%")
        if ((self.mixer.volume == 0) or (self.mixer.muted)):
            self.icon.set_from_icon_name('audio-volume-muted')
        elif (self.mixer.volume <= 33):
            self.icon.set_from_icon_name('audio-volume-low')
        elif (self.mixer.volume <= 66):
            self.icon.set_from_icon_name('audio-volume-medium')
        else:
            self.icon.set_from_icon_name('audio-volume-high')

    def on_activate(self, widget):
        self.mixer.toggleScaleWindow()

    def on_right_click(self, widget, button, time):
        self.menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.icon)

    def on_scroll(self, wigdet, event):
        if (event.direction == gtk.gdk.SCROLL_UP):
            self.mixer.raiseVolume()
        elif (event.direction == gtk.gdk.SCROLL_DOWN):
            self.mixer.lowerVolume()

    def on_mute_toggled(self, widget):
        self.mixer.toggleMute()

    def on_about(self, widget):
        self.mixer.showAbout()

    def on_quit(self, widget):
        self.mixer.quit()
