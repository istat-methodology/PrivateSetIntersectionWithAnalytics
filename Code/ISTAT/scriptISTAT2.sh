#Servers starting 
python psiServer.py 127.0.0.1 5001 ./DATASET_A_ISTAT.csv ../ISTATkey&

read -p "Attendo che l'altro server sia in ascolto" yn

# create intersection Files
python psiClient2.py  127.0.0.1 5000 ./DATASET_A_ISTAT.csv ../BIkey intersezioneISTAT.txt

# prepareencripted local dataset for intersecated row  and send it to linke 
python psiSymmetricCriptSend.py 127.0.0.1 5002 3425245235 ./DATASET_A_ISTAT.csv intersezioneISTAT.txt ISTAT

