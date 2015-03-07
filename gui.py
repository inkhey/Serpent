 #!/usr/bin/python
 # -*- coding: utf-8 -*-
#Interface graphique pygame du jeu
import os, sys
import time
import pygame
from pygame.locals import *
from Serpent import *
TAILLE_CASE = 20
def pos (x) :  return x[1]*TAILLE_CASE,x[0]*TAILLE_CASE
if not pygame.font: print 'Attention, polices désactivées'
if not pygame.mixer: print 'Attention, son désactivé'


FOND=255,255,255
pygame.init()
fenetre = pygame.display.set_mode((TAILLE_CASE*Plateau.TAILLE_MAX,TAILLE_CASE*Plateau.TAILLE_MAX))
fenetre.fill(FOND)
m=Plateau(4,4)

#chargement des images
imgSerp= pygame.image.load("./img/corps.png").convert_alpha()
imgMur=pygame.image.load("./img/murs.png").convert_alpha()
imgPomme=pygame.image.load("./img/pommes.png").convert_alpha()
imgPoire=pygame.image.load("./img/poire.png").convert_alpha()

def afficher() :
	for Scoord in m.s.get_coord() :
		posxy = pos(Scoord)
		fenetre.blit(imgSerp,posxy )
		
	for Mcoord in m.get_murs() :
		posxy = pos(Mcoord)
		fenetre.blit(imgMur,posxy )

	for Pcoord in m.get_pommes() :
		posxy = pos(Pcoord)
		fenetre.blit(imgPomme,posxy )
		
	for Pcoord in m.get_poires() :
		posxy = pos(Pcoord)
		fenetre.blit(imgPoire,posxy )

continuer = 1

#Jeux
while continuer  :

	fenetre.fill(FOND)
	direction = m.s.get_direction()
	for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
		if event.type == QUIT : 
			continuer=0
			break
		if event.type == KEYDOWN:
			if  event.key == K_LEFT :
				direction = Direction.OUEST
			elif event.key == K_RIGHT :
				direction = Direction.EST
			elif event.key == K_UP :
				direction = Direction.NORD
			elif event.key == K_DOWN :
				direction = Direction.SUD
	if	not continuer : break;
	afficher()
	time.sleep(m.s.get_vitesse())
	m.s.set_direction(direction)
	m.s.avancer()
	m.aManger()
	pygame.display.flip()
	if m.aPerdu(): 
		continuer = 0
	if m.aGagner(): 
		continuer = 0

fin=1

#animation de fin
while fin:

	fenetre.fill(FOND)
	afficher()
	time.sleep(m.s.get_vitesse())
	m.s.reduire()
	pygame.display.flip()
	for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
		if event.type == QUIT : 
			fin=0
			break

#message final
print (m.message)
