import pygame
import os
from PIL import Image
import pyautogui
import pyperclip
import time

cl_white = (255,255,255)
cl_black = (0,0,0)
cl_grey = (50,50,50)
cl_lgrey = (150,150,150)
cl_red = (255,0,0)
cl_green = (50,255,50)
cl_yellow = (255,255,0)
cl_blue = (0,0,255)

cl_need = (131,179,129)





xx = 800
yy = 600








k_ctrl = False
k_shift = False
k_alt = False
k_space = False

mouse_touching_l = False
mouse_touching_r = False

k_r = False
k_e = False
k_v = False
k_x = False
k_d = False

person_x = 0
person_y = 0

pygame.init()
screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption('GraphWar Trainer')
pygame.display.set_icon(pygame.image.load('data/icon.ico'))


ss = pyautogui.screenshot()
ss.save(r'data/current.png')
time.sleep(0.5)

screen_png = pygame.image.load('data/screen.png')
current_png = pygame.image.load('data/current.png')


#line,parabola
func = 'line'
power = 2
k = 1
dx = 0

kk = 15.2

step = 0.02

out_func = ''


pi = 3.141592653589793238462643383279

def deg(alpha_rad):
	return alpha_rad * (180/pi)

def rad(alpha_deg):
	return alpha_deg * (pi/180)

def dist(x1,y1,x2,y2):
	return m.sqrt((x1-x2)**2 + (y1-y2)**2)

def line(x,y,x2,y2,color,width):
	pygame.draw.line(screen,color,(x,y),(x2,y2),width)

def line_a(x,y,x2,y2,color,width):
	pygame.draw.aaline(screen,color,(x,y),(x2,y2),width)

def circle(x,y,color,width):
	pygame.draw.circle(screen,color,(x,y),width)

def rect(x,y,lenght,height,color,width):
	pygame.draw.rect(screen,color,(x,y,lenght,height),width)

font = [0]*128
for i in range(2,128):
	font[i] = pygame.font.Font(None,i)

def textout(x,y,size,color,text):
	out = font[size].render(text, 1, color)
	screen.blit(out,(x,y))



def get_screen():
	s = ['']*yy
	for i in range(0,yy):
		s[i] = ['']*xx

	for y in range(0,yy):
		for x in range(0,xx):
			s[y][x] = screen.get_at((x,y))

	return s




def draw_main():
	screen.blit(screen_png,(0,0))
	screen.blit(current_normal_png,(15,15))
	if person_x or person_y:
		circle(person_x+xx//2,450//2+14-person_y,cl_red,6)

	textout(200,484,28,cl_black,out_func)


	textout(490,482,21,[cl_black,cl_red][int(func == 'line')],'1 - line')
	textout(560,482,21,[cl_black,cl_red][int(func == 'parabola')],'2 - parabola (numpad-power)')
	textout(490,497,21,cl_black,'LMC - Set point')
	textout(490,512,21,cl_black,'RMC+Mouse x - change delta x')
	textout(490,527,21,cl_black,'Scroll - change k (Minus - negative k)')
	
	textout(490,542,21,[cl_black,cl_red][int(k_shift)],'Shift (hold) - smoother changing')
	textout(490,557,21,cl_black,'Ctrl+C - Copy func')
	textout(490,572,21,cl_black,'r - refind graphwar window')


def normalize():
	global screen
	global current_png
	global current_normal_png
	screen.blit(current_png,(0,0))
	delta_x = 0
	delta_y = 0

	done = 0

	for x in range(1200):
		for y in range(800):
			if not(done):
				r = screen.get_at((x,y))[0]
				g = screen.get_at((x,y))[1]
				b = screen.get_at((x,y))[2]

				if (r,g,b) == cl_need:
					r = screen.get_at((x+1,y+1))[0]
					g = screen.get_at((x+1,y+1))[1]
					b = screen.get_at((x+1,y+1))[2]
					if (r,g,b) == cl_black:
						delta_x,delta_y = -x-1,-y-1
						done = 1

	screen = pygame.display.set_mode((770,450))
	screen.blit(current_png,(delta_x-1,delta_y-1))

	pygame.image.save(screen,'data/current_normal.png')

	current_normal_png = pygame.image.load('data/current_normal.png')

	screen = pygame.display.set_mode((xx,yy))



def draw_func(func):
	global out_func

	x = -50
	while x <= 50 and x >= -50:
		if func == 'line':
			y = k*x - k*person_x/kk
			out_func = str(round(k,3))+'*x'
		if func == 'parabola':
			y = k*((x+dx)**power) - k*(((person_x+dx*kk)/kk)**power)
			out_func = str(round(k,3+power))+'(x'+'+'*int(dx>=0)+str(round(dx,3))+')^'+str(power)

		
		circle(x*kk+xx//2,-y*kk+450//2+14-person_y,cl_red,1)


		x += step


def check_mouse_delta():
	global dx

	if mouse_touching_r:
		dx += ((mouse_xl - mouse_x)/kk)*[1,0.1][int(k_shift)]





normalize()


mouse_x = xx//2 + 200
mouse_y = yy//2

running = True
world_i = 0

state = 0


while running:

	screen.fill(cl_white)

	mouse_pos = pygame.mouse.get_pos()

	mouse_xl = mouse_x
	mouse_yl = mouse_y

	mouse_x = mouse_pos[0]
	mouse_y = mouse_pos[1]


	draw_main()
	draw_func(func)
	check_mouse_delta()


	





	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LCTRL:
				k_ctrl = True
			if event.key == pygame.K_LALT:
				k_alt = True
			if event.key == pygame.K_LSHIFT:
				k_shift = True
			if event.key == pygame.K_SPACE:
				k_space = True



		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LCTRL:
				k_ctrl = False
			if event.key == pygame.K_LALT:
				k_alt = False
			if event.key == pygame.K_LSHIFT:
				k_shift = False
			if event.key == pygame.K_SPACE:
				k_space = False

			if event.key == pygame.K_c:
				pyperclip.copy(out_func)

			if event.key == pygame.K_KP2:
				power = 2
			if event.key == pygame.K_KP3:
				power = 3
			if event.key == pygame.K_KP4:
				power = 4

			if event.key == pygame.K_e:
				k_e = False
			if event.key == pygame.K_v:
				k_v = False
			if event.key == pygame.K_x:
				k_x = False
			if event.key == pygame.K_d:
				k_d = False
			if event.key == pygame.K_r:
				k_r = False
				ss = pyautogui.screenshot()
				ss.save(r'data/current.png')
				time.sleep(0.5)
				screen_png = pygame.image.load('data/screen.png')
				current_png = pygame.image.load('data/current.png')
				screen = pygame.display.set_mode((1200,800))
				normalize()
			if event.key == pygame.K_1:
				func = 'line'
			if event.key == pygame.K_2:
				func = 'parabola'
			if event.key == pygame.K_MINUS:
				k *= -1





		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				mouse_touching_l = True
				person_x = mouse_x-xx//2
				person_y = 450//2-mouse_y+14


			if event.button == 3:
				mouse_touching_r = True
				
			if event.button == 4:
				mouse_scrolling_u = True
				
			if event.button == 5:
				mouse_scrolling_d = True
				

		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				mouse_touching_l = False
			if event.button == 3:
				mouse_touching_r = False

			if event.button == 4:
				mouse_scrolling_u = False
				k *= (1+1.5*[0.1,0.01][int(k_shift)])
			if event.button == 5:
				mouse_scrolling_d = False
				k /= (1+1.5*[0.1,0.01][int(k_shift)])





	
	pygame.display.flip()