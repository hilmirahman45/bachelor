# Importiere alle erforderlichen Module und Ressourcen
import pygame
import sys
from menu import main_menu  # Beispielname für deine Hauptspiel-Datei

# Initialisiere Pygame
pygame.init()

# Definiere die Bildschirmgröße
WIDTH = 800
HEIGHT = 600

# Erstelle das Pygame-Fenster
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Starte das Spiel
main_menu()

# Beenden des Spiels und Rückkehr zum Betriebssystem
pygame.quit()
sys.exit()
