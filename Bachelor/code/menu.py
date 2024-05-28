import pygame
import sys
import csv
from maingame import flappy_bird_game

# Initialisierung von Pygame
pygame.init()
pygame.mixer.init()

buttonsound = pygame.mixer.Sound('sounds/buttonclick.mp3')

# Bildschirmdimensionen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menüfenster")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Schriftart
font = pygame.font.SysFont(None, 55)

def create_button(image, hover_image, x, y, button_width, button_height, click):
    button_surface = pygame.transform.scale(image, (button_width, button_height))
    button_rect = button_surface.get_rect(topleft=(x, y))
    
    screen.blit(button_surface, button_rect.topleft)

    mouse = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse):
        hover_surface = pygame.transform.scale(hover_image, (button_width, button_height))
        screen.blit(hover_surface, button_rect.topleft)  # Bild an der gleichen Position wie das Rechteck zeichnen
        if click:
            return True

    return False

def create_simple_button(image, x, y, icon_width, icon_height, click):
    button_surface = pygame.transform.scale(image, (icon_width, icon_height))
    button_rect = button_surface.get_rect(topleft=(x, y))
    #pygame.draw.rect(screen, RED, button_rect, 1)  # Rechteck um die Schaltfläche zeichnen (Dicke 1)
    screen.blit(button_surface, button_rect.topleft)
    
    mouse = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse) and click:
        return True
    
    return False

def show_scoreboard():
    # Lade die Spielerdaten aus der CSV-Datei und sortiere sie nach Punkten
    try:
        with open('highscores.csv', mode='r') as file:
            reader = csv.reader(file)
            player_data = list(reader)
    except FileNotFoundError:
        player_data = []

    # Sortiere die Spielerdaten nach den Punkten in absteigender Reihenfolge
    player_data.sort(key=lambda x: int(x[1]), reverse=True)

    # Zeige die besten 3 Spieler auf dem Bildschirm an
    y_offset = HEIGHT // 2 - 50  # Startposition für das Scoreboard
    for i, entry in enumerate(player_data[:3], start=1):
        font = pygame.font.SysFont('comicsansms', 30)
        text = font.render(f"{i}. {entry[0]}  {entry[1]}", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 30

def scoreboard_screen():
    back_button_img = pygame.image.load('images/back.png').convert_alpha()
    back_button_hover_img = pygame.image.load('images/backhover.png').convert_alpha()
    
    button_width = 150
    button_height = 50
    back_button_x = WIDTH // 2 - button_width // 2
    back_button_y = HEIGHT - 100

    running = True
    while running:
        screen.fill(BLACK)
        
        font = pygame.font.SysFont('comicsansms', 55)
        title = font.render("HIGHSCORES", True, WHITE)
        title_x = WIDTH // 2 - title.get_width() // 2
        title_y = HEIGHT // 5 - title.get_height() // 2
        
        screen.blit(title, (title_x, title_y))

        show_scoreboard()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linksklick
                    click = True
        
        if create_button(back_button_img, back_button_hover_img, back_button_x, back_button_y, button_width, button_height, click):
            return  # Zurück zum Hauptmenü
        
        pygame.display.update()

def main_menu():
    play_button_img = pygame.image.load('images/playbutton.png').convert_alpha()
    play_button_hover_img = pygame.image.load('images/playhover.png').convert_alpha()
    quit_button_img = pygame.image.load('images/quitbutton.png').convert_alpha()
    quit_button_hover_img = pygame.image.load('images/quithover.png').convert_alpha()
    menubackground = pygame.image.load('images/mainmenubackground.webp').convert_alpha()
    menubackground = pygame.transform.scale(menubackground, (WIDTH, HEIGHT))
    scoreboard_button_img = pygame.image.load('images/icon.png').convert_alpha()
    scoreboard_button_img = pygame.transform.scale(scoreboard_button_img, (75, 75))

    button_width = 250
    button_height = 100
    button_spacing = 20  # Reduziere den Abstand zwischen den Schaltflächen
    icon_width, icon_height = 75, 75
    
    # Positioniere die Schaltflächen an spezifischen Koordinaten
    play_button_x = WIDTH // 2 - button_width // 2
    play_button_y = HEIGHT * 0.4  # Verschiebe die Play-Schaltfläche nach unten
    quit_button_x = WIDTH // 2 - button_width // 2
    quit_button_y = play_button_y + button_height + button_spacing
    scoreboard_button_x = WIDTH // 2 - 25  # 25 ist die Hälfte der Buttonbreite (50 / 2)
    scoreboard_button_y = quit_button_y + button_height + 50

    running = True
    while running:
        screen.blit(menubackground, (0, 0))
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linksklick
                    buttonsound.play()
                    click = True
                    

        if create_button(play_button_img, play_button_hover_img, play_button_x, play_button_y, button_width, button_height, click):
            buttonsound.play()
            flappy_bird_game(screen, WIDTH, HEIGHT)
            
        if create_simple_button(scoreboard_button_img, scoreboard_button_x, scoreboard_button_y, icon_width, icon_height, click):
            scoreboard_screen()
            buttonsound.play()

            # Keine Änderung an `running`, damit das Menü erneut angezeigt wird

        if create_button(quit_button_img, quit_button_hover_img, quit_button_x, quit_button_y, button_width, button_height, click):
            buttonsound.play()
            pygame.quit()
            sys.exit()
        
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
