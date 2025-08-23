# 🩺 Glik - Blood Sugar Viewer

![Glik Logo](src/assets/logo_glik.png)

## 📝 Description
Glik is a Windows desktop viewer that allows you to monitor blood glucose data from Nightscout or directly from Dexcom Share. As a Type 1 diabetic, I've created this app to help me and others keep track of their glucose levels even on Windows.

## 📝 Descrizione
Glik è un visualizzatore desktop per Windows che permette di monitorare i dati della glicemia da Nightscout o direttamente da Dexcom Share. Essendo diabetico tipo 1, ho creato questa app per aiutare me e altri a tenere traccia dei loro livelli di glicemia anche su Windows.

## ⚡ Main Features / Caratteristiche Principali
- 🔄 Automatic data updates (configurable) / Aggiornamento automatico dei dati (configurabile)
- 🎨 Dark mode interface / Interfaccia dark mode
- 🔔 System tray display / Visualizzazione nella system tray
- 🚀 Windows autostart / Avvio automatico con Windows
- 🔒 API Secret support / Supporto per API Secret
- 🔑 Encryption of the API/ Cifratura dell'API
- 📱 **NEW: Dexcom Share support** / **NUOVO: Supporto Dexcom Share**
- 🔄 **NEW: Dual connection modes** / **NUOVO: Modalità di connessione doppia**
- ✅ **FIXED: Permission issues resolved** / **RISOLTO: Problemi di permessi risolti**
- ✅ **FIXED: Configuration persistence** / **RISOLTO: Persistenza configurazione** 

## 📥 Download
- [⬇️ Download Glik v1.0.6 / Scarica Glik v1.0.6](https://github.com/emmanueleP/glik/releases/download/v1.0.6/Glik_Setup.exe)
- ✅ **Latest version fixes permission issues and configuration persistence** / **L'ultima versione risolve i problemi di permessi e la persistenza della configurazione**

## 🖥️ System Requirements / Requisiti di Sistema
- Windows 10/11 (64-bit)
- 100MB disk space / spazio su disco
- 2GB RAM
- Internet connection / Connessione Internet
- **Option 1**: [Nightscout site](https://nightscout.github.io/) configured and working / configurato e funzionante
- **Option 2**: Dexcom account with Share service enabled / Account Dexcom con servizio Share abilitato

## 🛠️ Installation / Installazione
1. Download the executable / Scarica l'eseguibile
2. Run `Glik.exe` / Esegui il file `Glik.exe`
3. On first launch, choose your connection type and enter credentials / Al primo avvio, scegli il tipo di connessione e inserisci le credenziali:
   - **Nightscout**: URL del sito e API Secret
   - **Dexcom Share**: Username/email e password Dexcom
4. The app will start in the system tray / L'app si avvierà nella system tray

## 🎯 Usage / Utilizzo
- Double click on the system tray icon to open the main window / Doppio click sull'icona nella system tray per aprire la finestra principale
- Right click on the icon to access the context menu / Click destro sull'icona per accedere al menu contestuale
- `R` to manually refresh data / per aggiornare manualmente i dati
- `Ctrl+Q` to completely close the application / per chiudere completamente l'applicazione

## 🎨 Color Legend / Legenda Colori
- 🟢 Green/Verde: In range glucose (70-180 mg/dL) / Glicemia in range
- 🔴 Red/Rosso: High glucose (>180 mg/dL) / Glicemia alta
- 🟡 Orange/Arancione: Low glucose (<70 mg/dL) / Glicemia bassa

## 🔧 Recent Fixes / Correzioni Recenti
### ✅ v1.0.6 - Permission Issues Resolved / Problemi di Permessi Risolti
- **Fixed**: Permission denied errors when saving configuration in compiled exe
- **Fixed**: Configuration not persisting between app launches
- **Fixed**: API keys not being saved correctly
- **Solution**: All configuration files now saved in `%APPDATA%\Glik` instead of Program Files
- **Benefit**: App now works correctly when installed in C:\Program Files\Glik

### ✅ v1.0.5 - Auto-start and Configuration
- **Fixed**: Windows auto-start not working properly
- **Fixed**: Configuration migration from legacy paths
- **Added**: Better error handling and user feedback

## 👨‍💻 Development 
- [Glik on GitHub](https://github.com/emmanueleP/glik)
- [Glik on GitHub Releases](https://github.com/emmanueleP/glik/releases)
- [Report Issues](https://github.com/emmanueleP/glik/issues) / [Segnala Problemi](https://github.com/emmanueleP/glik/issues)

### 🚀 Current Status / Stato Attuale
- ✅ **Windows**: Fully functional with all recent fixes / Completamente funzionale con tutte le correzioni recenti
- 🔄 **macOS**: In development / In sviluppo





