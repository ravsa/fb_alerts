#!/usr/bin/python
from gi.repository import Gtk as gtk
from gi.repository import GLib as glib
from gi.repository import Gdk as gdk
import cPickle
import os
spn = None
root = None
image, image2, vbox, ebox, plab, elab = None, None, None, None, None, None
xx, yy, kk = 0, 0, 0
store1 = 0
file = open(os.path.expanduser('~/.fb_creds'), 'w')


def login():
    global spn, root, image, image2, vbox, ebox, plab, elab

    def animation():
        global xx, yy, kk
        yy = gdk.Screen().width() / 2 - 150

        def temp1():
            global xx, yy, ad
            xx += .4
            root.move(yy, xx)
            if xx >= gdk.Screen().height() / 2 - 150:
                glib.timeout_add(1.8, temp3)
                return False
            return True

        def temp3():
            global store1
            store1 += .4
            root.set_size_request(store1, 0)
            if store1 >= 300:
                glib.timeout_add(1.8, temp2)
                return False
            return True

        def temp2():
            global kk, image2, image, ebox, vbox, plab, elab, store1
            kk += .4
            root.set_size_request(store1, kk)
            if kk >= 20:
                image.show()
            if kk >= 140:
                plab.show()
            if kk >= 170:
                elab.show()
            if kk >= 210:
                image2.show()
            if kk >= 300:
                root.show_all()
                return False
            return True
        glib.timeout_add(1.8, temp1)

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
    root.set_title('Login (OffLine)')
    root.move(xx, yy)
    root.set_size_request(30, 0)
    root.connect('destroy', lambda x: gtk.main_quit())
    spn = gtk.Spinner()
    spn.set_size_request(30, 30)
    vbox = gtk.VBox()
    image = gtk.Image()
    image2 = gtk.Image()
    image2.set_size_request(120, 120)
    image.set_from_file(os.path.expanduser('~/.fb_alerts/icons/login.png'))
    ebox = gtk.EventBox()
    ebox.add(image)
    ebox.connect('button-press-event', process)
    image2.set_from_file(os.path.expanduser('~/.fb_alerts/icons/user.png'))
    elab = gtk.Entry(text="Email")
    plab = gtk.Entry(text="PassWord")
    plab.set_visibility(False)
    vbox.pack_start(image2, False, False, 7)
    vbox.pack_start(elab, False, False, 7)
    vbox.pack_start(plab, False, False, 7)
    vbox.pack_start(spn, False, False, 2)
    vbox.pack_start(ebox, False, False, 20)
    root.add(vbox)
    vbox.show()
    root.show()
    spn.hide()
    animation()
    gtk.main()
login()
file.close()
