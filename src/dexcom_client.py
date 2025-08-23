"""
Glik - A Nightscout desktop viewer
Copyright (C) 2025 Emmanuele Pani

Client per la connessione a Dexcom Share API
"""

import sys
import os
from datetime import datetime
from typing import Optional, Dict, Any

try:
    from pydexcom import Dexcom, Region
    PYDEXCOM_AVAILABLE = True
except ImportError:
    PYDEXCOM_AVAILABLE = False
    print("pydexcom non disponibile. Installa con: pip install pydexcom")

class DexcomClient:
    """Client per la connessione a Dexcom Share API"""
    
    def __init__(self, username: str = "", password: str = "", region: str = "ous"):
        """
        Inizializza il client Dexcom
        
        Args:
            username: Username, email o numero di telefono Dexcom
            password: Password Dexcom
            region: Regione ('us', 'ous', 'jp')
        """
        self.username = username
        self.password = password
        self.region = region
        self.dexcom = None
        self.connected = False
        self.last_error = None
        
        if not PYDEXCOM_AVAILABLE:
            self.last_error = "pydexcom non disponibile"
            return
            
        self._connect()
    
    def _connect(self):
        """Tenta la connessione a Dexcom"""
        try:
            if not self.username or not self.username.strip() or not self.password or not self.password.strip():
                self.last_error = "Username e password non possono essere vuoti"
                return False
            
            # Valida la regione
            valid_regions = ["OUS", "US", "JP"]
            if self.region.upper() not in valid_regions:
                self.last_error = f"Regione non valida '{self.region}'. Regioni valide: {', '.join(valid_regions)}"
                return False
            
            # Valida il formato dell'username (email, telefono o username)
            username = self.username.strip()
            if "@" in username:
                # Email
                if not username.count("@") == 1 or not "." in username.split("@")[1]:
                    self.last_error = "Formato email non valido"
                    return False
            elif username.startswith("+") and username[1:].isdigit():
                # Numero di telefono
                if len(username) < 10:
                    self.last_error = "Numero di telefono troppo corto"
                    return False
            elif len(username) < 3:
                # Username
                self.last_error = "Username troppo corto (minimo 3 caratteri)"
                return False
            
            # Valida la password
            password = self.password.strip()
            if len(password) < 6:
                self.last_error = "Password troppo corta (minimo 6 caratteri)"
                return False
            
            # Verifica che non ci siano caratteri non validi nelle credenziali
            import re
            if re.search(r'[<>"\']', username) or re.search(r'[<>"\']', password):
                self.last_error = "Credenziali contengono caratteri non validi (<, >, \", ')"
                return False
            
            # Verifica che le credenziali non siano troppo lunghe
            if len(username) > 100 or len(password) > 100:
                self.last_error = "Credenziali troppo lunghe (massimo 100 caratteri)"
                return False
            
            # Verifica che le credenziali non contengano solo spazi o caratteri di controllo
            if username.isspace() or password.isspace():
                self.last_error = "Credenziali non possono contenere solo spazi"
                return False
            
            # Verifica che le credenziali non contengano caratteri di controllo
            if any(ord(c) < 32 for c in username + password):
                self.last_error = "Credenziali contengono caratteri di controllo non validi"
                return False
            
            # Verifica che le credenziali non contengano caratteri non stampabili
            if not username.isprintable() or not password.isprintable():
                self.last_error = "Credenziali contengono caratteri non stampabili"
                return False
            
            # Verifica che le credenziali non contengano caratteri di escape
            if "\\" in username or "\\" in password:
                self.last_error = "Credenziali non possono contenere caratteri di escape (\\)"
                return False
            
            # Converti la regione in enum
            region_enum = getattr(Region, self.region.upper(), Region.OUS)
            
            print(f"Tentativo di connessione a Dexcom con regione: {self.region.upper()}")
            
            # Crea la connessione
            self.dexcom = Dexcom(
                username=self.username,
                password=self.password,
                region=region_enum
            )
            
            # Testa la connessione
            print("Test connessione Dexcom...")
            reading = self.dexcom.get_current_glucose_reading()
            print(f"Connessione riuscita! Lettura: {reading.value} mg/dL")
            
            self.connected = True
            self.last_error = None
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"Errore connessione Dexcom: {error_msg}")
            
            # Fornisci messaggi di errore più specifici
            if "authentication" in error_msg.lower() or "login" in error_msg.lower():
                self.last_error = f"Credenziali non valide: {error_msg}"
            elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                self.last_error = f"Problema di connessione: {error_msg}"
            elif "region" in error_msg.lower():
                self.last_error = f"Regione non valida '{self.region}'. Prova: ous, us, jp"
            else:
                self.last_error = f"Errore Dexcom: {error_msg}"
            
            self.connected = False
            return False
    
    def get_current_glucose(self) -> Optional[Dict[str, Any]]:
        """
        Ottiene la lettura glicemica corrente
        
        Returns:
            Dizionario con i dati glicemici o None se errore
        """
        if not self.connected or not self.dexcom:
            if not self._connect():
                return None
        
        try:
            print("Richiesta lettura glicemica corrente da Dexcom...")
            reading = self.dexcom.get_current_glucose_reading()
            
            if not reading:
                self.last_error = "Nessuna lettura glicemica corrente disponibile"
                print("Nessuna lettura corrente disponibile")
                return None
            
            print(f"Lettura corrente ricevuta: {reading.value} mg/dL")
            
            # Converti in formato compatibile con Nightscout
            glucose_data = {
                "sgv": reading.value,  # Valore in mg/dL
                "direction": reading.trend_direction,  # Direzione trend
                "trend": reading.trend,  # Trend numerico
                "trend_arrow": reading.trend_arrow,  # Freccia trend
                "trend_description": reading.trend_description,  # Descrizione trend
                "dateString": reading.datetime.isoformat(),  # Timestamp
                "delta": 0,  # Dexcom non fornisce delta, calcoleremo
                "mmol_l": reading.mmol_l  # Valore in mmol/L
            }
            
            return glucose_data
            
        except Exception as e:
            error_msg = str(e)
            print(f"Errore nel recuperare lettura corrente: {error_msg}")
            
            # Fornisci messaggi di errore più specifici
            if "authentication" in error_msg.lower() or "login" in error_msg.lower():
                self.last_error = f"Credenziali scadute o non valide: {error_msg}"
            elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                self.last_error = f"Problema di connessione: {error_msg}"
            elif "no data" in error_msg.lower() or "empty" in error_msg.lower():
                self.last_error = "Nessun dato glicemico disponibile al momento"
            else:
                self.last_error = f"Errore nel recuperare dati: {error_msg}"
            
            self.connected = False
            return None
    
    def get_glucose_history(self, count: int = 2) -> Optional[list]:
        """
        Ottiene la cronologia delle letture glicemiche
        
        Args:
            count: Numero di letture da recuperare
            
        Returns:
            Lista di letture glicemiche o None se errore
        """
        if not self.connected or not self.dexcom:
            if not self._connect():
                return None
        
        try:
            print(f"Richiesta {count} letture glicemiche da Dexcom...")
            # Ottieni tutte le letture disponibili e poi limita il numero
            readings = self.dexcom.get_glucose_readings()
            
            # Limita il numero di letture se necessario
            if readings and len(readings) > count:
                readings = readings[:count]
            
            if not readings:
                self.last_error = "Nessuna lettura glicemica disponibile da Dexcom"
                print("Nessuna lettura glicemica disponibile")
                return None
            
            print(f"Ricevute {len(readings)} letture da Dexcom (richieste: {count})")
            
            glucose_list = []
            for reading in readings:
                glucose_data = {
                    "sgv": reading.value,
                    "direction": reading.trend_direction,
                    "trend": reading.trend,
                    "trend_arrow": reading.trend_arrow,
                    "trend_description": reading.trend_description,
                    "dateString": reading.datetime.isoformat(),
                    "delta": 0,
                    "mmol_l": reading.mmol_l
                }
                glucose_list.append(glucose_data)
            
            # Calcola delta se abbiamo almeno 2 letture
            if len(glucose_list) >= 2:
                glucose_list[0]["delta"] = glucose_list[0]["sgv"] - glucose_list[1]["sgv"]
            
            return glucose_list
            
        except Exception as e:
            error_msg = str(e)
            print(f"Errore nel recuperare dati glicemici: {error_msg}")
            
            # Fornisci messaggi di errore più specifici
            if "authentication" in error_msg.lower() or "login" in error_msg.lower():
                self.last_error = f"Credenziali scadute o non valide: {error_msg}"
            elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                self.last_error = f"Problema di connessione: {error_msg}"
            elif "no data" in error_msg.lower() or "empty" in error_msg.lower():
                self.last_error = "Nessun dato glicemico disponibile al momento"
            else:
                self.last_error = f"Errore nel recuperare dati: {error_msg}"
            
            self.connected = False
            return None
    
    def is_available(self) -> bool:
        """Verifica se pydexcom è disponibile"""
        return PYDEXCOM_AVAILABLE
    
    def get_status(self) -> Dict[str, Any]:
        """Restituisce lo stato della connessione"""
        return {
            "connected": self.connected,
            "available": self.is_available(),
            "error": self.last_error,
            "username": self.username,
            "region": self.region
        }
    
    def update_credentials(self, username: str, password: str, region: str):
        """Aggiorna le credenziali e riconnette"""
        self.username = username
        self.password = password
        self.region = region
        self._connect()
    
    def disconnect(self):
        """Disconnette dal servizio Dexcom"""
        self.dexcom = None
        self.connected = False
        self.last_error = None
