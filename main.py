# main.py
import sys
import os

# Ancre Python à la racine du projet
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.interface import lancer_interface

if __name__ == "__main__":
    lancer_interface()