From its second version Lithar will use a shelve file(s) to save multiple backup information.
the shelve file name is LitharMaster

The data it will save are (for each back up project):
1. Backup name (i.e. a name that identifies the project)
2. the Absolute path of the original folder (the one to be backed up)
3. the absolute path of the destinatio where to save backups (bakPath)

The shelve files contains entry structured as follows:
LitharMaster.key = the name of the backup (1.)
LitharMaster.value= a tuple containing original and bakPath paths

additionally there is also a LitharMaster[indexList] list variable that contains all the backups name for reference.