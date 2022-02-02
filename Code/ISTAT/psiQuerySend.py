#! /usr/bin/python
import urllib
import urllib2
import sys
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES

if len(sys.argv)!=6:
    print "IP ,port,queryString,ClientName,SymKey "

    sys.exit(0)

print ("QUERY MODE")
IP = sys.argv[1]
port = sys.argv[2]
queryString=sys.argv[3]
ClientName = sys.argv[4]
SymKey = sys.argv[5]
url = 'http://'+IP+':'+port

# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]



class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        self.key = md5(key.encode('utf8')).hexdigest()

    def encrypt(self, raw):
        raw = pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc)).decode('utf8')

aes=AESCipher(SymKey)

def mycrypt(s):
    return aes.encrypt(s)
    #return (aes.encrypt(aes._pad(s)))

def mydecrypt(s):
    return  aes.decrypt(s)


def DecListStr(ListString):

    #print ListString
    l=[]
    for fieldName in ListString.split(" "):
        #print "@@@@@@@@@@@@@@@@@@@@"
        #print fieldName
        #print mydecrypt(fieldName)
        #print "@@@@@@@@@@@@@@@@@@@@"
        l.append(mydecrypt(fieldName))

    return " ; ".join(l)


#print queryString



def mycryptQueryStr(queryString):
    l=[]
    for field in queryString.split(','):
        l.append(mycrypt(field))
    return " ".join(l)



columnlist=[]
columnlist.append("QUERY")
columnlist.append(ClientName)
columnlist.append(mycryptQueryStr(queryString))

msg="  ".join(columnlist)

#print "-----------------"
#print msg
#print "-------------------"

params = urllib.urlencode({'params': msg})

#invio la stringa al server
response = urllib2.urlopen(url, params).read()
print "--- resp: ----"
#print response

rowlist=response.split("  ")
#print rowlist[1]

print DecListStr(rowlist[1])
for fieldlist in rowlist[2:]:
    r=fieldlist.split(" ")
    a=[]
    for field_i in range(len(r)):

        if (field_i==len(r)-1):
            a.append( r[field_i])
        else:
            a.append( mydecrypt(r[field_i]))
    print " ; ".join(a)
sys.exit(0)
