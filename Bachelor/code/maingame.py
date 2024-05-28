import pygame
import random
import sys
from quiz import *
from gameover import *

# Flappy Bird Spiel
def flappy_bird_game(screen, WIDTH, HEIGHT):
    # Laden des Hintergrundbilds
    background_img = pygame.image.load('images/blackground.png').convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    # Farben
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)  # Neu hinzugefügte Farbe für die Anzeige der Hitbox

    # Spielvariablen
    gravity = 0.5
    character_movement = 0

    # Laden der Bilder
    character_img = pygame.image.load('images/bird.png').convert_alpha()
    character_img = pygame.transform.scale(character_img, (70, 70))  # Anpassen der Größe des Charakters
    character_rect = character_img.get_rect(center=(50, 300))

    pipe_img = pygame.image.load('images/futurepipe.png').convert_alpha()
    pipe_img = pygame.transform.scale(pipe_img, (140, 600))  # Anpassen der Größe der Röhren

    pipe_gap = 200  # Größere Öffnung
    pipe_speed = 5

    # Score Variablen
    score = 0
    score_font = pygame.font.SysFont(None, 55)

    # Erstellen der Röhren
    def create_pipe(pipe_gap, horizontal_distance):
        min_height = HEIGHT // 6
        max_height = HEIGHT - min_height - pipe_gap
        random_height = random.randint(min_height, max_height)  # Sicherstellen, dass die Röhre nicht zu hoch ist
        bottom_pipe_rect = pipe_img.get_rect(midtop=(WIDTH + horizontal_distance, random_height + pipe_gap // 2))
        top_pipe_rect = pipe_img.get_rect(midbottom=(WIDTH + horizontal_distance, random_height - pipe_gap // 2))
        return {'rect': bottom_pipe_rect, 'passed': False}, {'rect': top_pipe_rect, 'passed': False}

    pipe_list = []
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 50)  # Größerer Abstand zwischen den Röhren

    # Spielschleife
    running = True
    clock = pygame.time.Clock()
    quiz_attempts = 0
    correct_answer_given = False
    quiz_done = False  # Variable, um festzuhalten, ob das Quiz bereits durchgeführt wurde
    pipe_gap = 200  # Vertikaler Abstand zwischen den Röhren
    horizontal_distance = 300  # Horizontaler Abstand zwischen den Röhren
    next_pipe_distance = 0  # Abstand für die nächste Röhre
    pygame.mixer.init()
    flapsound = pygame.mixer.Sound('sounds/flap.mp3')
    backgroundmusic = pygame.mixer.Sound('sounds/backgroundmusic.mp3')
    backgroundmusic.set_volume(0.1)
    backgroundmusic.play(-1)  # Hintergrundmusik abspielen
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flapsound.play()
                    character_movement = 0
                    character_movement -= 10
            if event.type == SPAWNPIPE:
                # Röhren mit dem horizontalen Abstand erstellen
                pipe_list.extend(create_pipe(pipe_gap, next_pipe_distance))
                next_pipe_distance += horizontal_distance  # Nächste Röhre mit horizontal_distance Abstand erstellen

        character_movement += gravity
        character_rect.y += character_movement

        # Überprüfen, ob der Vogel das obere oder untere Ende des Bildschirms erreicht hat
        if character_rect.top <= 0 or character_rect.bottom >= HEIGHT:
            running = False
            backgroundmusic.stop()
            game_over_screen(screen, WIDTH, HEIGHT, int(score))

        # Bildschirm mit Hintergrundbild füllen
        screen.blit(background_img, (0, 0))

        # Charakter zeichnen
        screen.blit(character_img, character_rect)

        # Röhren bewegen und zeichnen
        for pipe in pipe_list:
            pipe['rect'].x -= pipe_speed
            pygame.draw.rect(screen, (255, 0, 0), pipe['rect'])  # Röhren-Rechteck zeichnen
            screen.blit(pipe_img, pipe['rect'])

        # Score aktualisieren und anzeigen
        for pipe in pipe_list:
            if pipe['rect'].right < character_rect.left and not pipe['passed']:
                score += 0.5
                pipe['passed'] = True

        # Score Text rendern
        score_text = score_font.render(f'Score: {int(score)}', True, WHITE)
        screen.blit(score_text, (10, 10))

        questions = load_questions('fragen.json')

        # Kollisionen überprüfen und Quiz durchführen
        # Kollisionen überprüfen und Quiz durchführen
        for pipe in pipe_list:
            if character_rect.colliderect(pipe['rect']) and not quiz_done:
                running = False
                pygame.mixer.pause()  # Alle laufenden Soundkanäle pausieren
                if quiz_attempts == 0:
                    score *= 1  # Keine Änderung am Score
                elif quiz_attempts == 1:
                    score *= 0.5  # 50% des Scores zurücksetzen
                elif quiz_attempts == 2:
                    score *= 0.25  # 75% des Scores zurücksetzen
                elif quiz_attempts == 3:
                    score = 0
                    
                correct_answer_given = quiz(screen, WIDTH, HEIGHT, questions, score)  # Quiz starten
                pygame.mixer.unpause()  # Alle Soundkanäle fortsetzen
                quiz_done = True
                if correct_answer_given:
                    quiz_attempts += 1  # Zurücksetzen der Quiz-Versuche
                    character_rect.center = (50, 300)  # Vogel zurücksetzen
                    pipe_list = []  # Röhrenliste leeren
                    correct_answer_given = False  # Zustand für korrekte Antwort zurücksetzen
                    quiz_done = False  # Zustand für Quiz zurücksetzen
                    next_pipe_distance = 0  # Abstand für nächste Röhre zurücksetzen
                    running = True  # Spiel fortsetzen
                elif not correct_answer_given:
                    backgroundmusic.stop()
                    game_over_screen(screen, WIDTH, HEIGHT, int(score))


        # Röhren entfernen, wenn sie aus dem Bildschirm verschwinden
        pipe_list = [pipe for pipe in pipe_list if pipe['rect'].right > 0]

        pygame.display.update()
        clock.tick(30)

# Beenden des Spiels und Rückkehr zum Menü
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Flappy Bird")
    flappy_bird_game(screen, 800, 800)
    pygame.quit()
    sys.exit()
