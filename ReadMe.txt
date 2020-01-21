Lithar è un programma di backup.
Funzioni desiderate:
- Creare il backup di tutti i contenuti di una folder (Target), incluse le subfoldere i loro contenuti fino alle ultime ramificazioni.
- Aggiornare un backup pre-esistente della folder Target, aggiornando soltanto i file che sono stati modificati.
- Probabilmente lo status modificato verrà valutato in base alle data di ultima modifica del file.


PARTI:

PART I (done)
-Benvenuto e controllo della situazione.
-Lithar riceve la sorgente dei dati originali e la destinazione in cui salvare il backup
-Lithar chiede se si vuole fare un l'archivio .zip del backup
-- Mostra l'elenco degli Archivi precedenti e il timestamp della loro ultima modifica.

PART II (ToDo)
Lithar offre di creare/aggiornare archivi

ToDo Core:
-Funzione createArc() che crea un archivio

-Funzione updateArc() aggiorna un archivio esistente sovrascrivendo i file modificati. --ABANDONED--

ToDo Optional Refactoring
-cambiare il formato della data dell'ultima modifica (ad es in PART I)
-Funzione acquirePath(): modularizzare la funzione per prendere i path sorgente e destinazione
--Funzione cleanPath(): prende i path da masterFile e rimuove il linebreak alla fine (se presente).
---- cambiare nel codice le occorrenze di masterLine[0][:-1] ad una variabile col path generato da cleanPath()
-Funzione createMaster(): crea il Masterfile da cui prendere i path sorgente e destinazione
