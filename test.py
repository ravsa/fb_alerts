from bs4 import BeautifulSoup as bp
import re
soup=bp(open('Facebook.html','r').read())
x=[]
str=''
for i in soup.find_all('a',href=re.compile('.*notification.*')):
    x.append(i.get_text())
for i in x[1:-1]:
    if i == '':
        str+='\n_______________\n'
    str+=i
print str
