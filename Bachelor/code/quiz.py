import pygame
import random
import sys
import json

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
TURQUOISE = (64, 224, 208)

# Laden von Fragen aus einer JSON-Datei
def load_questions(filename):
    with open(filename, 'r') as file:
        questions = json.load(file)
    return questions

# Rendern eines mehrzeiligen Textes
def render_multiline_text(surface, text, font, color, x, y, max_width):
    words = text.split()
    lines = []
    line = ''
    for word in words:
        test_line = line + word + ' '
        if font.size(test_line)[0] < max_width:
            line = test_line
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)
    
    # Berechnung der vertikalen Position, um den Text zentriert anzuzeigen
    total_height = len(lines) * font.get_linesize()
    y -= total_height // 2
    
    for line in lines:
        rendered_text = font.render(line, True, color)
        text_rect = rendered_text.get_rect(center=(x, y))
        surface.blit(rendered_text, text_rect)
        y += font.get_linesize()

# Das Quiz-Spiel
def quiz(screen, WIDTH, HEIGHT, questions, score):
    pygame.mixer.init()  # Initialisierung des Sound-Systems
    correct_sound = pygame.mixer.Sound('sounds/correct.mp3')  # Sound für die richtige Antwort
    wrong_sound = pygame.mixer.Sound('sounds/incorrect.mp3')  # Sound für die falsche Antwort
    quizbackground = pygame.image.load('images/quizbackground.png')
    quizbackground = pygame.transform.scale(quizbackground, (WIDTH, HEIGHT))
    
    font = pygame.font.SysFont('comicsansms', 55)
    small_font = pygame.font.SysFont('comicsansms', 35)
    question_font = pygame.font.SysFont('comicsansms', 45, bold=True)
    option_font = pygame.font.SysFont('comicsansms', 30)
    correct_answer_given = False

    # Wähle eine Frage aus
    question_data = random.choice(questions)
    question = question_data['question']
    options = question_data['answers']
    correct_answer = question_data['correct_answer']

    # Positionen für die Antwortoptionen speichern
    option_rects = []
    backgroundmusic = pygame.mixer.Sound('sounds/backgroundmusic.mp3')
    backgroundmusic.stop()
    while not correct_answer_given:
        screen.blit(quizbackground, (0, 0))
        
        # Frage anzeigen
        render_multiline_text(screen, question, question_font, SILVER, WIDTH // 2, HEIGHT // 4, WIDTH - 40)
        
        option_x = WIDTH // 2
        option_y = HEIGHT // 2
        
        # Berechnung der maximalen Breite für die Optionen
        max_option_width = max([small_font.size(f"{chr(97 + i)}. {option}")[0] for i, option in enumerate(options)])
        
        # Antwortoptionen anzeigen
        for i, option in enumerate(options):
            prefix = chr(97 + i)  # a, b, c, d usw.
            text_surface = option_font.render(f"{prefix}. {option}", True, WHITE)
            text_rect = text_surface.get_rect(midtop=(option_x, option_y))
            option_rects.append((text_rect, option, prefix))
            option_y += text_surface.get_height() + 20  # Anpassung der vertikalen Position und Abstand zwischen den Optionen

        # Mausposition abfragen
        mouse_pos = pygame.mouse.get_pos()
        
        # Antwortoptionen zeichnen und bei Bedarf hervorheben
        for text_rect, option, prefix in option_rects:
            if text_rect.collidepoint(mouse_pos):
                color = GOLD
            else:
                color = WHITE
            screen.blit(option_font.render(f"{prefix}. {option}", True, color), text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for text_rect, option, prefix in option_rects:
                    if text_rect.collidepoint(mouse_pos):
                        if option == correct_answer:
                            correct_sound.play()  # Sound für richtige Antwort abspielen
                            correct_answer_given = True
                        else:
                            wrong_sound.play()    # Sound für falsche Antwort abspielen
                            correct_answer_given = False
                            # Falsche Antwortanzeige
                            wrong_answer_text = font.render("Falsche Antwort!", True, RED)
                            screen.blit(wrong_answer_text, (WIDTH // 2 - wrong_answer_text.get_width() // 2, HEIGHT // 2 - 100))
                            pygame.display.update()
                            pygame.time.wait(2000)  # Warte 2 Sekunden, bevor das Spiel endet
                            return False  # Hier kann auch ein "game_over_screen" aufgerufen werden

        pygame.display.update()
    
    return True

# Beispiel, wie das Quiz gestartet werden könnte
if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Quiz Spiel")
    questions = load_questions('fragen.json')
    score = 0  # oder irgendein initialer Punktestand
    quiz(screen, WIDTH, HEIGHT, questions, score)
    pygame.quit()
