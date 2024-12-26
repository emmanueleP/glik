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

import json
import hashlib
from PyQt5.QtWidgets import (QMainWindow, QSystemTrayIcon, QAction, QMenu, QLabel, 
                            QVBoxLayout, QWidget, QStyle, QMessageBox, QDialog,
                            QFrame, QPushButton, QHBoxLayout,)
from PyQt5.QtGui import QIcon, QPalette, QColor, QKeySequence, QPixmap, QPainter, QFont
from PyQt5.QtCore import Qt, QTimer, QPoint
import requests
from .config_dialog import ConfigDialog
from .about_dialog import AboutDialog
from .welcome_dialog import WelcomeDialog
from .help_dialog import HelpDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Glik")
        self.resize(800, 600)
        
        # Imposta l'icona della finestra
        self.setWindowIcon(QIcon("src/assets/logo_glik.png"))
        
        # Inizializza la configurazione prima di tutto
        self.init_config()
        
        # Imposta tema scuro
        self.set_dark_theme()
        
        # Menu
        self.create_menu()
        
        # Layout principale con frame
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Frame per il valore glicemico
        glucose_frame = QFrame()
        glucose_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        glucose_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        glucose_layout = QVBoxLayout(glucose_frame)
        
        # Etichetta per il valore corrente
        self.glucose_label = QLabel("Caricamento...")
        self.glucose_label.setStyleSheet("""
            font-size: 72px;
            font-weight: bold;
            color: #ffffff;
            padding: 10px;
        """)
        self.glucose_label.setAlignment(Qt.AlignCenter)
        
        # Etichetta per il trend e il timestamp
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("""
            font-size: 16px;
            color: #cccccc;
            padding: 5px;
        """)
        self.info_label.setAlignment(Qt.AlignCenter)
        
        glucose_layout.addWidget(self.glucose_label)
        glucose_layout.addWidget(self.info_label)
        
        # Bottone di refresh
        self.refresh_button = QPushButton()
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                border-radius: 15px;
                padding: 8px;
                min-width: 30px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:disabled {
                background-color: #1d1d1d;
                border-color: #2d2d2d;
            }
        """)
        self.refresh_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.refresh_button.clicked.connect(self.fetch_glucose_data)
        self.refresh_button.setToolTip("Aggiorna dati (R)")
        
        # Layout per il bottone di refresh
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_button)
        
        # Aggiunta del bottone al layout principale
        glucose_layout.addLayout(button_layout)
        
        main_layout.addWidget(glucose_frame)
        self.setCentralWidget(main_widget)
        
        # Setup dell'autenticazione
        self.headers = {
            'api-secret': self.config.get('api_secret_sha1', ''),
            'Content-Type': 'application/json'
        }
        
        # Setup system tray (spostato qui)
        self.setup_system_tray()
        
        # Timer per aggiornamento dati
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_glucose_data)
        refresh_interval = self.config.get("refresh_interval", 30) * 1000
        self.timer.start(refresh_interval)
        
        # Primo caricamento dati
        self.fetch_glucose_data()
        
        # Mostra la finestra
        self.show()

    def init_config(self):
        """Inizializza la configurazione dell'app"""
        # Mostra il dialog di benvenuto se è la prima volta
        if WelcomeDialog.show_if_first_time():
            try:
                with open("src/config.json", "r") as f:
                    self.config = json.loads(f.read())
            except:
                self.config = {
                    "nightscout_url": "",
                    "api_secret": "",
                    "api_secret_sha1": "",
                    "dark_mode": True
                }
        else:
            try:
                with open("src/config.json", "r") as f:
                    self.config = json.loads(f.read())
            except:
                self.config = {
                    "nightscout_url": "",
                    "api_secret": "",
                    "api_secret_sha1": "",
                    "dark_mode": True
                }

    def create_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #2d2d2d;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #3d3d3d;
            }
        """)
        
        # Menu File
        file_menu = menubar.addMenu("File")
        file_menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
        """)
        
        # Azione Benvenuto
        welcome_action = QAction("Benvenuto", self)
        welcome_action.setShortcut(QKeySequence("Ctrl+E"))
        welcome_action.triggered.connect(self.show_welcome)
        file_menu.addAction(welcome_action)
        
        # Separatore
        file_menu.addSeparator()
        
        # Azione Esci
        exit_action = QAction("Esci", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.quit_application)
        file_menu.addAction(exit_action)
        
        # Menu Strumenti
        tools_menu = menubar.addMenu("Strumenti")
        tools_menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
        """)
        
        settings_action = QAction("Impostazioni", self)
        settings_action.triggered.connect(self.show_config_dialog)
        tools_menu.addAction(settings_action)
        
        # Menu Info
        info_menu = menubar.addMenu("Info")
        info_menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
        """)
        
        about_action = QAction("Informazioni", self)
        about_action.triggered.connect(self.show_about)
        info_menu.addAction(about_action)
        
        help_action = QAction("Aiuto", self)
        help_action.triggered.connect(self.show_help)
        info_menu.addAction(help_action)

    def set_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: white;
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
            QMessageBox {
                background-color: #2d2d2d;
                color: white;
            }
        """)

    def show_config_dialog(self):
        dialog = ConfigDialog(self)
        dialog.set_config(self.config)
        
        if dialog.exec_() == QDialog.Accepted:
            new_config = dialog.get_config()
            self.config.update(new_config)
            
            try:
                with open("src/config.json", "w") as f:
                    json.dump(self.config, f, indent=4)
                
                # Aggiorna gli headers
                self.headers = {
                    'api-secret': self.config['api_secret_sha1'],
                    'Content-Type': 'application/json'
                }
                
                # Aggiorna l'intervallo del timer
                self.timer.setInterval(new_config["refresh_interval"] * 1000)
                
                # Ricarica i dati
                self.fetch_glucose_data()
                
                QMessageBox.information(self, "Successo", "Configurazione salvata con successo!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore nel salvare la configurazione: {str(e)}")

    def setup_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # Menu contestuale per il tray
        tray_menu = QMenu()
        tray_menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
        """)
        
        show_action = QAction("Mostra", self)
        show_action.triggered.connect(self.show)
        
        settings_action = QAction("Impostazioni", self)
        settings_action.triggered.connect(self.show_config_dialog)
        
        quit_action = QAction("Esci", self)
        quit_action.triggered.connect(self.close)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(settings_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # Doppio click per mostrare la finestra
        self.tray_icon.activated.connect(self.on_tray_activated)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.activateWindow()

    def closeEvent(self, event):
        if self.config.get("minimize_to_tray", True) and self.tray_icon.isVisible():
            QMessageBox.information(self, "Glik",
                "L'applicazione continuerà a funzionare in background.\n"
                "Per chiuderla completamente, usa Ctrl+Q.")
            self.hide()
            event.ignore()
        else:
            event.accept()

    def update_tray_icon(self, glucose_value, trend, color, local_time):
        # Crea un'icona personalizzata con il valore glicemico
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Imposta il font con dimensione basata sul numero di cifre
        font = QFont()
        text = str(glucose_value)
        if len(text) <= 2:
            font.setPointSize(32)  # Aumentato significativamente per numeri a 1-2 cifre
        elif len(text) == 3:
            font.setPointSize(26)  # Aumentato significativamente per numeri a 3 cifre
        else:
            font.setPointSize(20)  # Aumentato per numeri più lunghi
            
        font.setBold(True)
        painter.setFont(font)
        
        # Calcola il rettangolo del testo
        text_rect = painter.fontMetrics().boundingRect(text)
        
        # Calcola il fattore di scala per adattare il testo mantenendo le proporzioni
        scale_w = 31.0 / text_rect.width()   # Usa quasi tutto lo spazio disponibile
        scale_h = 31.0 / text_rect.height()  # Usa quasi tutto lo spazio disponibile
        scale = min(scale_w, scale_h)  # Usa il fattore più piccolo per mantenere le proporzioni
        
        # Applica la trasformazione
        painter.translate(16, 16)  # Sposta al centro
        painter.scale(scale, scale)  # Scala il testo
        painter.translate(-text_rect.width()/2, text_rect.height()/2)  # Centra il testo
        
        # Disegna il valore
        painter.setPen(QColor(color))
        painter.drawText(0, 0, text)
        
        painter.end()
        
        # Imposta l'icona
        self.tray_icon.setIcon(QIcon(pixmap))
        
        # Aggiorna il tooltip
        self.tray_icon.setToolTip(f"Glicemia: {glucose_value} mg/dL {trend} | Aggiornato: {local_time}")

    def fetch_glucose_data(self):
        try:
            api_url = f"{self.config['nightscout_url']}/api/v1/entries.json"
            
            params = {
                'count': 1,  # Torniamo a richiedere solo l'ultima lettura
                'find[type]': 'sgv'
            }
            
            # Imposta il bottone di refresh come disabilitato durante il caricamento
            self.refresh_button.setEnabled(False)
            self.refresh_button.setToolTip("Caricamento...")
            
            response = requests.get(api_url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                # Aggiorna il valore corrente
                entry = data[0]
                glucose_value = entry["sgv"]
                direction = entry.get("direction", "")
                timestamp = entry.get("dateString", "")
                delta = entry.get("delta", 0)
                
                # Converti il timestamp in formato locale
                from datetime import datetime
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    local_time = dt.astimezone().strftime("%H:%M")
                except:
                    local_time = timestamp
                
                # Converti le frecce di direzione secondo Nightscout
                trend_arrows = {
                    "DoubleUp": "⇈",
                    "SingleUp": "↑",
                    "FortyFiveUp": "↗",
                    "Flat": "→",
                    "FortyFiveDown": "↘",
                    "SingleDown": "↓",
                    "DoubleDown": "⇊",
                    "NOT COMPUTABLE": "-",
                    "RATE OUT OF RANGE": "⚡"
                }
                
                trend = trend_arrows.get(direction, "")
                
                # Aggiorna le etichette con più informazioni
                self.glucose_label.setText(f"{glucose_value}")
                self.info_label.setText(f"{trend} mg/dL\n{delta:+.1f} mg/dL\nUltimo aggiornamento: {local_time}")
                
                # Colori standard di Nightscout
                if glucose_value > 180:
                    color = "#FF4444"  # Alto
                elif glucose_value < 70:
                    color = "#FFaa44"  # Basso
                else:
                    color = "#44FF44"  # In range
                
                self.glucose_label.setStyleSheet(f"""
                    font-size: 72px;
                    font-weight: bold;
                    color: {color};
                    padding: 10px;
                """)
                
                # Aggiorna l'icona nel system tray
                self.update_tray_icon(glucose_value, trend, color, local_time)
                
            else:
                raise Exception("Nessun dato disponibile")
                
        except Exception as e:
            print(f"Errore dettagliato: {str(e)}")
            self.glucose_label.setText("Errore")
            self.info_label.setText(str(e))
        
        finally:
            # Riabilita il bottone di refresh
            self.refresh_button.setEnabled(True)
            self.refresh_button.setToolTip("Aggiorna dati (R)")

    def keyPressEvent(self, event):
        # Gestione scorciatoia R per refresh
        if event.key() == Qt.Key_R:
            self.fetch_glucose_data()
        super().keyPressEvent(event) 

    def show_about(self):
        """Mostra la finestra delle informazioni"""
        dialog = AboutDialog(self)
        dialog.exec_()

    def quit_application(self):
        """Chiude completamente l'applicazione senza minimizzare nel tray"""
        self.tray_icon.hide()  # Nasconde l'icona dal tray
        self.close()  # Chiude l'applicazione 

    def show_welcome(self):
        """Mostra la finestra di benvenuto"""
        dialog = WelcomeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            config = dialog.get_config()
            self.config.update(config)
            try:
                with open("src/config.json", "w") as f:
                    json.dump(self.config, f, indent=4)
                
                # Aggiorna gli headers
                self.headers = {
                    'api-secret': self.config['api_secret_sha1'],
                    'Content-Type': 'application/json'
                }
                
                # Ricarica i dati
                self.fetch_glucose_data()
                
                QMessageBox.information(self, "Successo", "Configurazione salvata con successo!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore nel salvare la configurazione: {str(e)}") 

    def show_help(self):
        """Mostra la finestra di aiuto"""
        dialog = HelpDialog(self)
        dialog.exec_() 

    def changeEvent(self, event):
        """Gestisce l'evento di minimizzazione"""
        if self.isMinimized():  
            self.hide()  # Nasconde la finestra invece di minimizzarla
        super().changeEvent(event) 