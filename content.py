from gi.repository import Notify
from bs4 import BeautifulSoup
import mechanize
import cPickle
import re
import os
import time
update_time = 40
creds, notification, message, request, online, browser, cookies, soup = None, None, None, None, None, None, None, None
no_connection = True
failed = True
with open(os.path.expanduser('~/.fb_creds'), 'r') as file:
    creds = cPickle.load(file)


def init():
    global browser, cookies
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    cookies = mechanize.CookieJar()
    browser.addheaders = [
        ('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0')]


def content():
    global browser, creds, notification, message, request, online, soup, no_connection, failed
    init()
    Notify.init('idontknow')
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
                        Notify.Notification.new("<b>Authentication Failure</b>", 'Check your email and password',
                                                os.path.abspath('./icons/error/auth_fail.png')).show()
                        failed = False
                    time.sleep(update_time)
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
                time.sleep(update_time)
                no_connection = True
                failed = True
        except mechanize.URLError:
            if no_connection:
                Notify.Notification.new("<b>No_Connection</b>", 'connection error in FB_alert',
                                        os.path.abspath('./icons/error/no_connection.png')).show()
                no_connection = False
            time.sleep(60)
        except:
            if failed:
                Notify.Notification.new("<b>Authentication Failure</b>", 'Check your email and password',
                                        os.path.abspath('./icons/error/auth_fail.png')).show()
                failed = False
            time.sleep(60)
