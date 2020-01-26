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
#! python3
import os, logging, shutil, re, sys, time, zipfile, send2trash
def leaveLithar():
    input("Premi Invio per lasciare Lithar.")
    sys.exit()

def cleanPath(line):
    ''' removes the linebreak at the end of a string line (if present)'''
    if line.endswith("\n"):
        return line[:-1]
    else:
        return line

def acquirePath():
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

#ToDo: crea una funzione per far creare il file LitharMaster.txt direttamente al programma 
# chiedendo all'utente i percorsi necessari.
def createBak(source, dest):
    ''' creates a new directory source_bakXX where the source is copied.
    XX is a serial number, in case of more than 1 backups'''
    
    lastBak = 0
    serialN=0
    for folder in bakList:
        try:
            serialN = int(folder.lstrip(baseFileName+"_bak"))
        except:
            pass
        if serialN > lastBak:
            lastBak = serialN

    shutil.copytree(source, dest + os.sep + os.path.basename(source)+ "_bak"+ str(lastBak+1)) # mother folder is just the folder with serial number
    #shutil.copytree(source, dest + os.sep + os.path.basename(source)+ "_bak"+ str(lastBak+1)+os.sep + os.path.basename(source)) #mother folder with same name as original
    print("È stata creata una nuova folder di backup: %s" %(os.path.basename(source)+ "_bak"+ str(lastBak+1)))

def updateBak(bak):
    ''' Parent func for updating and removing files in an already existent backup.
    Also reports the above cahgnes with showChanges'''
    updatedList = []
    redundantList = []
    def updateBakFile(bak):
        ''' bak = basename of the backup folder.
        Loops into the source and the _bak folder, comparing the last modified date of each file
        in the backup and in the source. If the source is more recent it will overwrite the one in the _bak
        If the file is not present in the bak it will be added.'''
        logging.debug("bak: %s" %bak)
        for curFolder, folders, fileNames in os.walk(original):
            logging.debug("curFolder: %s curRel: %s" %(curFolder, os.path.relpath(curFolder,original)))
            
            removeBakFile(os.path.join(bakPath, bak, "" if curFolder == original else os.path.relpath(curFolder,original)),curFolder)

            for fileName in fileNames:
                origLmd = os.path.getmtime(os.path.join(curFolder,fileName))
                try:
                #Catch an error in case the file in the original does not exist in the bak
                    bakFilename = os.path.join(bakPath,bak,"" if curFolder == original else os.path.relpath(curFolder,original),fileName)
                    #logging.debug("backfilename: %s" %bakFilename)
                    bakLmd = os.path.getmtime(bakFilename)
                except FileNotFoundError:
                    print(fileName, "non esiste nel backup e verrà inserito ora.")
                    bakLmd = 0
                #logging.debug("curFolder: %s   fileName: %s    original: %s" %(curFolder, fileName, original))
                # logging.debug("origin file: %s fileName: %s" %(os.path.join(curFolder,fileName),fileName))
                # logging.debug("baked file: %s" %bakFilename)
                # logging.debug("----------*-*--------------")
                if origLmd > bakLmd:
                    shutil.copy(os.path.join(curFolder,fileName), bakFilename)
                    updatedList.append(bakFilename)
            
    def removeBakFile(bakFolder,actualFolder):
        """ checks if a the bakfolder has a file that is not present anymore in the actualFolder (redundantFile).
        If so, it renames the redundant file with a "bak_" prefix and moves it to the bin."""
        logging.debug("ActualFolder: %s" %actualFolder)
        logging.debug("BakFolder: %s" %bakFolder)
        for bakFile in os.listdir(bakFolder):
            if os.path.isfile(os.path.join(bakFolder,bakFile)):
                if bakFile not in os.listdir(actualFolder):
                    logging.debug("redundant: %s" %bakFile)
                    redundantFlag = shutil.move(os.path.join(bakFolder,bakFile),os.path.join(bakFolder,"bak_"+bakFile))
                    send2trash.send2trash(redundantFlag)
                    redundantList.append(redundantFlag)

    def showChanges():
        '''shows the list of removed redundant files'''
        def showList(lista):
            for i in lista:
                print(str(lista.index(i))+")".ljust(4) + os.path.basename(i).ljust(40," ") + os.path.dirname(os.path.relpath(i,os.path.join(bakPath)).ljust(40)))
        if len(updatedList)>0:
            print("Sono stati aggiornati i seguenti file:")
            showList(updatedList)
        print(100*"~")
        if len(redundantList)>0:
            print("Sono stati rimossi i seguenti file:")
            showList(redundantList)
         
    updateBakFile(bak)
    showChanges()
    
def checkForFile(tipo = "bak"):
    '''returns a list of the specific file or folder in the bakPath directory
    2nd argument: "zip" to check for .zip archives, "bak" to check for backup fodler'''
    fileList = []
    if tipo == "bak":
        pat = re.compile(baseFileName + "_bak" +r'\d*')
    elif tipo == "zip":
        pat = re.compile(baseFileName + r'\d*' + ".zip")
    else:
        print("ATTENZIONE TIPO DI FILE NON SPECIFICATO!")
    
    for thing in os.listdir(bakPath):
       
        logging.debug("testing now: %s " %(thing))
        logging.debug("matchArchive: %s" % str(pat.search(thing)))   
        if pat.search(thing) is not None:
            fileList.append(thing)

    return fileList

