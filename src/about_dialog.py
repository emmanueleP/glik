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

from PyQt5.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from .resources import get_logo_path, get_icon_path

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Informazioni")
        self.setWindowIcon(QIcon(get_icon_path()))
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo = QPixmap(get_logo_path())
        logo_label.setPixmap(logo.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        # Testo
        info_text = QLabel(
            "<h3>Glik</h3>"
            "<p>Versione 1.0.4</p>"
            "<p>Un visualizzatore desktop per Windows per visualizzare i dati della glicemia usando Nightscout.</p>"
            "<p>Basato sulla <a href='https://nightscout.github.io/'>documentazione Nightscout</a></p>"
            "<p>© 2025 - Emmanuele Pani.</p>"
            "<p>Questo software è rilasciato sotto licenza GNU AGPL v3.0</p>")
        info_text.setOpenExternalLinks(True)
        info_text.setWordWrap(True)
        info_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_text)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: white;
                min-width: 400px;
            }
            QLabel {
                color: white;
            }
            QLabel a {
                color: #3daee9;
            }
        """) 