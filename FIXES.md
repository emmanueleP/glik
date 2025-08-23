# Correzioni Applicate - Glik

## Problemi Risolti

### 1. Configurazione non salvata ✅
**Problema**: L'applicazione non salvava più le API configurate in un file, costringendo l'utente a reinserire le credenziali ad ogni apertura.

**Causa**: Inconsistenza nei percorsi di salvataggio della configurazione. I metodi `show_config_dialog()` e `show_welcome()` salvavano in percorsi diversi da quello usato per il caricamento.

**Soluzione**: 
- Uniformato il percorso di salvataggio per usare sempre `%APPDATA%\Glik\config.json`
- Implementata migrazione automatica da configurazioni legacy
- Corretto il metodo `load_config()` per gestire meglio la migrazione
- Rimossa funzione `get_config_path()` non utilizzata

### 2. Avvio automatico non funzionante ✅
**Problema**: L'applicazione non si avviava automaticamente all'avvio di Windows.

**Causa**: Problemi nella gestione del Task Scheduler di Windows e percorsi non corretti.

**Soluzione**:
- Semplificato il comando di creazione del task
- Aggiunto fallback per la creazione del task
- Implementata verifica dello stato dell'avvio automatico
- Migliorata gestione degli errori

## Modifiche Tecniche

### File `src/gui.py`
- **Metodo `load_config()`**: Aggiunta migrazione automatica da configurazioni legacy
- **Metodo `show_config_dialog()`**: Corretto percorso di salvataggio per usare APPDATA
- **Metodo `show_welcome()`**: Uniformato percorso di salvataggio
- Rimossa funzione `get_config_path()` non utilizzata

### File `src/config_dialog.py`
- **Metodo `manage_autostart()`**: Semplificato e migliorato
- **Nuovo metodo `check_autostart_status()`**: Verifica lo stato attuale dell'avvio automatico
- Migliorata gestione degli errori

### File `src/crypto.py`
- Corretto percorso per la chiave di crittografia

## Come Testare

1. **Test configurazione**:
   - Avvia l'applicazione
   - Vai su Strumenti > Impostazioni
   - Inserisci le tue API Nightscout
   - Salva e riavvia l'app
   - Verifica che le configurazioni siano mantenute

2. **Test avvio automatico**:
   - Vai su Strumenti > Impostazioni
   - Spunta "Avvia all'avvio di Windows"
   - Salva
   - Riavvia Windows
   - Verifica che l'app si avvii automaticamente

## Note Importanti

- Le configurazioni vengono ora salvate in `%APPDATA%\Glik\config.json`
- La chiave di crittografia è salvata in `.glik_key` nella directory dell'applicazione
- L'avvio automatico usa il Task Scheduler di Windows per maggiore affidabilità
- È implementata migrazione automatica da configurazioni precedenti

## Risoluzione Problemi

Se l'avvio automatico non funziona:
1. Verifica che l'utente abbia i permessi per creare task pianificati
2. Controlla i log dell'applicazione per errori
3. Prova a disabilitare e riabilitare l'opzione

Se la configurazione non viene salvata:
1. Verifica i permessi di scrittura in `%APPDATA%\Glik`
2. Controlla che non ci siano errori di crittografia
3. Verifica che la directory esista

## Stato delle Correzioni

- ✅ **Configurazione**: Risolto - ora salva correttamente in APPDATA
- ✅ **Avvio automatico**: Risolto - ora funziona con Task Scheduler
- ✅ **Migrazione**: Implementata - configurazioni legacy migrate automaticamente
- ✅ **Percorsi**: Uniformati - tutti i metodi usano lo stesso percorso
