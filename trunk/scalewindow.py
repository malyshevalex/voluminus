
import sys
import gtk

class ScaleWindow:
    def __init__(self, mixer):
        self.mixer = mixer
        builder = gtk.Builder()
        builder.add_from_file(sys.path[0] + '/scalewindow.ui')
        self.window = builder.get_object('scaleWindow')
        self.scale = builder.get_object('scale')
        self.scale.connect('value_changed', self.on_scale_value_changed)
        self.muteBtn = builder.get_object('mute')
        self.muteBtn.connect('toggled', self.on_mute_toggled)

    def update(self):
        self.scale.set_value(self.mixer.volume)
        self.muteBtn.set_active(self.mixer.muted)

    def show(self):
        self.moveToIcon(self.mixer.statusIcon.icon);
        self.window.show()
        self.update()

    def hide(self):
        self.window.hide()

    def moveToIcon(self, icon):
        (screen, rect, orientation) = icon.get_geometry()
        (windowWidth, windowHeight) = self.window.get_size()
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        (x, y) = (0, 0)
        if (orientation == gtk.ORIENTATION_HORIZONTAL):
            x = rect.x + int((rect.width - windowWidth) / 2)
            if (x < 0):
                x = 0
            elif (x + windowWidth > screenWidth):
                x = screenWidth - windowWidth
            y = rect.y + rect.height
            if (y + windowHeight > screenHeight):
                y = rect.y - windowHeight
        else:
            x = rect.x + rect.height
            if (x + windowWidth > screenWidth):
                x = rect.x - windowWidth
            y = rect.y + int((rect.height - windowHeight) / 2)
            if (y < 0):
                y = 0
            elif (y + windowHeight > screenHeight):
                y = screenHeight - windowHeight
        self.window.move(x, y)

    def on_scale_value_changed(self, widget):
        self.mixer.setVolume(int(widget.get_value()))

    def on_mute_toggled(self, widget):
        self.mixer.setMute(widget.get_active())
