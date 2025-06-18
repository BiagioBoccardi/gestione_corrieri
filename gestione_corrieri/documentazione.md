# Gestione Corrieri

Gestione Corrieri è un’applicazione Django per la gestione di ordini, corrieri, veicoli e consegne, con dashboard e interfaccia admin.

---

## Modelli

### Ordine

- **id_ordine**: AutoField (PK)
- **data_e_ora_ordine**: DateField
- **indirizzo**: CharField (max_length=100)
- **stato**: CharField (scelte: DA_ASSEGNARE, ASSEGNATO, TRANSITO, IN_CONSEGNA, COMPLETATO)
- **priorita**: IntegerField (scelte: 10 "Alta", 5 "Media", 1 "Bassa")
- **peso**: FloatField

### Corriere

- **id_corriere**: AutoField (PK)
- **nome**: CharField (max_length=100)
- **capacità_massima**: IntegerField
- **posizione_attuale**: CharField (max_length=100, default="Non specificata")

### Veicolo

- **id_veicolo**: AutoField (PK)
- **Codice_Corriere**: IntegerField (collega a id_corriere di Corriere)
- **capacità_massima**: IntegerField
- **Targa_mezzo**: CharField

## classe funzionale al progetto

### Consegna

- **id_consegna**: AutoField (PK)
- **id_ordine**: ForeignKey su Ordine
- **id_corriere**: ForeignKey su Corriere
- **id_veicolo**: ForeignKey su Veicolo

---

## Funzionalità

---

- Gestione ordini e stato avanzamento
- Assegnazione corrieri e veicoli
- Dashboard con statistiche
- Interfaccia admin Django (interfaccia html personalizzata)

---

## Requisiti Non Funzionali

---

1. **Scalabilità**  
   Il sistema deve poter gestire almeno 10.000 ordini simultanei.
2. **Prestazioni**  
   La funzione di assegnazione deve rispondere entro 2 secondi dall’inserimento di un nuovo ordine.
3. **Interfaccia Utente**  
   Interfaccia web semplice ed efficace con dashboard in tempo reale.

---

## Avvio rapido

1. Installa le dipendenze:
   ```
   pip install django
   ```
2. Applica le migrazioni:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Crea un superuser:
   ```
   python manage.py createsuperuser
   ```
4. Avvia il server:
   ```
   python manage.py runserver
   ```
