def clear_csv(filename):
    with open(filename, 'w') as file:
        file.truncate(0)  # Lösche den Inhalt der Datei

# Beispielaufruf:
filename = "highscores.csv"  # Passe den Dateinamen entsprechend an
clear_csv(filename)

