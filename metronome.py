#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys
import subprocess
import time
from threading import Thread
import os

path = os.path.dirname(os.path.realpath(__file__))

class MetroWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Yes!! ami metronome banaite parci")
        self.speed = 70
        self.run = False
        # maingrid
        maingrid = Gtk.Grid()
        maingrid.set_column_homogeneous(True)
        maingrid.set_row_homogeneous(False)
        maingrid.set_border_width(30)
        self.add(maingrid)
        # icon
        image = Gtk.Image(xalign=0)
        image.set_from_file(os.path.join(path, "icon.png"))
        maingrid.attach(image, 0, 0, 1, 1)
        # vertical slider,  initial value, min, max, step, page, psize
        self.v_scale = Gtk.Scale(
            orientation=Gtk.Orientation.VERTICAL,
            adjustment=Gtk.Adjustment.new(self.speed, 10, 240, 1, 0, 0)
            )
        self.v_scale.set_vexpand(True)
        self.v_scale.set_digits(0)
        self.v_scale.connect("value-changed", self.scale_moved)
        maingrid.attach(self.v_scale, 1, 0, 2, 1)

        self.togglebutton = Gtk.Button("_Run", use_underline=True)
        self.togglebutton.connect("clicked", self.time_out)
        self.togglebutton.set_size_request(70,20)
        maingrid.attach(self.togglebutton, 3, 3, 1, 1)

        # start the thread
        self.update = Thread(target=self.run_metro, args=[])
        self.update.setDaemon(True)
        self.update.start()

    def scale_moved(self, event):
        self.speed = int(self.v_scale.get_value())

    def time_out(self, *args):
        if self.run == True:
            self.run = False
            self.togglebutton.set_label("Run")
        else:
            self.run = True
            self.togglebutton.set_label("Pauze")

    def pauze(self):
        return 60/self.speed

    def run_metro(self):
        soundfile = "/usr/share/sounds/ubuntu/stereo/bell.ogg"
        while True:
            if self.run == True:
                subprocess.Popen([
                    "ogg123", soundfile
                    ])
            time.sleep(self.pauze())

def run_gui():
    window = MetroWindow()
    window.connect("delete-event", Gtk.main_quit)
    window.set_resizable(False)
    window.show_all()
    Gtk.main()

run_gui()
