from gi.repository import Notify
from bs4 import BeautifulSoup
import mechanize
import cPickle
import os
import time
update_time = 10
creds, notification, message, request, online, browser, cookies, soup = None, None, None, None, None, None, None, None
with open(os.path.abspath('creds'), 'r') as file:
    creds = cPickle.load(file)


def init():
    global browser, cookies
    Notify.init('idontknow')
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    cookies = mechanize.CookieJar()
    browser.addheaders = [
        ('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0')]


def content():
    global browser, creds, notifications, messages, request, online, soup
    init()
    while True:
        try:
            browser.open('https://m.facebook.com')
            browser.select_form(nr=0)
            browser.form['email'] = creds[0]
            browser.form['pass'] = creds[1]
            res = browser.submit()
            while True:
                browser.open('https://m.facebook.com')
                soup = BeautifulSoup(browser.response().read())
                
        except mechanize.URLError, e:
            Notify.uninit()
            Notify.Notification.new("<b>Disconnect</b>", 'connection error',
                                    os.path.abspath('./icons/messages/1.png')).show()
            Notify.uninit()
            break
        except Exception, e:
            Notify.Notification.new("<b>Authentication Failure</b>", 'Check your email and password',
                                    os.path.abspath('./icons/messages/1.png')).show()
            Notify.uninit()
            break
content()
