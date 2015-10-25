#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Serpent.py
#
#  Copyright 2014 Guénaël Muller <contact@inkey-art.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
from collections import deque
# liste chaînée pour gérer de façon optimisé le serpent.
from random import randint


class Serpent(object):

    """Création d'un Serpent

    attributs:
            coords : coordonnées des divers morceaux du Serpent
            direction : direction du serpent, voir classe Direction.
            vitesse : vitesse du serpent, voir classe Vitesse.

    attributs de configuration:
            TAILLE_DEB : Taille de départ du Serpent : 3 par défaut
            TAILLE_MIN : Taille minimale acceptable d'un Serpent

    """
    TAILLE_DEB = 3  # Taille de départ du Serpent
    TAILLE_MIN = 2  # Taille minimale acceptable d'un Serpent,
    # si plus petit, il meurt
    # CONSTRUCTEUR

    def __init__(self, x, y, direction):
        '''Constructeur avec position de départ x,y et directions'''
        self.coords = deque([(x, y)])  # Tableau de coordonnée du Serpent
        self.direction = direction  # direction
        self.vitesse = Vitesse.NORMAL  # vitesse

        # On rempli le serpent par rapport à sa taille initiale
        for a in range(0, self.TAILLE_DEB):
            self.grandir()

    def tete(self):
        '''Récupérer les coordonnées de la tête du Serpent'''
        return self.coords[len(self.coords) - 1]

    # GESTION TAILLE
    def calculCoord(self, direction):
        '''calcul et renvoi des coordonnée du prochain élément'''
        # On récupères les coordonées de la tête
        nvCoord = list(self.tete())
        # on les modifient en conséquence
        for i in range(0, 2):
            # on applique bêtement la direction
            nvCoord[i] += direction[i]
            # On réadapte par rapport au torique
            while nvCoord[i] < 0 or nvCoord[i] >= Plateau.TAILLE_MAX:
                if nvCoord[i] < 0:
                    nvCoord[i] += Plateau.TAILLE_MAX
                if nvCoord[i] >= Plateau.TAILLE_MAX:
                    nvCoord[i] -= Plateau.TAILLE_MAX
            assert nvCoord[i] < 0 or nvCoord >= Plateau.TAILLE_MAX
        # on retourne le résultat en tuple
        return tuple(nvCoord)

    def grandir(self):
        '''Faire grandir le serpent d'une case'''
        self.coords.append(tuple(self.calculCoord(self.direction)))

    # Reduire le serpent d'une case
    def reduire(self):
        '''Faire réduire le serpent	'''
        if len(self.coords) > 0:
            self.coords.popleft()

    # GESTION DEPLACEMENT

    def avancer(self):
        '''Faire avancer le serpent	'''
        self.grandir()
        self.reduire()
    '''
	MODIFICATEURS
	'''

    def set_direction(self, direction):
        """Changer la direction à l'aide d'un objet Direction"""
        if direction[0] == -self.direction[0] and direction[1] == -self.direction[1]:
            return False
        self.direction = direction
        return True

    def inv_sens(self):
        """Inverse le sens de déplacement"""
        nvDir = []
        # On récupéres les 2 positions de la queue
        posActu = self.coords[0]
        posPrec = self.coords[1]
        # on inverse le serpent
        self.coords.reverse()
        # on change la direction en conséquence
        for e in range(0, 2):
            val = posActu[e] - posPrec[e]
            nvDir.append(val)
        # if self.calculCoord(tuple(nvDir)) in self.coords :
            # for e in nvDir :
            # e=-e
        self.direction = tuple(nvDir)
# Main


