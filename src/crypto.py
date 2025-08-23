"""
Glik - A Nightscout desktop viewer
Copyright (C) 2025 Emmanuele Pani
"""

from cryptography.fernet import Fernet
import base64
import os
import sys
import json
from pathlib import Path

class ConfigCrypto:
    def __init__(self):
        self.key = self._get_or_create_key()
        self.cipher_suite = Fernet(self.key)
    
    def _get_or_create_key(self):
        """Ottiene o crea una chiave di cifratura nella directory APPDATA"""
        key_file = Path(self._get_app_path()) / ".glik_key"
        
        if key_file.exists():
            with open(key_file, "rb") as f:
                return f.read()
        else:
            # Genera una nuova chiave
            key = Fernet.generate_key()
            # Salva la chiave
            key_file.parent.mkdir(parents=True, exist_ok=True)
            with open(key_file, "wb") as f:
                f.write(key)
            return key
    
    def _get_app_path(self):
        """Ottiene il percorso per salvare i file di configurazione e chiavi"""
        # Usa sempre APPDATA per i file di configurazione e chiavi
        appdata_path = os.path.join(os.getenv('APPDATA'), 'Glik')
        # Crea la directory se non esiste
        os.makedirs(appdata_path, exist_ok=True)
        return appdata_path
    
    def encrypt_config(self, config_data):
        """Cifra i dati di configurazione"""
        json_str = json.dumps(config_data)
        encrypted_data = self.cipher_suite.encrypt(json_str.encode())
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt_config(self, encrypted_data):
        """Decifra i dati di configurazione"""
        try:
            # Prima prova a vedere se è un JSON non cifrato
            try:
                return json.loads(encrypted_data)
            except json.JSONDecodeError:
                pass
            
            # Se non è JSON, prova a decifrare
            encrypted_data = encrypted_data.strip()
            padding = len(encrypted_data) % 4
            if padding:
                encrypted_data += '=' * (4 - padding)
                
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
            return json.loads(decrypted_data)
        except Exception as e:
            if __debug__:
                print(f"Errore decifratura: {e}")
                print(f"Dati ricevuti: {encrypted_data}")
            return None

    def migrate_config(self, config_path):
        """Migra un file di configurazione non cifrato a cifrato"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Cifra e salva
            encrypted = self.encrypt_config(config)
            with open(config_path, 'w') as f:
                f.write(encrypted)
            return True
        except Exception as e:
            if __debug__:
                print(f"Errore migrazione: {e}")
            return False 