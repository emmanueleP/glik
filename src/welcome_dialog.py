"""
Glik - A Nightscout desktop viewer
Copyright (C) 2025 Emmanuele Pani

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QFormLayout)
from PyQt5.QtCore import Qt
import json
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from .crypto import ConfigCrypto
from .resources import get_logo_path, get_icon_path

class WelcomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Benvenuto in Glik")
        self.setWindowIcon(QIcon(get_icon_path()))
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: white;
                min-width: 400px;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 8px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Logo
        logo_label = QLabel()
        logo = QPixmap(get_logo_path())
        logo_label.setPixmap(logo.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        # Messaggio di benvenuto
        welcome_label = QLabel(
            "Benvenuto in Glik!\n\n"
            "© 2025 - Emmanuele Pani. Under GNU AGPL v3.0\n\n"
            "Per iniziare, inserisci l'URL del tuo sito Nightscout "
            "e il token API Secret.\n"
            "Potrai modificare queste impostazioni in seguito dal menu Strumenti."
        )
        welcome_label.setWordWrap(True)
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Form per i dati
        form_layout = QFormLayout()
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://mio-sito.nightscout.org")
        
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("token-api-secret")
        
        form_layout.addRow("URL Nightscout:", self.url_input)
        form_layout.addRow("API Secret:", self.token_input)
        
        layout.addLayout(form_layout)
        
        # Pulsante di conferma
        save_button = QPushButton("Inizia")
        save_button.clicked.connect(self.accept)
        layout.addWidget(save_button)
    
    def get_config(self):
        import hashlib
        token = self.token_input.text().strip()
        return {
            "nightscout_url": self.url_input.text().strip(),
            "api_secret": token,
            "api_secret_sha1": hashlib.sha1(token.encode()).hexdigest(),
            "dark_mode": True,
            "minimize_to_tray": True,
            "refresh_interval": 30
        }

    @staticmethod
    def show_if_first_time():
        """Mostra il dialog solo se non esiste già un file di configurazione"""
        import sys
        import os.path
        
        crypto = ConfigCrypto()
        
        # Ottieni il percorso dell'eseguibile
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        config_path = os.path.join(application_path, "config.json")
        
        # Se esiste un file di configurazione, prova a migrarlo
        if os.path.exists(config_path):
            crypto.migrate_config(config_path)
            return False
            
        if not os.path.exists(config_path):
            default_config = {
                "nightscout_url": "",
                "api_secret": "",
                "api_secret_sha1": "",
                "dark_mode": True,
                "minimize_to_tray": True,
                "refresh_interval": 30,
                "autostart": False
            }
            
            # Cifra e salva la configurazione di default
            encrypted_config = crypto.encrypt_config(default_config)
            with open(config_path, "w") as f:
                f.write(encrypted_config)
            
            dialog = WelcomeDialog()
            if dialog.exec_() == QDialog.Accepted:
                config = dialog.get_config()
                # Cifra e salva la nuova configurazione
                encrypted_config = crypto.encrypt_config(config)
                with open(config_path, "w") as f:
                    f.write(encrypted_config)
                return True
        return False 