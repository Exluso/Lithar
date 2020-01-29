import os, logging, shutil, shelve

logging.basicConfig(
    level = logging.DEBUG, 
    format = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")

def showList(lista):
    '''prints a List in a human friendly layout.
    Index first, then the corresponding value'''
    

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

        if len(shelveIndex[indice]) >0:
            print("#)".ljust(4), "BACKUP".ljust(20))
            for item in shelveIndex[indice]:
                print(str(shelveIndex[indice].index(item)+1).ljust(4),
                item.ljust(20))
                return True
        else:
            print("Non sono stati trovati backup indicizzati.")
            return False

    def askUser0(areBackups):
        ''' asks the user if they want to work on a backup or create a 
        new one.
        Return a string that represents the user choice.'''

        if areBackups: 
            print(
            "Digita il numero corrispondente per accedere ad un backup."
            )
        print('Digita "n" per creare un nuovo backup.')

        choice = input() #crash in console!!!
        return choice

    def createSave():
        '''creates the LitharMaster shelve files.
        Initialize them with a indexList list Variable.'''

        shelveIndex = shelve.open(masterFile)
        shelveIndex[indice]=[]
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

    
    def createRecord():
        '''creates a new record (entry) in the savedata file.
        The entry includes the backup name, itand its original
        and backPath path'''
        #ToDo controlla che salvi le variabili in shelveIndex
        
        name = input("Digita il nome che vuoi dare al backup:\n")
        original = input("Digita il percorso della folder originale:\n")
        bakPath = input("Digita il percorso dove salvare i/l backup:\n")
        
        
        shelveIndex = shelve.open(masterFile)
        
        shelveIndex[indice].append(name)
        shelveIndex[name]=(original,bakPath)
        
        shelveIndex.close()
        
    
    choice = (askUser0(showBakList()))
    
    if choice == "n":
        createRecord()
        
acquirePath()

