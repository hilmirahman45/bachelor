import pygame
import random
import sys
import csv
import os


# FARBEN
DARKRED = (139, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGREY = (169, 169, 169)
PURPLE = (128, 0, 128)
MAGENTA = (255, 0, 255)

def game_over_screen(screen, WIDTH, HEIGHT, score):
    exit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
    gameoverpic = pygame.image.load(os.path.join('images','gameoverbackground.png'))
    gameoverpic = pygame.transform.scale(gameoverpic, (WIDTH, HEIGHT))
    screen.blit(gameoverpic, (0, 0))
    gameover_font = pygame.font.Font(os.path.join('fonts','gameoverburn.ttf'), 100) 
    gameover_text = gameover_font.render('GAME OVER', True, MAGENTA)
    screen.blit(gameover_text, (WIDTH // 2 - gameover_text.get_width() // 2, HEIGHT - 500 - gameover_text.get_height() // 2))

    # Highscore und Name
    name_input = ''
    input_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 50, 400, 50)
    name_font = pygame.font.SysFont('comicsansms', 30)
    active = False
    cursor_visible = True
    cursor_timer = pygame.time.get_ticks()
    pygame.mixer.init()
    gameover = pygame.mixer.Sound('sounds/gameover.mp3')
    gameover.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                elif event.key == pygame.K_RETURN:
                    with open('highscores.csv', 'a', newline='') as csvfile:
                        fieldnames = ['Name', 'Score']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow({'Name': name_input, 'Score': score})
                    return name_input
                else:
                    if len(name_input) < 15:
                        name_input += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                else:
                    active = False

        # Blinken des Cursors
        if active:
            if pygame.time.get_ticks() - cursor_timer > 500:
                cursor_visible = not cursor_visible
                cursor_timer = pygame.time.get_ticks()
        
        pygame.draw.rect(screen, PURPLE, input_rect)
        pygame.draw.rect(screen, BLACK, input_rect, 2)
        input_surface = name_font.render(name_input, True, BLACK)
        screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))
        
        # Cursor anzeigen
        if cursor_visible and active:
            cursor = name_font.render('|', True, WHITE)
            screen.blit(cursor, (input_rect.x + 5 + input_surface.get_width(), input_rect.y + 5))
        
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    WIDTH, HEIGHT = pygame.display.get_surface().get_size()
    pygame.display.set_caption("Flappy Bird")
    game_over_screen(screen, WIDTH, HEIGHT, score = 0)
    pygame.quit()
