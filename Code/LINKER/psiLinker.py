
import pandas as pd
from flask import Flask
from flask import request
import sys


print (sys.argv)
IP = sys.argv[1]
port = sys.argv[2]


app = Flask(__name__)


def Stream2List(text):
    data=[]
    for row in  text.split("  ")[:4]:
        data.append(row.split(" "))
    return data


def mkdf(nomeFile_df):
    LinkerFile=open(nomeFile_df,'r')
    text=LinkerFile.readline()
    LinkerFile.close()

    d=[]
    for row in  text.split("  "):
        d.append(row.split(" "))

    column=d[1]
    print "column",column
    print d[2]

    df=pd.DataFrame(d[2:],columns=column)
    return df,column[0]


def FromList2Mess(msglist,user,columns):
    columnlist=[]
    columnlist.append(user)
    columnlist.append(" ".join(columns))
    for rowlist  in msglist:
        s=[]
        for ss in rowlist:
            ss=str(ss)
            s.append(ss)
        row=" ".join(s)
        columnlist.append(row)
    msg="  ".join(columnlist)
    return msg






@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        vals = request.form['params']
        print "Client values received"
        print vals

        data=Stream2List(vals)

        #print "--------------"
        #print data[0]
        #print data[1]
        #print data[2]
        #print "--------------"



        msgType= data[0][0]

        if (data[0][0]=='BI'):
            LinkerBancaItalia=open('LinkerBI.txt','w')
            LinkerBancaItalia.write(vals)
            LinkerBancaItalia.close()
            return ("Welcome BI")

        if (data[0][0]=='ISTAT'):
            LinkerBancaIstat=open('LinkerISTAT.txt','w')
            LinkerBancaIstat.write(vals)
            LinkerBancaIstat.close()
            return ("Welcome istat")

        #print "@@@",msgType
        if (msgType=='QUERY'):
            print "-------- SERVER QUERY ----------"
            query=data[2]#[0]
            #print "----------"
            #print query
            #print "----#####------"
            field=query#.split(' ')
            #print field
            #print "----#####---------"
            dfISTAT,idkeyA=mkdf('LinkerISTAT.txt')

            dfBI,idkeyB=mkdf('LinkerBI.txt')

            DataIntersection = pd.merge(dfBI, dfISTAT, how='inner', left_on = idkeyA, right_on = idkeyB)

            print ("server: query mode ----")

            resultdf= DataIntersection.groupby(field).count()[idkeyA].reset_index()
            columns=resultdf.columns
            #print columns.values
            msglist=resultdf.values.tolist()
            m=FromList2Mess(msglist,'LINKER',columns)
            #print str(m)

            return str(m)



        resp= 'no actions'
        return str(resp)







if __name__ == '__main__':
    #generate RSA key pair (public,private) for the server

    # print  n
    #
    # print  d
    #
    # # d chiave privata
    # fout=open(localKey,"w")
    # fout.write(str(n))
    # fout.close()
    #
    # fin=open(fileName,"r")
    # srv_vals=fin.read()
    # fin.close()
    # server_elements=srv_vals.split(",")
    # for i in range(len(server_elements)):
    #     server_elements[i]=str(server_elements[i])
    # print server_elements[:10]
    #_=raw_input('server element top 10')
    app.run(host=IP, port=port)
