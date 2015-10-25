# -*- coding: utf-8 -*-
# interface en mode texte curses pour Serpent
from Serpent import *
import curses  # pour le dessin
import time    # pour la mesure du temps d'attente

ecran = curses.initscr()
curses.noecho()  # intialisation de l'écran
ecran.keypad(True)       # UN code sur les touches de fonctions
curses.curs_set(False)   # cacher le curseur
curses.start_color()
hauteur, largeur = ecran.getmaxyx()
debut = hauteur / 2
m = Plateau(4, 4)


def message(s):
    # longueur libre de chaque côté du message
    vide = (largeur - len(s)) / 2
    # hauteur d'affichage du message
    debut = hauteur / 2 - 2
    # message au centre de la ligne
    ecran.addstr(int(Plateau.TAILLE_MAX / 2), Plateau.TAILLE_MAX + 5, s)
    ecran.nodelay(False)                        # attente sur les getch()
    ecran.getch()                               # pour attendre...

message("Bienvenue")  # messaqe début

curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE)


ecran.getch()            # Attente frappe clavier
ecran.nodelay(True)      # pas d'attente sur getch()

while not (m.aGagner() or m.aPerdu()):
    ecran.clear()
    ecran.addstr(0, 0, (Plateau.TAILLE_MAX + 2) * "*", curses.color_pair(4))
    ecran.addstr(Plateau.TAILLE_MAX + 1, 0,
                 (Plateau.TAILLE_MAX + 2) * "*", curses.color_pair(4))

    # affichage
    for i in range(1, Plateau.TAILLE_MAX + 1):
        ecran.addstr(i, 0, "*", curses.color_pair(4))
    for i in range(1, Plateau.TAILLE_MAX + 1):
        ecran.addstr(i, Plateau.TAILLE_MAX + 1, "*", curses.color_pair(4))
    for elem in m.s.coords:
        ecran.addstr(elem[0] + 1, elem[1] + 1, 'S', curses.color_pair(1))

    for elem in m.murs:
        ecran.addstr(elem[0] + 1, elem[1] + 1, 'M', curses.color_pair(4))

    for elem in m.pommes:
        ecran.addstr(elem[0] + 1, elem[1] + 1, 'O', curses.color_pair(2))

    for elem in m.poires:
        ecran.addstr(elem[0] + 1, elem[1] + 1, 'b', curses.color_pair(3))
    # delai
    time.sleep(m.s.vitesse)

    # recupération directions
    c = ecran.getch()
    if (c == curses.KEY_LEFT):
        direction = Direction.OUEST
    elif (c == curses.KEY_RIGHT):
        direction = Direction.EST
    elif (c == curses.KEY_UP):
        direction = Direction.NORD
    elif (c == curses.KEY_DOWN):
        direction = Direction.SUD
    else:
        direction = m.s.direction
    m.s.direction = direction
    m.s.avancer()
    m.aManger()

if m.aGagner():
    message('Gagné !')
else:
    message('Perdu')


ecran.nodelay(False)
ecran.getch()            # Attente frappe clavier
curses.endwin()          # Terminer proprement
