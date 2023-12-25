"""
File: game.py
Author: GUNDUZ Maxime
Date: 2023
Description: Contient les fonctions nécessaire pour le déroulement du jeu.
"""

import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
import random
import pygame

def IntroPopup():

    """
    Affiche une fenêtre d'introduction avec les règles du jeu.
    Si l'utilisateur ne souhaite pas jouer, il peut quitter le jeu.
    """

    Bienvenue = "Bienvenue cher Joueur !\n"
    regles = """Ce jeu est inspiré de la série "Alice in borderland", le jeu du 3 de Pic présent dans l'épisode 1.\n\nVoici les règles :
    Dans chaque pièce, deux portes sont présentes : l'une est étiquetée 'Vie' et l'autre 'Mort'.
    Une de ces portes conduit à une salle suivante, tandis que l'autre mène à une fin prématurée.
    Il est crucial de noter que choisir la porte 'Vie' ne garantit pas nécessairement une sortie sans danger,
    tout comme opter pour la porte 'Mort' ne signifie pas une issue fatale. Le jeu se base sur le hasard.
    Il existe trois salles au total. Pour chaque décision prise, le joueur dispose de 20 secondes pour choisir la porte appropriée,
    sauf pour la dernière salle où la durée est réduite à 10 secondes.
    À chaque étape, le résultat est aléatoire : l'une des portes conduit à une continuation du jeu,
    tandis que l'autre met fin à la partie. Pour gagner, le joueur doit sortir indemne trois fois consécutivement dans le temps imparti.
    Si ce n'est pas le cas, il est éliminé.
    Même le concepteur de ce jeu n'est pas à l'abri de la défaite.
    La nature aléatoire du jeu signifie que la probabilité de succès est de 1 sur 8,
    ce qui implique que les participants ont 7 chances sur 8 de ne pas réussir.\n"""

    response = messagebox.askquestion("Message d'introduction", Bienvenue + regles + "Êtes-vous prêt à commencer le jeu ?")
    
    if response == 'no':
        messagebox.showinfo("Au Revoir", "Au revoir !")
        exit()

def Audio_Mute():

    """
    Permet de mettre en sourdine ou de réactiver la musique de fond du jeu.
    """

    global is_muted
    is_muted = not is_muted
    if is_muted:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

def play_background_music():

    """
    Joue la musique de fond du jeu en boucle.
    """

    pygame.mixer.init()
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.music.load("./assets/Sound/GameTheme.wav")
    pygame.mixer.music.play(-1)

def play_sound(sound_file):

    """
    Joue un son spécifique si le jeu n'est pas en mode sourdine.
    """

    if not is_muted:
        sound = pygame.mixer.Sound(sound_file)
        sound.play()

def play_countdown_sound():

    """
    Joue un son de compte à rebours si le temps restant est inférieur ou égal à 5 secondes.
    """

    if not is_muted:
        countdown = pygame.mixer.Sound("./assets/Sound/bit.wav")
        countdown.play()

def lose():

    """
    Gère la logique lorsque le joueur perd et propose de rejouer.
    """

    pygame.mixer.music.stop()
    play_sound("./assets/Sound/lose.wav")
    
    response = messagebox.askquestion("Perdu", "Vous avez perdu, voulez vous rejouer ?")
    if response == 'no':
        messagebox.showinfo("Au Revoir", "Au revoir !")
        exit()
    else:
        global time_left, room
        time_left = 20
        room = 1
        play_background_music()

def win():

    """
    Gère la logique lorsque le joueur gagne et propose de rejouer.
    """

    pygame.mixer.music.stop()
    play_sound("./assets/Sound/win.wav")
    response = messagebox.askquestion("Felicitation", "Vous avez gagné, voulez vous rejouer ?")
    if response == 'no':
        messagebox.showinfo("Au Revoir", "Au revoir !")
        exit()
    else:
        global time_left, room
        time_left = 20
        room = 1
        play_background_music()

