#! /usr/bin/python
import urllib
import urllib2
import sys

from hashlib import md5
from base64 import b64decode
from base64 import b64encode



import pandas as pd
from Crypto.Cipher import AES




if len(sys.argv)!=7:
    print "IP,port,SymKey,fileName,intersection,user"
    sys.exit(0)

print (sys.argv)
IP = sys.argv[1]
port = sys.argv[2]
SymKey = sys.argv[3]
fileName = sys.argv[4]
intersection = sys.argv[5]
user=sys.argv[6]




#
# class AESCipher(object):
#
#     def __init__(self, key):
#         self.bs = 32
#         self.key = hashlib.sha256(key.encode()).digest()
#
#     def encrypt(self, raw):
#         raw = self._pad(raw)
#         iv = Random.new().read(AES.block_size)
#         cipher = AES.new(self.key, AES.MODE_ECB, iv)
#         return base64.b64encode(iv + cipher.encrypt(raw))
#
#     def decrypt(self, enc):
#         enc = base64.b64decode(enc)
#         iv = enc[:AES.block_size]
#         cipher = AES.new(self.key, AES.MODE_ECB, iv)
#         return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
#
#     def _pad(self, s):
#         return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
#
#     @staticmethod
#     def _unpad(s):
#         return s[:-ord(s[len(s)-1:])]
#



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





def mycrypt(s):
    return aes.encrypt(s)
    #return (aes.encrypt(aes._pad(s)))


def mydecrypt(s):
    return  aes.decrypt(s)
    #return (aes._unpad(aes.decrypt(s)))


def FromList2Mess(msglist,user,columns):
    columnlist=[]
    columnlist.append(user)
    columnlist.append(" ".join(columns))
    for rowlist  in msglist:
        row=" ".join(rowlist)
        columnlist.append(row)
    msg="  ".join(columnlist)
    return msg

# symmetric shared key
aes=AESCipher(SymKey)


# read local dataset
df = pd.read_csv(fileName,sep=";")

# read the intersetion set ID
df_i = pd.read_csv(intersection,sep=";")

# select just the intersecated rows
columns=df.columns.values.tolist()
DataIntersection = pd.merge(df, df_i, how='inner', left_on = 'IDKEY', right_on = 'IDKEY')[columns]


df= DataIntersection

dfcrypt=df.applymap(mycrypt)

msglist=dfcrypt.values.tolist()

def colCript(columns):
    colcript=[]
    for w in columns:
        colcript.append(mycrypt(w))
    return colcript


columnsCript=colCript(columns)
msg=FromList2Mess(msglist,user,columnsCript)

url = 'http://'+IP+':'+port


params = urllib.urlencode({'params': msg})

print ("invio")
#invio la stringa al server
response = urllib2.urlopen(url, params).read()

print response