class Plateau(object):

    """Plateau avec un serpent, des pommes, des poires des murs,etc…
    attributs:
            message : message d'information
            poires : emplacements des poires
            pommes : emplacements des pommes
            murs : emplacements des murs

    attributs de configuration:
            TAILLE_MAX : Taille maximal du plateau
    """

    message = ""
    poires = [(10, 10), (1, 1), (5, 6), (7, 12)]
    # Emplacements des poires.
    #pommes = [(1,10),(8,1),(16,4)]
    pommes = []
    # Emplacements des pommes.
    murs = [(4, 5), (5, 5), (6, 5)]
    rand = lambda a, x, y:  (randint(x, y), randint(x, y))
    # Emplacement des murs.
    TAILLE_MAX = 20  # Taille maximum du Plateau.

    def __init__(self, xDep, yDep):
        """Création d'un Jeu avec un serpent"""
        self.s = Serpent(xDep, yDep, Direction.SUD)
        self.remplirTab(self.pommes, 30)

    def remplirTab(self, tab, nb):
        for a in range(0, nb):
            while True:
                tmp = self.rand(0, self.TAILLE_MAX - 1)
                if not (tmp in tab):
                    tab.append(tmp)
                    break

    def aManger(self):
        '''On regarde si le serpent à manger '''
        bPomme, bPoire = False, False

        for e in self.s.coords:
            if e in self.pommes:
                self.pommes.remove(e)
                bPomme = True
                break
            if e in self.poires:
                self.poires.remove(e)
                bPoire = True
                break
        if bPomme:
            self.s.grandir()
            self.s.vitesse = Vitesse.NORMAL
        elif bPoire:
            self.s.inv_sens()
            self.s.reduire()
            # self.s.vitesse=Vitesse.LENTE
        return bPomme or bPoire

    def aPerdu(self):
        """le serpent est mort ?"""
        if len(self.s.coords) < self.s.TAILLE_MIN:
            self.message = "Mort par anorexie"
            return True
        for e in self.s.coords:
            # for i in e :
                # if i not in range(0,self.TAILLE_MAX) :
                    # return True
            if e in self.murs:
                self.message = "Ce mur n'était pas en papier"
                return True
            if self.testDoublon(self.s.coords):
                self.message = "Cannibale ?"
                # print "hop là"
                return True
        return False

    def testDoublon(self, tab):
        for e in tab:
            nb = 0
            for a in tab:
                if e == a:
                    nb += 1
                    #print (str(e)+""+str(a))
            if nb > 1:
                return True
        return False

    def aGagner(self):
        """le serpent a réussi sa mission ?"""
        if not self.pommes and not self.poires:
            self.message = "Bravo!"
            return True
        return False

    def toString(self):
        """Affiche le plateau en texte"""
        sRet = ""
        for a in range(0, Plateau.TAILLE_MAX):
            for b in range(0, Plateau.TAILLE_MAX):
                bSerp, bTete, bPommes, bMurs, bPoire = False, False, False, False, False

                for element in self.s.coords:
                    if element[0] == a and element[1] == b:
                        bSerp = True
                        if element == self.s.tete():
                            bTete = True
                for element in self.pommes:
                    if element[0] == a and element[1] == b:
                        bPommes = True
                for element in self.murs:
                    if element[0] == a and element[1] == b:
                        bMurs = True

                for element in self.poires:
                    if element[0] == a and element[1] == b:
                        bPoire = True

                if bTete == True:
                    sRet += "T"
                elif bSerp == True:
                    sRet += "S"
                elif bPommes == True:
                    sRet += "O"
                elif bPoire == True:
                    sRet += "P"
                elif bMurs == True:
                    sRet += "M"
                else:
                    sRet += "*"
            sRet += "\n"
        return sRet


class Direction:

    """Valeur x,y des directions cardinales"""
    NORD = (-1, 0)
    SUD = (1, 0)
    EST = (0, 1)
    OUEST = (0, -1)


class Vitesse:
    NORMAL = 0.1
    RAPIDE = 0.05
    LENTE = 0.3

# help(Serpent.direction)
# help(Direction)
# help(Metier)

# interface minimale
if __name__ == '__main__':
    help(Direction)
    help(Serpent)
    help(Plateau)
    m = Plateau(4, 4)
    while not (m.aGagner() or m.aPerdu()):
        print(m.toString())
        car = raw_input("Entrez une Direction (N,S,E,O): ")
        direction = ()
        if (car == 'N'):
            direction = Direction.NORD
        elif (car == 'E'):
            direction = Direction.EST
        elif (car == 'S'):
            direction = Direction.SUD
        elif (car == 'O'):
            direction = Direction.OUEST
        m.s.set_direction(direction)
        m.s.avancer()
        m.aManger()

    if m.aGagner():
        print "Bravo !"
    else:
        print "Désolé !"
