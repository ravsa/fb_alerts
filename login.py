from simplecrypt import encrypt
import cPickle
import getpass
file=open('creds','w')
data=[encrypt('email',raw_input('email: ')),encrypt('password',getpass.getpass())]
cPickle.dump(data,file)
file.close()
