# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:53:15 2020

The program backs up an entire folder (i.e. all it's contents: file and subfolders) in a .zip archive.
If there is already a .zip archive with the same format used by the program, it will update
by overwriting the most recent version (if present) of each file.
Files without an update will be skipped.

@author: Exluso
"""

import os, logging, shutil, re, sys

logging.basicConfig(level = logging.DEBUG, format = "%(asctime)s - %(levelname)s - %(message)s")
#logging.disable(logging.CRITICAL) #uncomment to remove logging
logging.debug("Starts in cwd: " + os.getcwd())
 
#The program starts and gets the path of the target folder (i.e. the one that 
#needs to be zipped and the path where to store the .zip archive
#it also gets the root for the name of the .zip archive from the target folder
#LitharMaster.txt is where the path are stored.

try:
    masterFile = open(os.getcwd()+os.sep + "LitharMaster.txt","r")
    masterLines= masterFile.readlines()

except:
    print("""\nNon è stato trovato alcun LitharMaster.txt file.
    Per permettere al programma di funzionare crea LitharMaster.txt
    nella stessa folder del programma inserendo:
    1 riga il path della folder da zippare
    2 riga path dove creare l'archivio \n """)
    sys.exit()
    
    #ToDo: crea una funzione per far creare il file direttamente al programma 
    # chiedendo all'utente i percorsi necessari.

logging.debug("Sorgente: %s" %(masterLines[0][:-1]))
logging.debug("Destinazione: %s" %(masterLines[1]))

print("\nBENVENUTO IN LITHAR.")
print("L'oggetto del tuo back up è:\n %s." %(masterLines[0][:-1]))
print("Il backup verrà conservato in:\n %s. \n" %(masterLines[1]))

#checks if there is already a .zip file made by Lithar

newZipCoreName = os.path.basename(masterLines[0][:-1])

logging.debug("New Zip Core Name: %s" %(newZipCoreName))
logging.debug("dir files: %s" %(os.listdir(masterLines[1])))

for fileName in os.listdir(masterLines[1]):
    #ToDO: fai in modo che il loop ritorni una lista degli archivi precedenti solo alla fine del loop
    logging.debug("testing now: %s " %(fileName))
    logging.debug("matchArchive: %s" % str(re.search(newZipCoreName + r'\d*' + ".zip", fileName)))
    if re.search(newZipCoreName, fileName) is not None:
        print("È stato trovato un archivio con lo stesso nome: %s."  %(fileName))
    else:
        print("Non ci sono archivi precedenti. Ne creo uno.") # Placheholder


