#!/usr/bin/python
###SERVER###
import random
import sys
from time import time
import gmpy
import hashlib
from flask import Flask
from flask import request

e=2**16+1 #e= 65537

app = Flask(__name__)

print (sys.argv)
IP = sys.argv[1]
port = sys.argv[2]
fileName = sys.argv[3]
localKey = sys.argv[4]

def hash_int(x):
    return int(hashlib.sha256(str(x)).hexdigest(),16)

#generates a random prime of the requested bit length
def gen_prime(BIT_LEN):
    print "gen_prime"
    found=False
    while found==False:
        p=random.randrange(2**(BIT_LEN-1),2**BIT_LEN)
        found=gmpy.is_prime(p)
    return p

#generates a random safe prime of the requested bit length
def gen_safe_prime(BIT_LEN):
    print "gen_safe_prime"
    found=False
    while found==False:
        q=random.randrange(2**(BIT_LEN-2),2**(BIT_LEN-1))
        p=2*q+1
        found=gmpy.is_prime(p) and gmpy.is_prime(q)
    return p


def RSA_GEN(BIT_LEN):
    print "RSA_GEN"
    # this is faster but not so secure
    p=gen_prime(BIT_LEN)
    q=gen_prime(BIT_LEN)

    # p=gen_safe_prime(BIT_LEN)
    # q=gen_safe_prime(BIT_LEN)

    n=p*q
    f=(p-1)*(q-1)
    e=2**16+1
    d=gmpy.invert(e,f)
    return d,n

def RSA_ENC(m,n):
    print "RSA_ENC"
    return pow(m,e,n)
def RSA_DEC(c,d,n):
    return pow(c,d,n)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    print "hello_word"
    if request.method == 'POST':
        vals = request.form['params']
        print "Client values received"
        #print vals[:100]
        #_=raw_input("vals receved from client")
        client_elements=vals.split(",")
        for i in range(len(client_elements)):
            client_elements[i]=int(client_elements[i])

        m_B1=[RSA_DEC(x,d,n) for x in client_elements]
        #print m_B1[0]
        #_=raw_input("client message decrit")
        
        hs=[hash_int(i) for i in server_elements]
        
        m_B2=[hash_int(RSA_DEC(y,d,n)) for y in hs]
        print "sending response..."

        client_enc=""
        for cc in m_B1:
            client_enc+=str(cc)+","
        client_enc=client_enc[:-1]
        srv_enc=""
        for cc in m_B2:
            srv_enc+=str(cc)+","
        srv_enc=srv_enc[:-1]
        resp= client_enc+"|"+srv_enc
        return str(resp)

if __name__ == '__main__':
    #generate RSA key pair (public,private) for the server
    d,n=RSA_GEN(512)
    print  n 

    print  d 
 
    # d chiave privata
    fout=open(localKey,"w")
    fout.write(str(n))
    fout.close()

    fin=open(fileName,"r")
    server_elements=[ row.split(";")[0] for row in fin]
    #srv_vals=fin.read()
    fin.close()
    #server_elements=srv_vals.split(",")


    for i in range(len(server_elements)):
        server_elements[i]=str(server_elements[i])
    #print server_elements[:10]
    #_=raw_input('server element top 10')
    app.run(host=IP, port=port)
