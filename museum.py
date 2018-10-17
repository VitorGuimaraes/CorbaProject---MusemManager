# -*-coding: utf-8-*-

# System imports:
import os
import sys
import time

# Third party imports:
from omniORB import CORBA, PortableServer
import CosNaming, Guarda
import Sino

import pygame as pg 
from pygame.locals import *

pg.init()						   # Inicializa o pygame
pg.font.init()                     # Inicializa o addon de fontes

SCREEN_SIZE = (410, 590)           # Dimensões da tela
BACKGROUND_COLOR = (255, 255, 255)
CAPTION = "Controle de Museu"
clock = pg.time.Clock()
font = pg.font.Font("nyala.ttf", 45)

# Load images
back0 = pg.image.load("sprites/back0.png")
back1 = pg.image.load("sprites/back1.png")
back2 = pg.image.load("sprites/back2.png")
go0 = pg.image.load("sprites/go0.png")
go1 = pg.image.load("sprites/go1.png")
go2 = pg.image.load("sprites/go2.png")
visitor_update = pg.image.load("sprites/visitor_update.png")
night_visitor_update = pg.image.load("sprites/night_visitor_update.png")
museum = pg.image.load("sprites/museum.png")
night_museum = pg.image.load("sprites/night_museum.png")
closed = pg.image.load("sprites/closed.png")
opened = pg.image.load("sprites/open.png")
gate_background = pg.image.load("sprites/gate_background.png")
night_gate_background = pg.image.load("sprites/night_gate_background.png")
day = pg.image.load("sprites/day.png")
night = pg.image.load("sprites/night.png")
guard_front = pg.image.load("sprites/guard_front.png")
guard_side = pg.image.load("sprites/guard_side.png")
guard_update = pg.image.load("sprites/guard_update.png")
left_gate = pg.image.load("sprites/left_gate.png")
right_gate = pg.image.load("sprites/rigth_gate.png")
counter_update = pg.image.load("sprites/counter_update.png")

bell1 = pg.image.load("bell/1.png")
bell2 = pg.image.load("bell/2.png")
bell3 = pg.image.load("bell/3.png")
bell4 = pg.image.load("bell/1.png")
bell5 = pg.image.load("bell/5.png")
bell6 = pg.image.load("bell/6.png")
bell7 = pg.image.load("bell/7.png")
bell8 = pg.image.load("bell/8.png")
bell9 = pg.image.load("bell/9.png")
bell10 = pg.image.load("bell/10.png")

bells = [bell1, bell2, bell3, bell4, bell5, bell6, bell7, bell8, bell9, bell10]
gate_sound = pg.mixer.Sound("gate_sound.ogg")

# Initialise the ORB and find the root POA
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

def bind():
	try:
		obj = orb.resolve_initial_references("NameService")
		rootContext = obj._narrow(CosNaming.NamingContext)

		name = [CosNaming.NameComponent("Guard Server", "context"),
				CosNaming.NameComponent("Guard", "Object")]
		
		obj = rootContext.resolve(name)
		obj = obj._narrow(Guarda.Guard)
		
		if obj is None:
			print("Object reference is not an Guarda::Guard")
			sys.exit(1)

		print("Binded succesfully")
		return obj
		
	except CosNaming.NamingContext.NotFound, ex:
		print("Name not found")
		sys.exit(1)

def add_visitor(screen):
	start_y = 590

	while start_y >= 420:
		for y in range(5):
			screen.blit(gate_background, (0, 0))
			screen.blit(go0, (0, start_y))
			screen.blit(visitor_update, (0, 0))
			screen.blit(bell1, (0, 0))
			
			pg.display.update()
			clock.tick(30)
			start_y -= 2

		for y in range(3):
			screen.blit(gate_background, (0, 0))
			screen.blit(go1, (0, start_y))
			screen.blit(visitor_update, (0, 0))
			screen.blit(bell1, (0, 0))
			pg.display.update()
			clock.tick(30)
			start_y -= 2

		for y in range(5):
			screen.blit(gate_background, (0, 0))
			screen.blit(go2, (0, start_y))
			screen.blit(visitor_update, (0, 0))
			screen.blit(bell1, (0, 0))
			pg.display.update()
			clock.tick(30)
			start_y -= 2

def remove_visitor(screen, is_day):
	start_y = 420

	while start_y <= 590:
		for y in range(5):

			if is_day:
				screen.blit(gate_background, (0, 0))
			elif not is_day:
				screen.blit(night_gate_background, (0, 0))

			screen.blit(back0, (0, start_y))

			if is_day:
				screen.blit(visitor_update, (0, 0))
			
			elif not is_day:
				screen.blit(night_visitor_update, (0, 0))

			screen.blit(bell1, (0, 0))
			
			pg.display.update()
			clock.tick(30)
			start_y += 2

		for y in range(3):

			if is_day:
				screen.blit(gate_background, (0, 0))
			elif not is_day:
				screen.blit(night_gate_background, (0, 0))

			screen.blit(back1, (0, start_y))

			if is_day:
				screen.blit(visitor_update, (0, 0))
			
			elif not is_day:
				screen.blit(night_visitor_update, (0, 0))

			screen.blit(bell1, (0, 0))
			pg.display.update()
			clock.tick(30)
			start_y += 2

		for y in range(5):
			if is_day:
				screen.blit(gate_background, (0, 0))
			elif not is_day:
				screen.blit(night_gate_background, (0, 0))

			screen.blit(back2, (0, start_y))

			if is_day:
				screen.blit(visitor_update, (0, 0))
			
			elif not is_day:
				screen.blit(night_visitor_update, (0, 0))

			screen.blit(bell1, (0, 0))
			pg.display.update()
			clock.tick(30)
			start_y += 2

