import os, logging, shutil, shelve,sys

logging.basicConfig(
    level = logging.DEBUG, 
    format = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")


def acquirePath():
    """gets the data from a shelve file
    if the file does not exist, creates
    one"""

    def showBakList():
        '''prints the list of already available backups, paired with
        their original and bakPath paths.
        Returns a boolean: True if there are already backup saved in the
        file indice. False if the file indice is empty.'''
        shelveIndex = shelve.open(masterFile)
        print()
        if len(shelveIndex[indice]) > 0:
            print("#)".ljust(4), "BACKUP".ljust(20))
            for item in shelveIndex[indice]:
                print((str(shelveIndex[indice].index(item)+1)+")").ljust(4),
                item.ljust(20))
            shelveIndex.close()
            return True
        else:
            print("Non sono stati trovati backup indicizzati.")
            shelveIndex.close()

            return False

    def askUser0(areBackups):
        ''' asks the user if they want to work on a backup or create a 
        new one.
        Return a string that represents the user choice.'''
        print()
        if areBackups: 
            print((
            "Digita il numero corrispondente per accedere ad un progetto"
            " backup.")
            )
            print(("Digita 'delete' seguito dal numero corrispondente "
            "per eliminare un progetto backup . \n\tNOTA: questa proced"
            "ura non elimina le folder _bak relative al progetto, ma sol"
            "o la sua indicizzazione in Lithar."))
        print('Digita "n" per creare un nuovo progetto backup.')
        print('Digita "chiudi" per chiudere Lithar.')

        choice = input() #crash in console!!!
        return choice

    def createSave():
        '''creates the LitharMaster shelve files.
        Initialize them with a indexList list Variable.'''

        shelveIndex = shelve.open(masterFile)
        shelveIndex[indice]=[]
        shelveIndex.close()
    
    def createRecord():
        '''creates a new record (entry) in the savedata file.
        The entry includes the backup name, itand its original
        and backPath path'''
        #ToDo make it so that the shelveIndex[indice] does not contain 
        # duplicates when a new project is added with the same name of
        # a previous one.                
        name = input("Digita il nome che vuoi dare al backup:\n")
        original = input("Digita il percorso della folder originale:\n")
        bakPath = input("Digita il percorso dove salvare i/l backup:\n")
        
        
        shelveIndex = shelve.open(masterFile)
        
        ListaIndice = shelveIndex[indice]
        if name not in ListaIndice:
            ListaIndice.append(name)        
        shelveIndex[indice]=ListaIndice
        shelveIndex[name]=(original,bakPath)
        
        shelveIndex.close()
        print("Il nuovo record %s è stato creato." %name)

    def deleteRecord(index):
        '''removes a record from the shelve save file.
        Deletes the shelveIndex key with the paths and the 
        shelveIndex[indice] element
        index = index of the ShelveIndex[indice] correponding to the
        shelveIndex key to delete. '''
        shelveIndex = shelve.open(masterFile)
        ListaIndice = shelveIndex[indice]
        del shelveIndex[ListaIndice.pop(index)]
        shelveIndex[indice] = ListaIndice

        shelveIndex.close()
        print("Il record è stato eliminato.")
    
    def accessRecord(index):
        '''returns the original and bakPath paths for the selected
        record.
        index = integer of the record index in shelveIndex[indice]'''
        shelveIndex = shelve.open(masterFile)
        ListaIndice = shelveIndex[indice]
        origin, dest = shelveIndex[ListaIndice[index]]
        print()
        print("Vuoi accedere a:")
        print("Progetto: %s".ljust(20) %ListaIndice[index])
        print("Folder attuale: %s".ljust(20) %origin)
        print("Folder contenente i backup: %s".ljust(20) %dest)
        while True:
            confirm = input("\nConfermi (s/n): ")
            if confirm == "s":
                return (origin,dest)
            elif confirm == "n":
                #ToDo trova un modo migliore di uscire
                #input("Premi INVIO per chiudere Lithar.")
                sys.exit() #ToDo indaga perché sys.exit non esce dal loop
            else:
                print("Devi risponde s o n per sì o no.")


        shelveIndex.close()

    logging.debug("cwd: %s" %os.getcwd())
    
    masterFile = "LitharMaster" #name of the save data file
    indice = "indexList" #name of the save file core variable

    print(masterFile)

    while True:
        if os.path.isfile(os.path.join(('.'),masterFile)+".dat"):
            break
        else:
            createSave()      
    while True:
        choice = (askUser0(showBakList()))
        
        if choice == "n":
            createRecord()
        elif choice.startswith("delete"):
            deleteRecord(int(choice.lstrip("delete"))-1)
        elif choice == "chiudi":
            sys.exit()
        else:
            try:
                choice = int(choice)-1
                return accessRecord(choice)
            except:
                print("Hai inserito un valore sbagliato, riprova.")
        
originale, bakPath = acquirePath()
print("originale: %s \nbakPath: %s" %(originale, bakPath))

