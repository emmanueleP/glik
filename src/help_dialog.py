"""
Glik - A Nightscout desktop viewer
Copyright (C) 2025 Emmanuele Pani
"""

from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QScrollArea, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from .resources import get_icon_path

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aiuto")
        self.setWindowIcon(QIcon(get_icon_path()))
        self.setModal(True)
        self.resize(800, 600)
        
        # Crea un'area scrollabile
        scroll = QScrollArea(self)
        scroll.setStyleSheet("QScrollArea { background-color: #1e1e1e; border: none; }")
        
        content = QWidget()
        content.setStyleSheet("QWidget { background-color: #1e1e1e; }")
        
        layout = QVBoxLayout(content)
        
        # Titolo
        title = QLabel("Guida alla lettura dei dati")
        title.setStyleSheet("""
            QLabel { 
                color: white; 
                font-size: 18px; 
                font-weight: bold; 
                margin-bottom: 15px;
                background-color: transparent;
            }
        """)
        layout.addWidget(title)
        
        # Stile comune per tutte le label
        common_style = """
            QLabel { 
                color: white; 
                font-size: 14px;
                background-color: transparent;
            }
        """
        
        # Frecce di tendenza
        trend_text = """
        <div style='color: white;'>
            <h3>Frecce di Tendenza</h3>
            <p>Le frecce indicano la velocità e la direzione del cambiamento della glicemia:</p>
            <table>
            <tr><td>⇈ (DoubleUp)</td><td>Aumento rapido (>3 mg/dL/min)</td></tr>
            <tr><td>↑ (SingleUp)</td><td>Aumento (2-3 mg/dL/min)</td></tr>
            <tr><td>↗ (FortyFiveUp)</td><td>Aumento lento (1-2 mg/dL/min)</td></tr>
            <tr><td>→ (Flat)</td><td>Stabile (0-1 mg/dL/min)</td></tr>
            <tr><td>↘ (FortyFiveDown)</td><td>Diminuzione lenta (1-2 mg/dL/min)</td></tr>
            <tr><td>↓ (SingleDown)</td><td>Diminuzione (2-3 mg/dL/min)</td></tr>
            <tr><td>⇊ (DoubleDown)</td><td>Diminuzione rapida (>3 mg/dL/min)</td></tr>
            <tr><td>- (NOT COMPUTABLE)</td><td>Impossibile calcolare la tendenza</td></tr>
            <tr><td>⚡ (RATE OUT OF RANGE)</td><td>Variazione fuori range</td></tr>
            </table>
        </div>
        """
        
        trend_label = QLabel(trend_text)
        trend_label.setTextFormat(Qt.RichText)
        trend_label.setStyleSheet(common_style)
        layout.addWidget(trend_label)
        
        # Colori
        colors_text = """
        <div style='color: white;'>
            <h3>Colori della Glicemia</h3>
            <p>I colori indicano il range del valore glicemico:</p>
            <table>
            <tr><td><span style='color: #FF4444'>■ Rosso</span></td><td>Glicemia alta (>180 mg/dL)</td></tr>
            <tr><td><span style='color: #44FF44'>■ Verde</span></td><td>Glicemia in range (70-180 mg/dL)</td></tr>
            <tr><td><span style='color: #FFaa44'>■ Arancione</span></td><td>Glicemia bassa (<70 mg/dL)</td></tr>
            </table>
        </div>
        """
        
        colors_label = QLabel(colors_text)
        colors_label.setTextFormat(Qt.RichText)
        colors_label.setStyleSheet(common_style)
        layout.addWidget(colors_label)
        
        # Delta
        delta_text = """
        <div style='color: white;'>
            <h3>Delta (Δ)</h3>
            <p>Il delta mostra la variazione della glicemia rispetto alla lettura precedente:</p>
            <ul>
            <li>Un valore positivo (+) indica un aumento</li>
            <li>Un valore negativo (-) indica una diminuzione</li>
            </ul>
            <p>Esempio: +5.0 mg/dL significa che la glicemia è aumentata di 5 mg/dL dall'ultima lettura</p>
        </div>
        """
        
        delta_label = QLabel(delta_text)
        delta_label.setTextFormat(Qt.RichText)
        delta_label.setStyleSheet(common_style)
        layout.addWidget(delta_label)
        
        # Note
        notes_text = """
        <div style='color: white;'>
            <h3>Note Importanti</h3>
            <ul>
            <li>I dati vengono aggiornati automaticamente ogni 30 secondi (configurabile)</li>
            <li>È possibile aggiornare manualmente usando il tasto R o il pulsante di refresh</li>
            <li>L'app continua a funzionare in background quando viene minimizzata</li>
            </ul>
        </div>
        """
        
        notes_label = QLabel(notes_text)
        notes_label.setTextFormat(Qt.RichText)
        notes_label.setStyleSheet(common_style)
        layout.addWidget(notes_label)
        
        # Imposta il layout scrollabile
        content.setLayout(layout)
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        
        # Layout principale
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        
        # Stile della finestra
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QScrollBar:vertical {
                background: #2d2d2d;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #3d3d3d;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """) 