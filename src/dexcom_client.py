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
            if not self.username or not self.password:
                self.last_error = "Username e password richiesti"
                return False
                
            # Converti la regione in enum
            region_enum = getattr(Region, self.region.upper(), Region.OUS)
            
            # Crea la connessione
            self.dexcom = Dexcom(
                username=self.username,
                password=self.password,
                region=region_enum
            )
            
            # Testa la connessione
            self.dexcom.get_current_glucose_reading()
            self.connected = True
            self.last_error = None
            return True
            
        except Exception as e:
            self.last_error = str(e)
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
            reading = self.dexcom.get_current_glucose_reading()
            
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
            self.last_error = str(e)
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
            readings = self.dexcom.get_glucose_readings(min_count=count, max_count=count)
            
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
            self.last_error = str(e)
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
