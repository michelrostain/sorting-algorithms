import sys
import os

# Permet d'importer les modules locaux quelle que soit
# la façon dont le script est lancé.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.interface import lancer_interface

if __name__ == "__main__":
    lancer_interface()