def close_gate(screen):
	
	left_gate_start = 0 
	right_gate_start = 0

	gate_sound.play()
	for i in range(18):
		screen.blit(night_gate_background, (0, 0))

		screen.blit(left_gate, (left_gate_start, 0))
		screen.blit(right_gate, (right_gate_start, 0))

		screen.blit(night_visitor_update, (0, 0))
		screen.blit(bell1, (0, 0))

		pg.display.update()

		left_gate_start  += 1
		right_gate_start -= 1	
		clock.tick(5)

def open_gate(screen):

	left_gate_start = 18 
	right_gate_start = -18

	gate_sound.play()
	for i in range(18):
		screen.blit(gate_background, (0, 0))

		screen.blit(left_gate, (left_gate_start, 0))
		screen.blit(right_gate, (right_gate_start, 0))

		screen.blit(visitor_update, (0, 0))
		screen.blit(bell1, (0, 0))

		pg.display.update()
		clock.tick(5)

		left_gate_start  -= 1
		right_gate_start += 1	

def day_night(screen, is_day):

	if is_day is False:
		screen.blit(night, (0, 0))
		screen.blit(night_museum, (0, 0))
		screen.blit(bell1, (0, 0))

		screen.blit(guard_side, (0, 0))
		screen.blit(closed, (0, 0))

		pg.display.update()
		time.sleep(0.5)

		screen.blit(night_museum, (0, 0))

		screen.blit(guard_front, (0, 0))
		screen.blit(closed, (0, 0))
		pg.display.update()

	elif is_day is True:
		screen.blit(day, (0, 0))

		screen.blit(museum, (0, 0))
		screen.blit(left_gate, (18, 0))
		screen.blit(right_gate, (-18, 0))
		screen.blit(bell1, (0, 0))

		screen.blit(guard_side, (0, 0))
		screen.blit(opened, (0, 0))

		pg.display.update()
		time.sleep(0.5)

		screen.blit(museum, (0, 0))

		screen.blit(guard_front, (0, 0))
		screen.blit(opened, (0, 0))
		pg.display.update()

def bell(screen):
	for bell in bells:
		
		screen.blit(night_museum, (0, 0))
		screen.blit(closed, (0, 0))
		screen.blit(guard_front, (0, 0))

		screen.blit(bell, (0, 0))
		pg.display.update()

		clock.tick(12)
	
	for bell in reversed(bells):
		
		screen.blit(night_museum, (0, 0))
		screen.blit(closed, (0, 0))
		screen.blit(guard_front, (0, 0))

		screen.blit(bell, (0, 0))
		pg.display.update()

		clock.tick(12)

def main():

	screen = pg.display.set_mode(SCREEN_SIZE)		# Tamanho da janela
	screen.fill(BACKGROUND_COLOR)				    # Cor de fundo
	pg.display.set_caption(CAPTION)                 # Título da janela

	is_day = True
	guard_obj = bind()                              # Objeto Guarda


	while True:
		time.sleep(0.1)

		if is_day:
			screen.blit(day, (0, 0))
			screen.blit(museum, (0, 0))
			screen.blit(opened, (0, 0))
		
		elif not is_day:
			screen.blit(night, (0, 0))
			screen.blit(night_museum, (0, 0))
			screen.blit(closed, (0, 0))
			screen.blit(left_gate, (18, 0))
			screen.blit(right_gate, (-18, 0))

		screen.blit(bell1, (0, 0))
		screen.blit(counter_update, (0, 0))
		screen.blit(guard_front, (0, 0))

		visitors = guard_obj.get_visitors()
		screen.blit(font.render(str(visitors), 1, (255, 255, 255)), (60, 540))
			
		pg.display.update() 

		for event in pg.event.get():

			if event.type == pg.MOUSEBUTTONDOWN:
				x, y = pg.mouse.get_pos()

				visitors = guard_obj.get_visitors()

				if x >= 33 and x <= 49 and y >= 531 and y <= 546 and is_day:
					guard_obj.warns_guard("entered")

					screen.blit(counter_update, (0, 0))
					screen.blit(font.render(str(visitors), 1, (255, 255, 255)), (60, 540))
					add_visitor(screen)
				
				elif x >= 14 and x <= 29 and y >= 531 and y <= 546 and is_day and visitors > 0:
					guard_obj.warns_guard("exited")

					screen.blit(counter_update, (0, 0))
					screen.blit(font.render(str(visitors), 1, (255, 255, 255)), (60, 540))
					remove_visitor(screen, is_day)

				elif x >= 101 and x <= 137 and y >= 544 and y <= 579:
					is_day = not is_day
					day_night(screen, is_day)

					if not is_day:
						
						total_visitors = guard_obj.get_visitors()
						
						if total_visitors > 0:
							bell(screen)

						guard_obj.is_night()

						while total_visitors > 0:
							screen.blit(counter_update, (0, 0))
							screen.blit(font.render(str(total_visitors), 1, (255, 255, 255)), (60, 540))
							
							remove_visitor(screen, is_day)
							total_visitors -= 1
						
						close_gate(screen)

					elif is_day:
						open_gate(screen)

			elif event.type == QUIT:
				return 

if __name__ == "__main__":
	main()