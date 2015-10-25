from gi.repository import AppIndicator3 as ai
from gi.repository import Gtk as gtk
from gi.repository import Notify 
from bs4 import BeautifulSoup
import os
import signal
import thread
import json
import mechanize
import cPickle
import re
import time

app_notification='fb_notification'
app_message='fb_message'
app_request='fb_request'
ind_notification,ind_request,ind_message=None,None,None
update_time = 40
failed,no_connection,creds, notification, message, request, online, browser, cookies, soup = True, True, None, None, None, None, None, None,None,None
signal.signal(signal.SIGINT,signal.SIG_DFL)
with open(os.path.expanduser('~/.fb_creds'), 'r') as file:
    creds = cPickle.load(file)


def init():
    global app_request,app_message,app_notification,ind_message,ind_request,ind_notification,browser, cookies
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    cookies = mechanize.CookieJar()
    browser.addheaders = [
        ('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0')]
    
    ind_request=ai.Indicator.new(app_request,os.path.abspath('./icons/requests/no_request.png'),ai.IndicatorCategory.SYSTEM_SERVICES)
    ind_message=ai.Indicator.new(app_message,os.path.abspath('./icons/messages/no_message.png'),ai.IndicatorCategory.SYSTEM_SERVICES)
    ind_notification=ai.Indicator.new(app_notification,os.path.abspath('./icons/notifications/no_notification.png'),ai.IndicatorCategory.SYSTEM_SERVICES)

    ind_notification.set_menu(build_menu())
    ind_message.set_menu(build_menu())
    ind_request.set_menu(build_menu())

    ind_notification.set_status(ai.IndicatorStatus.ACTIVE)
    ind_message.set_status(ai.IndicatorStatus.ACTIVE)
    ind_request.set_status(ai.IndicatorStatus.ACTIVE)
    Notify.init(app_notification)
def content():
    init()
    global browser, creds, notification, message, request, online, soup, no_connection, failed,ind_message,ind_request,ind_notification
    while True:
        try:
                browser.open('https://m.facebook.com')
                browser.select_form(nr=0)
                browser.form['email'] = creds[0]
                browser.form['pass'] = creds[1]
                browser.submit()
                while True:
                    try:
                        browser.open('https://m.facebook.com')
                        soup = BeautifulSoup(browser.response().read())
                    except:
                        if failed:
                            Notify.Notification.new("<b>Authentication Failure</b>", 'Check your email and password', os.path.abspath('./icons/error/auth_fail.png')).show()
                            failed = False
                        time.sleep(update_time)
                    for s in soup.find('a', href=re.compile(r'.*notifications.*')):
                        try:
                            notification = int(
                                re.search(r'\((.*?)\)', s.get_text()).group(1))
                        except:
                            try:
                                notification = re.search(r'\((.*?)\)', s).group(1)
                            except:
                                pass
                    for s in soup.find('a', href=re.compile(r'.*messages.*')):
                        try:
                            message = int(
                                re.search(r'\((.*?)\)', s.get_text()).group(1))
                        except:
                            try:
                                message = int(re.search(r'\((.*?)\)', s).group(1))
                            except:
                                pass
                    for s in soup.find('a', href=re.compile(r'.*buddylist.*')):
                        try:
                            online = int(
                                re.search(r'\((.*?)\)', s.get_text()).group(1))
                        except:
                            try:
                                online = int(re.search(r'\((.*?)\)', s).group(1))
                            except:
                                pass
                    for s in soup.find('a', href=re.compile(r'.*friends.*')):
                        try:
                            request = int(
                                re.search(r'\((.*?)\)', s.get_text()).group(1))
                        except:
                            try:
                                request = int(re.search(r'\((.*?)\)', s).group(1))
                            except:
                                pass
                    time.sleep(update_time)
                    no_connection = True
                    failed = True
        except mechanize.URLError:
            if no_connection:
                Notify.Notification.new("<b>No_Connection</b>", 'connection error in FB_alert',
                                        os.path.abspath('./icons/error/no_connection.png')).show()
                no_connection = False
            time.sleep(6)
        except:
            if failed:
                Notify.Notification.new("<b>Authentication Failure</b>", 'Check your email and password',
                                            os.path.abspath('./icons/error/auth_fail.png')).show()
                failed = False
            time.sleep(6)

def build_menu():
    menu=gtk.Menu()
    exit=gtk.MenuItem('exit')
    exit.connect('activate',lambda x:gtk.main_quit())
    menu.append(exit)
    menu.show_all()
    return menu
thread.start_new_thread(content,())
gtk.main()
