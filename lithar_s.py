# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:53:15 2020 Finished 28/01/2020
ver 1.0

The program backs up an entire folder (i.e. all it's contents: file and 
subfolders) in a _bak folder.
If there is already a _bak folder with the same format used by Lithar 
it will be updated it by overwriting each archived file with a most 
recent version (if present in the original folder).Files without an 
update will be skipped. File removed from the original folder will be
removed from the _bak folder as well.

ver 1.1

Better acquirePath() function. Relies on a .dat file that contains a 
database/dic with the original and bakPath of several backup of 
different folders so that the user can choose which one to handle.

@author: Exluso
"""

#! python3
import os, logging, shutil, re, sys, time, zipfile, send2trash
from acquirePath2 import acquirePath

def leaveLithar():
    input("Premi Invio per lasciare Lithar.")
    sys.exit()

def shortPrint(path):
    '''print on screen the string of a path replacing the central part
    with ... to improve the display'''
    #ToDO this function

def cleanPath(line):
    '''removes the linebreak at the end of a string line (if present)'''
    if line.endswith("\n"):
        return line[:-1]
    else:
        return line

def createBak(source, dest):
    ''' creates a new directory source_bakXX where the source is copied.
    XX is a serial number, in case of more than 1 backups
    source = path of the original folder
    dest = path where to create the backup'''
    
    lastBak = 0
    serialN=0
    for folder in bakList:
        try:
            serialN = int(folder.lstrip(baseFileName+"_bak"))
        except:
            pass
        if serialN > lastBak:
            lastBak = serialN

    shutil.copytree("\\\\?\\" + source, os.path.join("\\\\?\\" + dest, os.path.basename(source)+ "_bak"+ str(lastBak+1))) # mother folder is just the folder with serial number
    #shutil.copytree(source, dest + os.sep + os.path.basename(source)+ "_bak"+ str(lastBak+1)+os.sep + os.path.basename(source)) #mother folder with same name as original
    print("È stata creata una nuova folder di backup: %s" %(os.path.basename(source)+ "_bak"+ str(lastBak+1)))

def updateBak(bak):
    ''' Parent func for updating and removing files in an already existent backup.
    Also reports the above changes with showChanges'''
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

            try:
                removeBakFile(os.path.join("\\\\?\\" + bakPath, bak, "" if curFolder == original else os.path.relpath(curFolder,original)),curFolder)
            except:
                pass
            for folder in folders:
                if folder not in os.listdir(os.path.join("\\\\?\\" + bakPath, bak, "" if curFolder == original else os.path.relpath(curFolder,original))):
                    os.mkdir(os.path.join("\\\\?\\" + bakPath, bak, "" if curFolder == original else os.path.relpath(curFolder,original), folder))


            #print(fileNames)
            for fileName in fileNames:
                origLmd = os.path.getmtime(os.path.join("\\\\?\\" + curFolder,fileName))
                try:
                # Catch an error in case the file in the original does not exist in the bak
                    bakFilename = os.path.join("\\\\?\\" + bakPath,bak,"" if curFolder == original else os.path.relpath(curFolder,original),fileName)
                    #logging.debug("backfilename: %s" %bakFilename)
                    bakLmd = os.path.getmtime(bakFilename)
                except FileNotFoundError:
                    print(fileName, "non esiste nel backup e verrà inserito ora.")
                    bakLmd = 0
                    #updatedList.append(fileName)
                #logging.debug("curFolder: %s   fileName: %s    original: %s" %(curFolder, fileName, original))
                # logging.debug("origin file: %s fileName: %s" %(os.path.join(curFolder,fileName),fileName))
                # logging.debug("baked file: %s" %bakFilename)
                # logging.debug("----------*-*--------------")
                if origLmd > bakLmd:
                    shutil.copy(os.path.join("\\\\?\\" + curFolder,fileName), bakFilename)
                    updatedList.append(bakFilename)

            # removeBakFile(os.path.join("\\\\?\\" + bakPath, bak,
            #                            "" if curFolder == original else os.path.relpath(curFolder, original)),
            #               curFolder)
            
    def removeBakFile(bakFolder,actualFolder):
        """ checks if a the bakfolder has a file that is not present anymore in the actualFolder (redundantFile).
        If so, it renames the redundant file with a "bak_" prefix and moves it to the bin."""
        logging.debug("ActualFolder: %s" %actualFolder)
        logging.debug("BakFolder: %s" %bakFolder)
        for bakFile in os.listdir(bakFolder):
            if os.path.isfile(os.path.join("\\\\?\\" + bakFolder,bakFile)):
                if bakFile not in os.listdir(actualFolder):
                    logging.debug("redundant: %s" %bakFile)
                    redundantFlag = shutil.move(os.path.join("\\\\?\\" + bakFolder,bakFile),os.path.join(bakFolder,"bak_"+bakFile))
                    send2trash.send2trash(redundantFlag)
                    redundantList.append(redundantFlag)
    logging.debug("redundantList: %s" %redundantList)
    logging.debug("updatedList: %s" %updatedList)
    def showChanges():
        '''shows the list of removed redundant files'''
        def showList(lista):
            for i in lista:
                print(str(lista.index(i))+")".ljust(4) + os.path.basename(i).ljust(40," ") + os.path.dirname(i).ljust(50))
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
            savingPath = os.path.join("\\\\?\\" + curFolder, fileName)
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
        #ToDO: prova a cambiare il formato della data, avendo l'anno 
        # prima dell'ora
        print(("Ho trovato i seguenti archivi che potrebbero contenere backup"
        " precedenti: \n"))
        print("#".ljust(4) + "ARCHIVIO".ljust(15)+ "ULTIMA MODIFICA".ljust(30))
        for folder in bakList:
            lmdEpoch = os.path.getmtime(bakPath+os.sep+folder)
            lmd = time.ctime(lmdEpoch)
            print((str(bakList.index(folder)+1)+ ") ").center(4," ") 
                + (folder).ljust(15) + str(lmd).ljust(30))
            
        for arc in archList:
            lmdEpoch = os.path.getmtime(bakPath+os.sep+arc)
            lmd = time.ctime(lmdEpoch)
            print(("z"+str(archList.index(arc))+ ") ").center(4) 
            + (arc).ljust(15) + str(lmd).ljust(30))
    
    if len(bakList) < 1:
        print("Non sono state trovate folder di backup precedenti.")
    if len(archList) < 1:
        print("Non sono stati trovati archivi .zip precedenti.")

def askUser():
    '''Lithar offers to create a backup, to update a backup, to create 
    an archive'''
    #ToDo: assegna i comandi a delle variabili e usale sia nelle 
    # stringhe che negli "if" (classe Lithar?)
    #ToDo: prova a colorare il testo su cmq line
    print()
    print("Digita \"b\" per creare una nuova folder di backup.")
    print(("Digita \"aggiorna\" seguito dal numero del backup per aggiornare "
    "il backup (es. aggiorna 1)."))
    print("Digita \"z\" per creare un nuovo archivio .zip")
    print("Digita qualunque altra cosa per uscire da Lithar.")
    
    choice = input("Inserisci il comando corrispondente alla tua scelta: \n")

    return choice

logging.basicConfig(
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")
# logging.disable(logging.CRITICAL) #uncomment to remove logging
print(100*"~")

print("\n/**BENVENUTO IN LITHAR**\\")
logging.debug("Starts in cwd: " + os.getcwd())


#path of original folder, path where to create the backup folder
original , bakPath = acquirePath()  
baseFileName = os.path.basename(original)

logging.debug("original: %s" %(original))
logging.debug("bakPath: %s" %(bakPath))



print("L'oggetto del tuo backup è:\n %s." %(original))
print("Il backup verrà conservato in:\n %s. \n" %(bakPath))
try:
    assert original not in bakPath, "Crossed Paths!"
except AssertionError:
    print(("Lithar can't create a backup (_bak) folder under the source folder"
    " itself. Make sure that the destination path of the backup it is not a "
    "subPath of the source. In other words: the source path should not be "
    "included in the backup path"))
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
        updateBak(os.path.join("\\\\?\\" + bakPath, bakList[int(choice.lstrip("aggiorna"))-1]))
    except IndexError:
        print("Hai inserito un numero che non corrisponde a nessun backup.")
    #except ValueError:
        print('Devi inserire un numero dopo "aggiorna".')
else:
    print("Comando non riconosciuto (o implementato).")

leaveLithar()


print(100*"~" + "\n")

    


