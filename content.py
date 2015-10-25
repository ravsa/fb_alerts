from gi.repository import Notify
from bs4 import BeautifulSoup
import mechanize
import cPickle
import re
from simplecrypt import decrypt
import os,sys
import time
update_time = 10
retry_time = 1
creds, notification, message, request, online, browser, cookies, soup = None, None, None, None, None, None, None, None
with open(os.path.abspath('creds'), 'r') as file:
    creds = cPickle.load(file)
creds=[decrypt('email',creds[0]),decrypt('password',creds[1])]
def init():
    global browser, cookies
    Notify.init('idontknow')
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    cookies = mechanize.CookieJar()
    browser.addheaders = [
        ('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0')]


def content():
    global browser, creds, notification, message, request, online, soup
    init()
    while True:
        time.sleep(retry_time)
        try:
            browser.open('https://m.facebook.com')
            browser.select_form(nr=0)
            browser.form['email'] = creds[0]
            browser.form['pass'] = creds[1]
            res = browser.submit()
            while True:
                time.sleep(update_time)
                try:
                    browser.open('https://m.facebook.com')
                    soup = BeautifulSoup(browser.response().read())
                except:
                    Notify.Notification.new(
                        "<b>Authentication Failure</b>", 'Check your email and password', os.path.abspath('./icons/messages/1.png')).show()
                    print "Error 321"
                    continue
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
                lis=[notification, request, message, online]
                print lis
                sys.exit()
        except mechanize.URLError, e:
            Notify.uninit()
            Notify.Notification.new("<b>Disconnect</b>", 'connection error',
                                    os.path.abspath('./icons/messages/1.png')).show()
            break
        except Exception, e:
            print e
            print "Error 123"
            Notify.Notification.new("<b>Authentication Failure</b>", 'Check your email and password',
                                    os.path.abspath('./icons/messages/1.png')).show()
            break
content()