5. Accedi a:
   - Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)
   - Dashboard: [http://localhost:8000/home](http://localhost:8000/home)
   - Ordini: [http://localhost:8000/lista_ordini/](http://localhost:8000/lista_ordini/)
   - Corrieri: [http://localhost:8000/corriere/](http://localhost:8000/corriere/)
   - Veicoli: [http://localhost:8000/veicolo/](http://localhost:8000/veicolo/)
   - API : [http://localhost:8000/api/](http://localhost:8000/api/)

---

## Modello Logico

| Tabella  | Attributi                                                      | Chiavi Primarie (PK) | Chiavi Esterne (FK)                    |
| -------- | -------------------------------------------------------------- | -------------------- | -------------------------------------- |
| Ordine   | id_ordine, data_e_ora_ordine, indirizzo, stato, priorita, peso | id_ordine            | -                                      |
| Corriere | id_corriere, nome, capacità_massima, posizione_attuale         | id_corriere          | -                                      |
| Veicolo  | id_veicolo, Codice_Corriere, capacità_massima, Targa_mezzo     | id_veicolo           | Codice_Corriere → Corriere.id_corriere |
| Consegna | id_consegna, id_ordine, id_corriere, id_veicolo                | id_consegna          | id_ordine, id_corriere, id_veicolo     |

**Relazioni:**

- Ogni **Consegna** è collegata a un solo **Ordine**, un solo **Corriere** e un solo **Veicolo** tramite chiavi esterne.
- Un **Ordine** può essere associato a più **Consegne** (relazione 1:N).
- Un **Corriere** può essere associato a più **Consegne** (relazione 1:N).
- Un **Veicolo** può essere associato a più **Consegne** (relazione 1:N).

## Modello ER

[Ordine] 1---N [Consegna] N---1 [Corriere]
| |
| |
+-------N---1------+
|
[Veicolo]

---
## Modello UML


[Ordine] 1---N [Consegna] N---1 [Corriere]
   |                             |
   |                             |
   +----------N---1-------------+
                |
            [Veicolo]



[User]

id_user : AutoField

nome : CharField

cognome : CharField

email : EmailField

password : CharField

ruolo : CharField

[Ordine]

id_ordine : AutoField

data_e_ora_ordine : DateField

indirizzo : CharField

stato : CharField

priorita : IntegerField

peso : FloatField

volume : FloatField

latitudine : FloatField

longitudine : FloatField

[Corriere]

id_corriere : AutoField

nome : CharField

capacità_massima : IntegerField

posizione_attuale : CharField

latitudine : FloatField

longitudine : FloatField

[Veicolo]

id_veicolo : AutoField

Codice_Corriere : CharField

capacità_massima : IntegerField

Targa_mezzo : CharField

[Consegna]

id_consegna : AutoField

id_ordine → Ordine (FK)

id_corriere → Corriere (FK)

id_veicolo → Veicolo (FK)

[NotificaConsegna]

ordine_id : IntegerField

indirizzo : TextField

data_consegna : DateTimeField

corriere : CharField

ricevuta_il : DateTimeField

## Conclusione

Ordine, Corriere e Veicolo sono entità principali.

Consegna è una entità ponte che mette in relazione gli altri tre.

User e NotificaConsegna sono entità di supporto:

User per autenticazione/ruoli,

NotificaConsegna per registrare eventi legati alle consegne.


## API

L'API è stata implementata utilizzando Django Rest Framework.

### Endpoints principali

| Metodo | Endpoint            | Descrizione               |
| ------ | ------------------- | ------------------------- |
| GET    | /api/ordini/        | Lista tutti gli ordini    |
| POST   | /api/ordini/        | Crea un nuovo ordine      |
| GET    | /api/ordini/{id}/   | Dettaglio di un ordine    |
| PUT    | /api/ordini/{id}/   | Modifica un ordine        |
| DELETE | /api/ordini/{id}/   | Elimina un ordine         |
| GET    | /api/corrieri/      | Lista tutti i corrieri    |
| POST   | /api/corrieri/      | Crea un nuovo corriere    |
| GET    | /api/corrieri/{id}/ | Dettaglio di un corriere  |
| PUT    | /api/corrieri/{id}/ | Modifica un corriere      |
| DELETE | /api/corrieri/{id}/ | Elimina un corriere       |
| GET    | /api/veicoli/       | Lista tutti i veicoli     |
| POST   | /api/veicoli/       | Crea un nuovo veicolo     |
| GET    | /api/veicoli/{id}/  | Dettaglio di un veicolo   |
| PUT    | /api/veicoli/{id}/  | Modifica un veicolo       |
| DELETE | /api/veicoli/{id}/  | Elimina un veicolo        |
| GET    | /api/consegne/      | Lista tutte le consegne   |
| POST   | /api/consegne/      | Crea una nuova consegna   |
| GET    | /api/consegne/{id}/ | Dettaglio di una consegna |
| PUT    | /api/consegne/{id}/ | Modifica una consegna     |
| DELETE | /api/consegne/{id}/ | Elimina una consegna      |

## Webhook
django signal:

spiegazione visuale del funzionamento: 
Sequence Diagram: Notifica Webhook al Corriere

+--------+          +--------+           +---------------------+
| Django |          | Signal |           | Webhook (Corriere)  |
+--------+          +--------+           +---------------------+
    |                   |                          |
    | Salvataggio       |                          |
    | oggetto Consegna  |                          |
    |------------------>|                          |
    |                   | post_save (created=True) |
    |                   |------------------------->|
    |                   | Recupera dati consegna   |
    |                   | e corriere               |
    |                   |------------------------->|
    |                   |  HTTP POST con JSON      |
    |                   |  (ordine, indirizzo...)  |
    |                   |------------------------->|
    |                   |                          |
    |                   |     200 OK / Risposta    |
    |                   |<-------------------------|
    |                   |                          |

# riassunto funzionamento webhook
Crea un evento: 
Quando una consegna (Consegna) viene creata

Azione automatica:

Inviare una richiesta HTTP (webhook) al corriere
di avenuta consegna.


> **Nota:**  
> Gli endpoint possono variare in base alla configurazione delle tue `urls.py` e dei tuoi `ViewSet`/`Router`.

## Requisiti Non Funzionali

1. Scalabilità

Requisito: Il sistema deve poter gestire almeno 10.000 ordini simultanei.

Soluzioni:

Architettura scalabile: Usare un'architettura a microservizi o modulare che consenta di distribuire il carico su più server.

Database ottimizzato:

Indici adeguati sulle tabelle per velocizzare le query (es. su stato, priorità, id_corriere).

Utilizzo di database relazionali scalabili ( Database non realazionali come MongoDB,  ).

2. Prestazioni

Requisito: La funzione di assegnazione deve rispondere entro 2 secondi dall’inserimento di un nuovo ordine.

Soluzioni:

Elaborazione asincrona:

Non eseguire la funzione di assegnazione direttamente durante la richiesta HTTP, ma spostarla in un task asincrono (Celery, RQ).

Così la risposta all’utente è immediata e la funzione di assegnazione viene eseguita in background.

Ottimizzazione query:

Minimizzare le query al DB: usare select_related, prefetch_related per ridurre il numero di query.

Usare indici e filtri precisi per recuperare solo i dati necessari.

Caching:

Cache temporanea di dati statici (es. lista corrieri e veicoli) per ridurre accessi al DB.

Profiling e tuning:

Monitorare le performance con strumenti di profiling (Django Debug Toolbar, NewRelic) per identificare colli di bottiglia e ottimizzare il codice.

Pre-calcolo:

Se possibile, calcolare o aggiornare anticipatamente dati utili (es. capacità residua dei corrieri) e memorizzarli in cache o in colonne dedicate.











3. Interfaccia Utente
Requisito: Creare un'interfaccia web semplice ed efficace con una vista dashboard che permetta di visualizzare dati in tempo reale.

Soluzioni:

## Framework frontend semplice e reattivo:

Usare React, Vue.js o anche un framework più leggero come HTMX + Django Templates per ridurre la complessità.

## Dashboard intuitiva:

Visualizzare indicatori chiave (numero ordini attivi, ordini assegnati, capacità corrieri) con grafici o tabelle aggiornate.

## Aggiornamenti in tempo reale:

Utilizzare WebSocket (es. Django Channels) o polling periodico per aggiornare i dati in tempo reale senza ricaricare la pagina.

## Design responsive:

Garantire fruibilità su desktop e mobile con layout responsive (es. Bootstrap, Tailwind CSS).

## Filtri e ricerche:

Permettere all’utente di filtrare ordini per stato, priorità, corriere, ecc., per rendere più facile la gestione.

## User experience:

Minimizzare i passaggi per compiere azioni, usare notifiche per aggiornamenti importanti, e mantenere l’interfaccia pulita e leggibile.