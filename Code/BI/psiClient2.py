#! /usr/bin/python
from StringIO import StringIO
import random
from time import time
import gmpy
import hashlib
import urllib
import urllib2
import json
import sys
#import pandas as pd
e=2**16+1 #e= 65537

print (sys.argv)
if len(sys.argv)==6:
    IP = sys.argv[1]
    port = sys.argv[2]
    fileName = sys.argv[3]
    remoteKey = sys.argv[4]
    intersection = sys.argv[5]

headerID='IDKEY'




def hash_int(x):
    return int(hashlib.sha256(str(x)).hexdigest(),16)

#read server's public key
#passaggio della chiave pubblica tra client e server
fin=open(remoteKey)
n=fin.read()
n=int(n.strip())
print "n server key",n
#a=raw_input('wait')

fin.close()
url = 'http://'+IP+':'+port

#read elements
fin=open(fileName,"r")

client_elements=[ row.split(";")[0] for row in fin]
client_elements.pop(0)




#vals=fin.read().strip()
fin.close()

#client_elements=vals.split(",")

#print client_elements[:10]
#print len(client_elements)
#a=raw_input('wait')
client_elements_clear=[]
client_elements_clear[:]=client_elements[:]

#sys.exit(0)
#client_elements lista degli elementi del DB client 

for i in range(len(client_elements)):
	client_elements[i]=str(client_elements[i])
# trasformo in stringa ma originariamente era in intero
hc=[hash_int(i) for i in client_elements]

#print hc[:10]
#print len(hc)
#a=raw_input('hc wait')
m_A=[]
rs=[]

for i in hc:
    
	r=random.randrange(n) #numero intero a caso nel range della server Pkey
	rs.append(r)
	obf=(pow(r, e,n)*i)%n
	m_A.append(str(obf))
#print rs[:10]
#_=raw_input('rs (r random) wait')
#print m_A[:10]
#_=raw_input('m_A (message cripted) wait')
# ho creato due liste, 
# rs una di numeri casuali
# m_A l'altra e' funzione dei rispettivi 
# numeri casuali,degli hash(elementi) del client
# e dei parametri crittografici e,n
vals=",".join(m_A)

#vals e' la concatenazione degli hash(elementi) crittati
print "Sending records to server"
print "il server sta elaborando"

params = urllib.urlencode({'params': vals})

#invio la stringa al server
response = urllib2.urlopen(url, params).read()

print "##############"
print "response"
print "##############"
print "Received records from server!"
response=response.strip()
response=response.split("|")
print "response"
print "##############"

client_elements=response[0].split(",")
print "client_elements: ",len(client_elements)
for i in range(len(client_elements)):
    client_elements[i]=int(client_elements[i])
#for i in range(10):
    #print client_elements[i]
#_=raw_input('response client elements  wait')

serv_elements=response[1].split(",")
print "serv_elements: ",len(serv_elements)
for i in range(len(serv_elements)):
    serv_elements[i]=int(serv_elements[i])
#for i in range(10):
    #print serv_elements[i]
#_=raw_input('response server elements  wait')

mymap={}
for i in range(len(client_elements)):
     k=client_elements[i]=hash_int((client_elements[i]*gmpy.invert(rs[i],n))%n)
     mymap[k]=i
client_elements[:10]     
#_=raw_input('transf. client elements linkabili con serv_elements wait')
     
#now let's count the common elements
cnt=0
intersectionFile=open(intersection,'w')
intersectionFile.write(headerID+"\n")
for i in client_elements:
    if i in serv_elements:
        #print mymap[i]
        print client_elements_clear[ mymap[i]]
        intersectionFile.write(client_elements_clear[ mymap[i]]+"\n")
        cnt+=1
print "common elements:", cnt
