from gi.repository import AppIndicator3 as ai
from gi.repository import Gtk as gtk
from gi.repository import Pango
from gi.repository import Notify 
import webbrowser as wb
from bs4 import BeautifulSoup
import os
import sys
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
notification_lab=list(range(100))
notification_ebox=list(range(100))
ind_notification,ind_request,ind_message=None,None,None
update_time = 10
failed,no_connection,creds, notification, message, request, online, browser, cookies, soup = True, True, None, None, None, None, None, None,None,None
tmp,extra,pextra,menya=None,None,None,None
count=0
signal.signal(signal.SIGINT,signal.SIG_DFL)
with open(os.path.expanduser('~/.fb_creds'), 'r') as file:
    creds = cPickle.load(file)


def init():
    global browser, cookies
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    cookies = mechanize.CookieJar()
    browser.addheaders = [
        ('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0')]
    Notify.init('idontknow')

    #ind_notification.set_menu(build_menu)
    #ind_request.set_menu(build_menu)
    #ind_message.set_menu(build_menu)


def create(): 
    global app_request,app_message,app_notification,ind_message,ind_request,ind_notification
    ind_notification=ai.Indicator.new(app_notification,os.path.abspath('./icons/notifications/no_notification.png'),ai.IndicatorCategory.SYSTEM_SERVICES)
    ind_request=ai.Indicator.new(app_request,os.path.abspath('./icons/requests/no_request.png'),ai.IndicatorCategory.SYSTEM_SERVICES)
    ind_message=ai.Indicator.new(app_message,os.path.abspath('./icons/messages/no_message.png'),ai.IndicatorCategory.SYSTEM_SERVICES)

    ind_notification.set_menu(notification_menu())
    ind_message.set_menu(message_menu())
    ind_request.set_menu(request_menu())
    ind_notification.set_status(ai.IndicatorStatus.ACTIVE)
    ind_message.set_status(ai.IndicatorStatus.ACTIVE)
    ind_request.set_status(ai.IndicatorStatus.ACTIVE)
def content():
    init()
    global browser, creds, notification, message, request, online, soup, no_connection, failed,ind_message,ind_request,ind_notification
    no_connection=True
    failed=True
    while True:
        try:
                #browser.open('https://m.facebook.com')
                #browser.select_form(nr=0)
                #browser.form['email'] = creds[0]
                #browser.form['pass'] = creds[1]
                #browser.submit()
                print "Hello,World!"
                while True:
                    try:
                        #browser.open('https://m.facebook.com')
                        #soup = BeautifulSoup(browser.response().read())
                        soup=BeautifulSoup(open('Facebook.html','r').read())
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
                                notification=0
                    for s in soup.find('a', href=re.compile(r'.*messages.*')):
                        try:
                            message = int(
                                re.search(r'\((.*?)\)', s.get_text()).group(1))
                        except:
                            try:
                                message = int(re.search(r'\((.*?)\)', s).group(1))
                            except:
                                message=0
                    for s in soup.find('a', href=re.compile(r'.*buddylist.*')):
                        try:
                            online = int(
                                re.search(r'\((.*?)\)', s.get_text()).group(1))
                        except:
                            try:
                                online = int(re.search(r'\((.*?)\)', s).group(1))
                            except:
                                online=0
                    for s in soup.find('a', href=re.compile(r'.*friends.*')):
                        try:
                            request = int(
                                re.search(r'\((.*?)\)', s.get_text()).group(1))
                        except:
                            try:
                                request = int(re.search(r'\((.*?)\)', s).group(1))
                            except:
                                request=0
                    notification_menu_data()
                    update()
                    time.sleep(update_time)
                    no_connection = True
                    failed = True
        except mechanize.URLError:
            if no_connection:
                Notify.Notification.new("<b>No_Connection</b>", 'connection error in FB_alert',
                                        os.path.abspath('./icons/error/no_connection.png')).show()
                no_connection = False
            time.sleep(6)
        except Exception,e:
            if failed:
                Notify.Notification.new("<b>_Authentication Failure</b>",str(e)+ 'Check your email and password',
                                            os.path.abspath('./icons/error/auth_fail.png')).show()
                failed = False
            time.sleep(6)
