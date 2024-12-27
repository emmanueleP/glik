"""
Glik - A Nightscout desktop viewer
Copyright (C) 2025 Emmanuele Pani
"""

import os
import sys

def get_resource_path(relative_path):
    """Ottiene il percorso assoluto per le risorse"""
    try:
        # PyInstaller crea una cartella temp e memorizza il percorso in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se non siamo in un exe, prova diversi percorsi base
        try_paths = [
            os.path.abspath("."),  # Directory corrente
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  # Directory del progetto
            os.path.dirname(os.path.abspath(sys.argv[0]))  # Directory dell'eseguibile
        ]
        
        # Prova ogni percorso finché non troviamo il file
        for base_path in try_paths:
            full_path = os.path.join(base_path, relative_path)
            if os.path.exists(full_path):
                return full_path
                
        # Se arriviamo qui, usa il primo percorso come fallback
        base_path = try_paths[0]
    
    return os.path.join(base_path, relative_path)

def get_logo_path():
    """Restituisce il percorso del logo PNG per la GUI"""
    paths = [
        'src/assets/logo_glik.png',  # Prima scelta
        'logo_glik.png',             # Seconda scelta
        'assets/logo_glik.png'       # Terza scelta
    ]
    
    # Prova ogni possibile percorso
    for path in paths:
        full_path = get_resource_path(path)
        if os.path.exists(full_path):
            return full_path
            
    # Se non troviamo il PNG, proviamo con l'ICO come fallback
    ico_paths = [
        'src/assets/logo_glik.ico',
        'logo_glik.ico',
        'assets/logo_glik.ico'
    ]
    
    for path in ico_paths:
        full_path = get_resource_path(path)
        if os.path.exists(full_path):
            return full_path
            
    return get_resource_path(paths[0])  # Ultimo tentativo con il primo percorso

def get_icon_path():
    """Restituisce il percorso dell'icona"""
    paths = [
        'src/assets/logo_glik.ico',
        'assets/logo_glik.ico',
        'logo_glik.ico'
    ]
    
    # Prova ogni possibile percorso
    for path in paths:
        full_path = get_resource_path(path)
        if os.path.exists(full_path):
            return full_path
            
    # Ritorna il primo percorso come fallback
    return get_resource_path(paths[0]) 