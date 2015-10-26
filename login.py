#!/usr/bin/python
from gi.repository import Gtk as gtk
from gi.repository import GLib as glib
from gi.repository import Gdk as gdk
import cPickle
import os
spn = None
root = None
xx, yy = 0, 0
file = open(os.path.expanduser('~/.fb_creds'), 'w')


def login():
    global spn, root

    def animation():
        def temp():
            global xx, yy
            xx += 1
            yy += 1 + ((float(gdk.Screen().width()) -
                        float(gdk.Screen().height())) / float(gdk.Screen().height()))
            root.move(yy, xx)
            if xx == gdk.Screen().height() / 2 - 150:
                return False
            return True
        glib.timeout_add(5, temp)

    def done():
        elab.hide()
        plab.hide()
        ebox.hide()
        spn.start()
        spn.show()
        glib.timeout_add_seconds(4, lambda x: gtk.main_quit(), '')

    def process(x, y):
        data = [elab.get_text(), plab.get_text()]
        cPickle.dump(data, file)
        done()
    root = gtk.Window()
    root.move(xx, yy)
    animation()
    root.set_default_size(300, 300)
    root.connect('destroy', lambda x: gtk.main_quit())
    spn = gtk.Spinner()
    spn.set_size_request(30, 30)
    vbox = gtk.VBox()
    image = gtk.Image()
    image2 = gtk.Image()
    image2.set_size_request(120, 120)
    image.set_from_file(os.path.abspath('./icons/login.png'))
    ebox = gtk.EventBox()
    ebox.add(image)
    ebox.connect('button-press-event', process)
    image2.set_from_file(os.path.abspath('./icons/user.png'))
    elab = gtk.Entry(text="Email")
    plab = gtk.Entry(text="PassWord")
    plab.set_visibility(False)
    vbox.pack_start(image2, False, False, 7)
    vbox.pack_start(elab, False, False, 7)
    vbox.pack_start(plab, False, False, 7)
    vbox.pack_start(spn, False, False, 2)
    vbox.pack_start(ebox, False, False, 20)
    root.add(vbox)
    root.show_all()
    spn.hide()
    gtk.main()
login()
file.close()
