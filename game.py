"""
File: game.py
Author: GUNDUZ Maxime
Date: 2023
Description: Contient l'appel de la fonction main.
"""

from Function import main    

# Main
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
