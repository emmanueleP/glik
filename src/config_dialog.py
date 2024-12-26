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

from PyQt5.QtWidgets import (QDialog, QLineEdit, QPushButton, QFormLayout, 
                            QHBoxLayout, QTabWidget, QWidget, QSpinBox, QLabel,
                            QCheckBox)
from PyQt5.QtGui import QIcon
import winreg
import os
import sys

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurazione Glik")
        self.setWindowIcon(QIcon("src/assets/logo_glik.png"))
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: white;
            }
            QLabel {
                color: white;
            }
            QLineEdit, QSpinBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: white;
                padding: 8px 12px;
                border: 1px solid #3d3d3d;
            }
            QTabBar::tab:selected {
                background-color: #3d3d3d;
            }
        """)
        
        # Tab widget
        tab_widget = QTabWidget()
        
        # Tab Connessione
        connection_tab = QWidget()
        connection_layout = QFormLayout()
        
        self.url_input = QLineEdit()
        self.token_input = QLineEdit()
        self.sha1_input = QLineEdit()
        
        connection_layout.addRow("URL Nightscout:", self.url_input)
        connection_layout.addRow("API Secret Token:", self.token_input)
        connection_layout.addRow("API Secret SHA1:", self.sha1_input)
        connection_tab.setLayout(connection_layout)
        
        # Tab Impostazioni
        settings_tab = QWidget()
        settings_layout = QFormLayout()
        
        self.refresh_interval = QSpinBox()
        self.refresh_interval.setMinimum(10)  # Minimo 10 secondi
        self.refresh_interval.setMaximum(300)  # Massimo 5 minuti
        self.refresh_interval.setSuffix(" secondi")
        self.refresh_interval.setToolTip("Intervallo di aggiornamento (10-300 secondi)")
        
        refresh_note = QLabel("Nota: Un intervallo troppo breve potrebbe causare problemi di performance")
        refresh_note.setStyleSheet("color: #888888; font-size: 10px;")
        
        settings_layout.addRow("Intervallo di refresh:", self.refresh_interval)
        settings_layout.addRow("", refresh_note)
        
        # Nuove opzioni
        self.autostart = QCheckBox("Avvia all'avvio di Windows")
        self.minimize_to_tray = QCheckBox("Minimizza nel system tray invece di chiudere")
        
        settings_layout.addRow(self.autostart)
        settings_layout.addRow(self.minimize_to_tray)
        
        settings_tab.setLayout(settings_layout)
        
        # Aggiungi tabs
        tab_widget.addTab(connection_tab, "Connessione")
        tab_widget.addTab(settings_tab, "Impostazioni")
        
        # Layout principale
        main_layout = QFormLayout()
        main_layout.addRow(tab_widget)
        
        # Pulsanti
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Salva")
        cancel_button = QPushButton("Annulla")
        
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        main_layout.addRow(buttons_layout)
        self.setLayout(main_layout)
        
    def get_config(self):
        config = {
            "nightscout_url": self.url_input.text().strip(),
            "api_secret": self.token_input.text().strip(),
            "api_secret_sha1": self.sha1_input.text().strip(),
            "refresh_interval": self.refresh_interval.value(),
            "minimize_to_tray": self.minimize_to_tray.isChecked(),
            "autostart": self.autostart.isChecked()
        }
        
        # Gestisci l'autostart
        self.manage_autostart(config["autostart"])
        
        return config
        
    def set_config(self, config):
        self.url_input.setText(config.get("nightscout_url", ""))
        self.token_input.setText(config.get("api_secret", ""))
        self.sha1_input.setText(config.get("api_secret_sha1", ""))
        self.refresh_interval.setValue(config.get("refresh_interval", 30))
        self.minimize_to_tray.setChecked(config.get("minimize_to_tray", True))
        self.autostart.setChecked(config.get("autostart", False))

    def manage_autostart(self, enable):
        app_path = os.path.abspath(sys.argv[0])
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                              winreg.KEY_ALL_ACCESS) as key:
                if enable:
                    winreg.SetValueEx(key, "Glik", 0, 
                                    winreg.REG_SZ, f'"{app_path}" --minimized')
                else:
                    try:
                        winreg.DeleteValue(key, "Glik")
                    except:
                        pass
        except Exception as e:
            print(f"Errore nella gestione dell'autostart: {e}") 