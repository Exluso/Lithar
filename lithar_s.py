# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:53:15 2020

@author: Exluso
"""

import os, logging, shutil, re

logging.basicConfig(level = logging.DEBUG, format = "%(asctime)s - %(levelname)s - %(message)s")
#logging.disable(logging.CRITICAL)

logging.debug("Start")

def matchArchive(testName, CoreName):
    #looks for .zip archive of with the same CoreName of the target folder.
    # CoreName: a str with the name of the original folder
    LithArchivePat = re.compile(CoreName + r"\d*.zip")
    if LithArchivePat.search(testName) != None:
        return True
    else:
        return False
    
#The program starts and gets the path of the target folder (i.e. the one that 
#needs to be zipped and the path where to store the .zip archive
# it also gets the root for the name of the .zip archive from the target folder
# masterFile.txt is where the path are stored.
masterFile = open("D:\Python projects\Lithar_Studi\LitharMaster.txt","r")

masterLines= masterFile.readlines()

logging.debug("Sorgente: %s" %(masterLines[0]))
logging.debug("Destinazione: %s" %(masterLines[1]))

print("BENVENUTO IN LITHAR.")
print("L'oggetto del tuo back up è:\n %s." %(masterLines[0][:-1]))
print("Il backup verrà conservato in:\n %s." %(masterLines[1]))

newZipCoreName = os.path.basename(masterLines[0])

logging.debug("Archive Core Name: %s" %(newZipCoreName))

for fileName in os.listdir(masterLines[1]):
    logging.debug("testing now: " + fileName)    
    if matchArchive(fileName, newZipCoreName): #fileName.endswith(".zip"):
        print("C'è già un archivio zip: %s" %(fileName))
        com = input("Vuoi aggiornarlo? (a) \nVuoi crearne uno nuovo? (n)\n")
        

