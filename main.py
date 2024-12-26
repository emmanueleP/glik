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

import sys
from PyQt5.QtWidgets import QApplication
from src.gui import MainWindow
import argparse

if __name__ == "__main__":
    # Parsing degli argomenti da linea di comando
    parser = argparse.ArgumentParser()
    parser.add_argument('--minimized', action='store_true', 
                       help="Avvia l'app minimizzata nel system tray")
    args = parser.parse_args()
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Tema di default
    
    window = MainWindow()
    
    # Se l'app è avviata con --minimized, nascondi la finestra principale
    if args.minimized:
        window.hide()
    
    sys.exit(app.exec_())