def createArc(dest, name):
    ''' Creates a .zip Archive named with a sequential number that follows the greater numbered name already in the folder
    INPUT: dest = absolute path where to create the .zip
    name = base name of the .zip (without sequential number) '''
    logging.debug("createArch.archlist: %s" %(archList))
    logging.debug("name: %s" %(name))
    #Create archive
    lastArch = 0
    #try:
    for arch in archList:
        serialNum = int(arch.lstrip(name).rstrip(".zip"))
        logging.debug("Current Serial: %d" % (serialNum))
        if serialNum > lastArch:
            lastArch = serialNum
    logging.debug("lastArch finale: {}".format(lastArch))
    
    newArc = zipfile.ZipFile(dest + os.sep + name + str(lastArch+1)+".zip","w")
    # adds file to archive
    for curFolder, subFolders, fileNames in os.walk(os.path.basename(original)):
        for fileName in fileNames:
            savingPath = os.path.join(curFolder, fileName)
            newArc.write(savingPath, compress_type=zipfile.ZIP_DEFLATED)
        
    # except:
    #     print("Qualcosa è andato storto. Verifica che il nome degli archivi già presenti sia come il seguente:")
    #     print('"Nome della folder originale" + numero seriale + ".zip"')
    # finally:
    newArc.close()

    print("È stato creato un nuovo archivio .zip: %s" %(name + str(lastArch+1)+".zip"))

def showItems():
    #Shows backup folder and zip archives already present
    if len(bakList)>0 or len(archList)>0 :
        #ToDO: prova a cambiare il formato della data, avendo l'anno prima dell'ora
        print("Ho trovato i seguenti archivi che potrebbero contenere backup precedenti: \n")
        print("#".ljust(4) + "ARCHIVIO".ljust(15) + "ULTIMA MODIFICA".ljust(30))
        for folder in bakList:
            lmdEpoch = os.path.getmtime(bakPath+os.sep+folder)
            lmd = time.ctime(lmdEpoch)
            print((str(bakList.index(folder)+1)+ ") ").center(4," ") + (folder).ljust(15) + str(lmd).ljust(30))
            
        for arc in archList:
            lmdEpoch = os.path.getmtime(bakPath+os.sep+arc) #return the "last modified" date (hopefully)
            lmd = time.ctime(lmdEpoch)
            print(("z"+str(archList.index(arc))+ ") ").center(4) + (arc).ljust(15) + str(lmd).ljust(30))
    
    if len(bakList) < 1:
        print("Non sono state trovate folder di backup precedenti.")
    if len(archList) < 1:
        print("Non sono stati trovati archivi .zip precedenti.")

def askUser():
    #Lithar offers to create a backup, to update a backup, to create an archive
    #ToDo: assegna i comandi a delle variabili e usale sia nelle stringhe che negli "if" (classe Lithar?)
    print()
    print("Digita \" b\" per creare una nuova folder di backup.")
    print("Digita \"aggiorna\" seguito dal numero del backup per aggiornare il backup (es. aggiorna 1).")
    print("Digita \"z\" per creare un nuovo archivio .zip")
    
    choice = input("Inserisci il comando corrispondente alla tua scelta: \n")

    return choice

logging.basicConfig(level = logging.DEBUG, format = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")
logging.disable(logging.CRITICAL) #uncomment to remove logging
print(100*"-")


 
#The program starts and gets the path of the target folder (i.e. the one that 
#needs to be zipped and the path where to store the .zip archive
#it also gets the root for the name of the .zip archive from the target folder
#LitharMaster.txt is where the path are stored.

logging.debug("Starts in cwd: " + os.getcwd())

original , bakPath = acquirePath() #path of original folder, path where to create the backup folder 
baseFileName = os.path.basename(original)

logging.debug("original: %s" %(original))
logging.debug("bakPath: %s" %(bakPath))

print("\nBENVENUTO IN LITHAR.")
print("L'oggetto del tuo backup è:\n %s." %(original))
print("Il backup verrà conservato in:\n %s. \n" %(bakPath))
try:
    assert original not in bakPath, "Crossed Paths!"
except AssertionError:
    print("""Lithar can't create a backup (_bak) folder under the source folder itself.
Make sure that the destination path of the backup it is not a subPath of the source.
In other words: the source path should not be included in the backup path""")
    leaveLithar()

# Checks if there are previous archives and prints them in order

logging.debug("New Zip Core Name: %s" %(baseFileName))
logging.debug("files in dir: %s" %(os.listdir(bakPath)))

archList =checkForFile("zip")
bakList = checkForFile("bak")

logging.debug("baklist: %s" %(bakList))
logging.debug("archList: %s" %(archList))

showItems()
choice = askUser()

#Result of the user choice
if choice == "b":
    createBak(original, bakPath)
elif choice == "z":
    createArc(bakPath, os.path.basename(original))
elif choice.startswith("aggiorna"):
    try:
        updateBak(os.path.join(bakPath,bakList[int(choice.lstrip("aggiorna"))-1]))
    except IndexError:
        print("Hai inserito un numero che non corrisponde a nessun backup.")
    except ValueError:
        print('Devi inserire un numero dopo "aggiorna".')
else:
    print("Comando non riconosciuto (o implementato)")

leaveLithar()


print(100*"-" + "\n")

    


