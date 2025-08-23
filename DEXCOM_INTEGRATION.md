# Integrazione Dexcom Share - Glik

## Panoramica

Glik ora supporta due tipi di connessione per ottenere i dati glicemici:

1. **Nightscout** - Connessione al tuo server Nightscout esistente
2. **Dexcom Share** - Connessione diretta al servizio Dexcom Share

## Connessione Dexcom Share

### Prerequisiti

- Account Dexcom attivo con servizio Share abilitato
- Almeno un follower configurato nel servizio Share
- Pacchetto Python `pydexcom` installato

### Installazione

```bash
pip install pydexcom
```

### Configurazione

1. Apri Glik e vai su **Strumenti > Impostazioni**
2. Seleziona **"Dexcom Share"** come tipo di connessione
3. Inserisci le tue credenziali Dexcom:
   - **Username/Email/Telefono**: Il tuo username Dexcom, email o numero di telefono
   - **Password**: La tua password Dexcom
   - **Regione**: Seleziona la tua regione
     - **OUS**: Europa e resto del mondo
     - **US**: Stati Uniti
     - **JP**: Giappone

### Formati Username

- **Email**: `user@example.com`
- **Telefono**: `+1234567890` (con prefisso internazionale)
- **Username**: `username`

### Note Importanti

- **Non usare le credenziali del follower**: Usa le tue credenziali Dexcom, non quelle di chi ti segue
- **Servizio Share richiesto**: Devi avere almeno un follower nel servizio Share per abilitare l'API
- **Credenziali valide**: Verifica che le tue credenziali funzionino sul sito Dexcom Account Management

## Vantaggi Dexcom Share

### Rispetto a Nightscout
- **Setup più semplice**: Non richiede configurazione di un server
- **Aggiornamenti in tempo reale**: Dati direttamente da Dexcom
- **Meno latenza**: Nessun server intermedio
- **Meno manutenzione**: Non devi gestire un server Nightscout

### Limitazioni
- **Dipendenza da Dexcom**: Se Dexcom cambia l'API, potrebbe richiedere aggiornamenti
- **Solo dati glicemici**: Non include altri dati come insulina, carboidrati, ecc.
- **Richiede account Dexcom**: Non funziona con altri CGM

## Risoluzione Problemi

### Errore "pydexcom non disponibile"
```bash
pip install pydexcom
```

### Errore "Invalid password"
- Verifica le tue credenziali Dexcom
- Assicurati di usare le tue credenziali, non quelle del follower
- Controlla la regione selezionata
- Verifica che il servizio Share sia abilitato

### Errore "Account not found"
- Verifica il formato dell'username
- Per i numeri di telefono, usa il formato internazionale (+1234567890)
- Prova a usare il tuo Account ID invece dell'username

### Errore di connessione
- Verifica la tua connessione internet
- Controlla che Dexcom non sia in manutenzione
- Prova a riavviare l'applicazione

## Migrazione da Nightscout

Se hai già una configurazione Nightscout:

1. Apri **Strumenti > Impostazioni**
2. Cambia il tipo di connessione in **"Dexcom Share"**
3. Inserisci le tue credenziali Dexcom
4. Salva la configurazione

La tua configurazione Nightscout rimarrà salvata e potrai tornare ad essa in qualsiasi momento.

## Supporto Tecnico

### Log dell'applicazione
Glik mostra messaggi di errore dettagliati nella console. Se hai problemi:

1. Avvia Glik da terminale/prompt comandi
2. Controlla i messaggi di errore
3. Fornisci questi messaggi quando richiedi supporto

### Risorse Utili
- [Documentazione pydexcom](https://gagebenne.github.io/pydexcom/pydexcom.html)
- [Repository pydexcom](https://github.com/gagebenne/pydexcom)
- [Dexcom Account Management](https://uam2.dexcom.com) (per utenti OUS)

## Sicurezza

- Le credenziali Dexcom vengono salvate in modo cifrato
- I dati vengono trasmessi direttamente tra Glik e Dexcom
- Nessun dato viene inviato a server terzi
- Le credenziali sono salvate localmente nel tuo computer

## Aggiornamenti

Quando aggiorni Glik:

1. Le tue configurazioni esistenti vengono mantenute
2. Le nuove funzionalità Dexcom vengono aggiunte automaticamente
3. Puoi continuare a usare Nightscout se preferisci