def notification_view(etc):
    wb.open_new_tab('https://www.facebook.com/notifications')
def notification_menu():
    global menya,extra,pextra
    men=gtk.Menu()
    extra=gtk.HBox()
    extra.show()
    pextra=gtk.Label()
    pextra.show()
    menya=gtk.MenuItem()
    menya.connect('activate',notification_view)
    extra.add(pextra)
    menya.add(extra)
    menya.show()
    men.append(menya)
    men.show()
    return men
def notification_menu_data():
    global soup,pextra,menya,tmp,notification
    temp=[]
    string=''
    count=0
    for i in soup.find_all('a',href=re.compile('.*notification.*')):
       temp.append(i.get_text()) 
    for i in temp[1:-1]:
        if i != '' and notification!= 0 :
            if count==0 and i != tmp and notification != None and notification !=0 :
                if i.find('like')!=-1:
                    status='<b>FB Like</b>'
                    Notify.Notification.new(status,i,os.path.abspath('./icons/like.png')).show()
                elif i.find('comment')!=-1:
                    status='<b>FB Comment</b>'
                    Notify.Notification.new(status,i,os.path.abspath('./icons/comment.png')).show()
                elif i.find('tag')!=-1:
                    status='<b>FB Tag</b>'
                    Notify.Notification.new(status,i,os.path.abspath('./icons/tag.png')).show()
                elif i.find('post')!=-1:
                    status='<b>FB Post</b>'
                    Notify.Notification.new(status,i,os.path.abspath('./icons/post.png')).show()
                else:
                    status='<b>FB Notification</b>'
                    Notify.Notification.new(status,i,os.path.abspath('./icons/facebook.png')).show()
                tmp=i
            string=string+'--->>>   '+i+'\n'
            count+=1
    pextra.set_text(string)
def message_menu():
    menu=gtk.Menu()
    none=gtk.MenuItem('see message')
    none.connect('activate',message_view)
    menu.append(none)
    menu.show_all()
    return menu
def message_view(etc):
    wb.open_new_tab('https://www.facebook.com/messages')
    
def request_menu():
    menu=gtk.Menu()
    none=gtk.MenuItem('see requests')
    none.connect('activate',request_view)
    menu.append(none)
    menu.show_all()
    return menu
def request_view(etc):
    wb.open_new_tab('https://www.facebook.com')

def update():
    global notification, message, request, online,ind_message,ind_request,ind_notification

    if notification != None and notification <= 99 and notification!=0 :
        ind_notification.set_icon(os.path.abspath('./icons/notifications/'+str(notification)+'.png'))
    elif  notification >= 99:
        ind_notification.set_icon(os.path.abspath('./icons/notifications/99+.png'))
    else:
        ind_notification.set_icon(os.path.abspath('./icons/notifications/no_notification.png'))

    if message != None and message <= 99 and message!= 0:
        ind_message.set_icon(os.path.abspath('./icons/messages/'+str(message)+'.png'))
    elif  message >= 99:
        ind_message.set_icon(os.path.abspath('./icons/messages/99+.png'))
    else:
        ind_message.set_icon(os.path.abspath('./icons/messages/no_message.png'))

    if request != None and request <= 99 and request !=0 :
        ind_request.set_icon(os.path.abspath('./icons/requests/'+str(request)+'.png'))
    elif  request >= 99:
        ind_request.set_icon(os.path.abspath('./icons/requests/99+.png'))
    else:
        ind_request.set_icon(os.path.abspath('./icons/requests/no_request.png'))

create()
thread.start_new_thread(gtk.main,())
content()
