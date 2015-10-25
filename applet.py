from gi.repository import AppIndicator3 as ai
from gi.repository import Gtk as gtk
from gi.repository import Notify as notify
from bs4 import BeautifulSoup
import os
import signal
import thread
import json
from content import init,request,message,notification,online,soup,content
signal.signal(signal.SIGINT,signal.SIG_DFL)
app_notification='fb_notification'
app_message='fb_message'
app_request='fb_request'
ind_notification,ind_request,ind_message=None,None,None

def main():
    global app_request,app_message,app_notification,ind_message,ind_request,ind_notification
    init()
    while True:
        thread.start_new_thread(content,())
        ind_request=ai.Indicator.new(app_request,os.path.abspath('./icons/requests/no_request.png'),ai.IndicatorCategory.SYSTEM_SERVICES)
        ind_message=ai.Indicator.new(app_message,os.path.abspath('./icons/messages/no_message.png'),ai.IndicatorCategory.SYSTEM_SERVICES)
        ind_notification=ai.Indicator.new(app_notification,os.path.abspath('./icons/notifications/no_notification.png'),ai.IndicatorCategory.SYSTEM_SERVICES)
    
    #   if data[1] != None and data[1] <= 99:
    #        indicator.set_icon(os.path.abspath('./notifications/'+str(data[1])+'.png'))
    #    elif  data[1] >= 99:
    #        indicator.set_icon(os.path.abspath('./notifications/99+.png'))
        ind_notification.set_menu(build_menu())
        ind_message.set_menu(build_menu())
        ind_request.set_menu(build_menu())
        ind_notification.set_status(ai.IndicatorStatus.ACTIVE)
        ind_message.set_status(ai.IndicatorStatus.ACTIVE)
        ind_request.set_status(ai.IndicatorStatus.ACTIVE)
def build_menu():
    menu=gtk.Menu()
    exit=gtk.MenuItem('exit')
    exit.connect('activate',lambda x:gtk.main_quit())
    menu.append(exit)
    menu.show_all()
    return menu
thread.start_new_thread(main,())
gtk.main()
