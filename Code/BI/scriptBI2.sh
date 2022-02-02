#Servers starting 
python psiServer.py 127.0.0.1 5000 ./DATASET_B_BANCA_ITALIA.csv ../BIkey&

read -p "Attendo che l'altro server sia in ascolto" yn
# create intersection Files
python psiClient2.py  127.0.0.1 5001 ./DATASET_B_BANCA_ITALIA.csv ../ISTATkey intersezioneBI.txt

# spedisce i dati criptati intersecati e arricchiti al linker
python psiSymmetricCriptSend.py 127.0.0.1 5002 3425245235 ./DATASET_B_BANCA_ITALIA.csv intersezioneBI.txt BI
