Lithar è un programma di backup.
Funzioni desiderate:
- Creare il backup di tutti i contenuti di una folder (Target), incluse le subfoldere i loro contenuti fino alle ultime ramificazioni.
- Aggiornare un backup pre-esistente della folder Target, aggiornando soltanto i file che sono stati modificati.
- Probabilmente lo status modificato verrà valutato in base alle data di ultima modifica del file Vs data di modifica del file in backup.
- Creare un archivio del backup


PARTI:

PART I
-Benvenuto e controllo della situazione. --DONE--
-Lithar riceve la sorgente dei dati originali e la destinazione in cui salvare il backup --DONE--
-Lithar mostra eventuali backup fodlers e archivi zip già presenti --DONE--
-- mostra la data di creazione del back dopo che si inserisce la data nel nome.
-Lithar chiede che azioni fare:
-- creare un nuovo backup --DONE--
--- creare un nuovo backup con la data di creazione nel nome della folder.
-- creare un archivio .zip (sempre dell'originale) --DONE--
-- Mostra l'elenco degli Archivi precedenti e il timestamp della loro ultima modifica.

PART II (ToDo)
Lithar offre di aggiornare folder di backup

ToDo Core:
-Funzione createArc() che crea un archivio (--DONE--)
-Funzione createBak() crea l'intero backup semplicemente copincollando le folder --DONE--
-Funzione checkFile() controlla che folder di backup e archivi .zip esistono già --DONE--
-Funzione updateBak() aggiorna una folder di backup sovrascrivendo i file con modifica più recente.

-Funzione updateArc() aggiorna un archivio .zip esistente sovrascrivendo i file modificati. --ABANDONED--

ToDo Optional e Refactoring
-cambiare il formato della data dell'ultima modifica (ad es in PART I)
-Funzione acquirePath(): modularizzare la funzione per prendere i path sorgente e destinazione --DONE--
--Funzione cleanPath(): prende i path da masterFile e rimuove il linebreak alla fine (se presente). --DONE--
-Funzione createMaster(): crea il Masterfile da cui prendere i path sorgente e destinazione
-file .bin con metadati sulle date di creazione? goosh
-file settings con litharsettings class per colori nella cmd line, comandi localizzati... supergooosh
