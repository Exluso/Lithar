# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:53:15 2020

The program backs up an entire folder (i.e. all it's contents: file and subfolders) in a .zip archive.
If there is already a .zip archive with the same format used by the program, it will update
by overwriting the most recent version (if present) of each file.
Files without an update will be skipped.

@author: Exluso
"""

import os, logging, shutil, re, sys, time

#ToDo: createArc function
def createArc(dest, name):
''' Creates a .zip Archive named with a sequential number that follows the greater numbered name already in the folder
INPUT: dest = absolute path where to create the .zip
        name = base name of the .zip (without sequential number) '''

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
print("L'oggetto del tuo backup è:\n %s." %(masterLines[0][:-1]))
print("Il backup verrà conservato in:\n %s. \n" %(masterLines[1]))

# Checks if there are previous archives and prints them in order

newZipCoreName = os.path.basename(masterLines[0][:-1])

logging.debug("New Zip Core Name: %s" %(newZipCoreName))
logging.debug("dir files: %s" %(os.listdir(masterLines[1])))

archList =[]
for fileName in os.listdir(masterLines[1]):
    #ToDO: prova a cambiare il formato della data, avendo l'anno prima dell'ora
    logging.debug("testing now: %s " %(fileName))
    logging.debug("matchArchive: %s" % str(re.search(newZipCoreName + r'\d*' + ".zip", fileName)))    
    if re.search(newZipCoreName, fileName) is not None:
        archList.append(fileName)
    logging.debug(archList)

if len(archList)>0:
    print("Ho trovato i seguenti archivi che potrebbero contenere backup precedenti: \n")
    for arc in archList:
        lmdEpoch = os.path.getmtime(masterLines[1]+os.sep+arc) #return the "last modified" date (hopefully)
        lmd = time.ctime(lmdEpoch)
        print((str(archList.index(arc))+ ") ").center(3) + (arc).ljust(15) + str(lmd).rjust(30,"_"))
    #ToDo: offer to update an archive or create a new one
else:
    #ToDo: it there are no archives, offer to create one
    choice = input("Non ci sono archivi precedenti. Ne creo uno? (y/n)") # placeholder


print(100*"-" + "\n")

    


