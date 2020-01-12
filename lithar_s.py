# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:53:15 2020

@author: Exluso
"""

import os, logging, shutil, re, sys

logging.basicConfig(level = logging.DEBUG, format = "%(asctime)s - %(levelname)s - %(message)s")
#logging.disable(logging.CRITICAL)

logging.debug("Starts in cwd:" + os.getcwd())

def matchArchive(testName, CoreName):
    #looks for .zip archive of with the same CoreName of the target folder.
    # CoreName: a str with the name of the original folder

    #TODO: vedi se funge
    
    LithArchivePat = re.compile(CoreName + r"\d*.zip")
    if LithArchivePat.search(testName) != None:
        return True
    else:
        return False
    
#The program starts and gets the path of the target folder (i.e. the one that 
#needs to be zipped and the path where to store the .zip archive
#it also gets the root for the name of the .zip archive from the target folder
#LitharMaster.txt is where the path are stored.

try:
    masterFile = open(os.getcwd()+os.sep + "LitharMaster.txt","r")
    masterLines= masterFile.readlines()

except:
    print("""Non è stato trovato alcun LitharMaster.txt file.
    Per permettere al programma di funzionare crea LitharMaster.txt
    nella stessa folder del programma inserendo:
    1 riga il path della folder da zippare
    2 riga path dove creare l'archivio """)
    sys.exit()
    
    #ToDo: crea una funzione per far creare il file direttamente al programma 
    # chiedendo all'utente i percorsi necessari.

logging.debug("Sorgente: %s" %(masterLines[0]))
logging.debug("Destinazione: %s" %(masterLines[1]))

print("BENVENUTO IN LITHAR.")
print("L'oggetto del tuo back up è:\n %s." %(masterLines[0][:-1]))
print("Il backup verrà conservato in:\n %s." %(masterLines[1]))

newZipCoreName = os.path.basename(masterLines[0])

logging.debug("New Zip Core Name: %s" %(newZipCoreName))

for fileName in os.listdir(masterLines[1]):
    logging.debug("testing now: " + fileName)    
    if matchArchive(fileName, newZipCoreName): #fileName.endswith(".zip"):
        print("C'è già un archivio zip: %s" %(fileName))
        com = input("Vuoi aggiornarlo? (a) \nVuoi crearne uno nuovo? (n)\n")
        

