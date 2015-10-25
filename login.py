import gtk
import glib
import cPickle,os
spn=None
file=open('creds','w')
def login():
    global spn
    def active(x,etc):
        etc.modify_text(gtk.STATE_NORMAL,etc.get_colormap().alloc_color('black'))
    def done():
        elab.hide()
        plab.hide()
        ebox.hide()
        spn.start()
        spn.show()
        glib.timeout_add_seconds(4,lambda x:gtk.main_quit(),'')
    def process(x,y):
                data=[elab.get_text(),plab.get_text()]
                cPickle.dump(data,file)
                done()
    root=gtk.Window()
    root.set_default_size(300,300)
    root.connect('destroy',lambda x:gtk.main_quit())
    spn=gtk.Spinner()
    spn.set_size_request(30,30)
    vbox=gtk.VBox()
    image=gtk.Image()
    image2=gtk.Image()
    image2.set_size_request(120,120)
    image.set_from_file(os.path.abspath('./icons/login.png'))
    ebox=gtk.EventBox()
    ebox.add(image)
    ebox.connect('button-press-event',process)
    image2.set_from_file(os.path.abspath('./icons/user.png'))
    elab=gtk.Entry()
    elab.set_text('Email')
    elab.modify_text(gtk.STATE_NORMAL,elab.get_colormap().alloc_color('light grey'))
    elab.connect('changed',active,elab)
    plab=gtk.Entry()
    plab.set_text('PassWord')
    plab.set_visibility(False)
    plab.connect('changed',active,plab)
    plab.modify_text(gtk.STATE_NORMAL,plab.get_colormap().alloc_color('light grey'))
    vbox.pack_start(image2,False,False,7)
    vbox.pack_start(elab,False,False,7)
    vbox.pack_start(plab,False,False,7)
    vbox.pack_start(spn,False,False,2)
    vbox.pack_start(ebox,False,False,20)
    root.add(vbox)
    root.show_all()
    spn.hide()
    gtk.main()
login()
file.close()