def game():

    """
    Gère le déroulement principal du jeu en fonction des décisions du joueur.
    """

    global time_left, room
    rand_nb = random.randint(0, 1)
    if rand_nb == 0:
        lose()
    else:
        if room == 3:
            win()
        else:
            play_sound("./assets/Sound/continue.wav")
            if room == 2:
                time_left = 10
            else:
                time_left = 20
            room += 1
            lbl_room.config(text=f"Numéro de salle : {room}/3")

def update_time():

    """
    Met à jour le temps restant et déclenche les actions nécessaires en fonction du temps.
    """

    global time_left, room
    if time_left > 0:
        if time_left <= 5:
            play_countdown_sound()
        mins = time_left // 60
        secs = time_left % 60
        lbl_chrono.config(text=f"Temps restant : {mins:02d}:{secs:02d}")
        time_left -= 1
        lbl_room.config(text=f"Numéro de salle : {room}/3")
        root.after(1000, update_time)
    else:
        lbl_chrono.config(text="Temps écoulé !")
        lose()

def Display_Chrono(root, temps):

    """
    Affiche un chronomètre à l'écran pour informer le joueur du temps restant.
    """

    global time_left
    time_left = temps
    minutes = temps // 60
    secondes = temps % 60
    global lbl_chrono
    lbl_chrono = tk.Label(root, text=f"Temps restant : {minutes:02d}:{secondes:02d}", font=("Arial", 14))
    lbl_chrono.pack(anchor=tk.NE, padx=20, pady=10)
    update_time()

def Display_button(root):

    """
    Affiche les boutons "Vie" et "Mort" que le joueur peut utiliser pour faire des choix.
    """

    life_img = Image.open("./assets/Image/Death.png")
    death_img = Image.open("./assets/Image/Live.png")
    width, height = 250, 400
    life_img = life_img.resize((width, height))
    death_img = death_img.resize((width, height))
    life_photo = ImageTk.PhotoImage(life_img)
    death_photo = ImageTk.PhotoImage(death_img)
    frame = tk.Frame(root)
    frame.pack(pady=50)
    frame_life = tk.Frame(frame)
    frame_life.pack(side=tk.LEFT, padx=20)
    btn_life = tk.Button(frame_life, image=life_photo, command=game)
    btn_life.image = life_photo
    btn_life.pack()
    lbl_life = tk.Label(frame_life, text="Mort", font=("Arial", 12))
    lbl_life.pack()
    frame_death = tk.Frame(frame)
    frame_death.pack(side=tk.LEFT, padx=20)
    btn_death = tk.Button(frame_death, image=death_photo, command=game)
    btn_death.image = death_photo
    btn_death.pack()
    lbl_death = tk.Label(frame_death, text="Vie", font=("Arial", 12))
    lbl_death.pack()

def main():

    """
    Fonction principale qui initialise et gère l'interface utilisateur et le déroulement du jeu.
    """

    global root, lbl_room, is_muted
    global time_left, room
    is_muted = False
    BoolGame = True
    time = 20
    room = 1
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = int(screen_width * 0.5)
    height = int(screen_height * 0.7)
    root.minsize(width, height)
    root.title("Death or Alive")
    root.resizable(False, False)
    messagebox.showinfo("Auteur", "Ce programme a étais réalisé par :\n- GUNDUZ Maxime \n- Github : https://github.com/MaxiyaG/\n- Date: Novembre 2023")
    IntroPopup()

    lbl_room = tk.Label(root, text=f"Numéro de salle : {room}/2", font=("Arial", 14))
    lbl_room.pack(anchor=tk.SW, padx=20, pady=10)
    btn_mute = tk.Button(root, text="Activer/Désactiver le son", command=Audio_Mute)
    btn_mute.pack(pady=20)
    play_background_music()
    while BoolGame:
        Display_button(root)
        Display_Chrono(root, time)
        root.mainloop()

