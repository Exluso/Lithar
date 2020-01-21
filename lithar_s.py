# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:53:15 2020

The program backs up an entire folder (i.e. all it's contents: file and subfolders) in a .zip archive.
If there is already a .zip archive with the same format used by the program, it will update it
by overwriting each archived file with a most recent version (if present in the original folder).
Files without an update will be skipped.

@author: Exluso
"""
#ToDo uncomment shebang
# #! python3
import os, logging, shutil, re, sys, time, zipfile

def cleanPath(line):
    ''' removes the linebreak at the end of a string line (if present)'''
    if line.endswith("\n"):
        return line[:-1]
    else:
        return line

def acquirePath(file):
    '''Takes the source from the first 2 lines from the LitharMaster.txt
    se il path termina con un linebreak lo rimuove tramite cleanPath().
    Returns 2 path source and dest'''
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

    source = cleanPath(masterLines[0])
    dest = cleanPath(masterLines[1])
    masterFile.close()

    return (source, dest)

#ToDo: crea una funzione per far creare il file direttamente al programma 
# chiedendo all'utente i percorsi necessari.
def createBak(source, dest):
    ''' creates a new directory source_bakXX where the source is copied.
    XX is a serial number, in case of more than 1 backups'''
    #ToDo implement a proper serial number
    serialN = "01" #placeholder
    shutil.copytree(source, dest + os.sep + os.path.basename(source)+ "_bak"+serialN)


def createArc(dest, name):
    ''' Creates a .zip Archive named with a sequential number that follows the greater numbered name already in the folder
    INPUT: dest = absolute path where to create the .zip
    name = base name of the .zip (without sequential number) '''
    logging.debug("createArch.archlist: %s" %(archList))
    logging.debug("name: %s" %(name))
    #Create archive
    lastArch = 0
    try:
        for arch in archList:
            serialNum = int(arch.lstrip(name).rstrip(".zip"))
            logging.debug("Current Serial: %d" % (serialNum))
            if serialNum > lastArch:
                lastArch = serialNum
        logging.debug("lastArch finale: {}".format(lastArch))
        
        newArc = zipfile.ZipFile(dest + os.sep + name + str(lastArch+1)+".zip","w")
    # adds file to archive
        for curFolder, subFolders, fileNames in os.walk(os.path.basename(source)):
            for fileName in fileNames:
                savingPath = os.path.join(curFolder, fileName)
                newArc.write(savingPath, compress_type=zipfile.ZIP_DEFLATED)
        
    except:
        print("Qualcosa è andato storto. Verifica che il nome degli archivi già presenti sia come il seguente:")
        print('"Nome della folder originale" + numero seriale + ".zip"')
    finally:
        newArc.close()

logging.basicConfig(level = logging.DEBUG, format = "%(asctime)s - %(levelname)s - %(message)s")
#logging.disable(logging.CRITICAL) #uncomment to remove logging
print("----------------------------------------------------------------------------------")

logging.debug("Starts in cwd: " + os.getcwd())
 
#The program starts and gets the path of the target folder (i.e. the one that 
#needs to be zipped and the path where to store the .zip archive
#it also gets the root for the name of the .zip archive from the target folder
#LitharMaster.txt is where the path are stored.

original , bakPath = acquirePath("MasterFile.txt") #path of original folder, path where to create the backup folder
logging.debug("Sorgente: %s" %(original))
logging.debug("Destinazione: %s" %(bakPath))

print("\nBENVENUTO IN LITHAR.")
print("L'oggetto del tuo backup è:\n %s." %(original))
print("Il backup verrà conservato in:\n %s. \n" %(bakPath))

# Checks if there are previous archives and prints them in order

newZipCoreName = os.path.basename(original)

logging.debug("New Zip Core Name: %s" %(newZipCoreName))
logging.debug("dir files: %s" %(os.listdir(bakPath)))

archList =[]
for fileName in os.listdir(bakPath):
    #ToDO: prova a cambiare il formato della data, avendo l'anno prima dell'ora
    logging.debug("testing now: %s " %(fileName))
    logging.debug("matchArchive: %s" % str(re.search(newZipCoreName + r'\d*' + ".zip", fileName)))    
    if re.search(newZipCoreName, fileName) is not None:
        archList.append(fileName)
    logging.debug(archList)

if len(archList)>0:
    print("Ho trovato i seguenti archivi che potrebbero contenere backup precedenti: \n")
    print("#".ljust(3) + "ARCHIVIO".ljust(15) + "ULTIMA MODIFICA".ljust(30))
    for arc in archList:
        lmdEpoch = os.path.getmtime(bakPath+os.sep+arc) #return the "last modified" date (hopefully)
        lmd = time.ctime(lmdEpoch)
        print((str(archList.index(arc))+ ") ").center(3) + (arc).ljust(15) + str(lmd).ljust(30))
    #ToDo: offer to update an archive or create a new one
    print("Per aggiornare un archivio, immetti il numero corrispondente.")
    choice = input("\nPer creare un nuovo backup digita \"b\", per un archivio digita \"n\".\n")
else:
    #ToDo: it there are no archives, offer to create one
    print("Non ci sono backup. Digita \"b\" per crearne uno.")
    choice = input("Non ci sono archivi precedenti. Digita \"z\" per crearne uno nuovo. \n") # placeholder

#ToDo: use assert/exception to check that the number of the archive is not greater than len(archList)

if choice == "b":
    createBak(original, bakPath)
elif choice == "z":
    createArc(bakPath, os.path.basename(original))


print(100*"-" + "\n")

    


