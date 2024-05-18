import pygame
import sys

result = 1
# Khởi tạo Pygame
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH=1280
SCREEN_HEIGHT=720
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)

font = pygame.font.Font('font/VNF-Comic Sans.ttf',96)
bar =  font.render('________',True,'black')
button=pygame.transform.scale(pygame.image.load('img/button.png'),(60,60))
x=SCREEN_WIDTH/2-button.get_width()/2
mouse_held=False

pygame.mixer.music.load('sound/ingame.mp3')
pygame.mixer.music.play(-1)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect((x, SCREEN_HEIGHT/2),(60, 60))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button_rect.collidepoint(mouse_pos):
                    mouse_held=True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_held=False
    if mouse_held:
        x=mouse_pos[0]-button.get_width()/2
        if x > SCREEN_WIDTH/2+bar.get_width()/2-button.get_width()/2:
            x = SCREEN_WIDTH/2+bar.get_width()/2-button.get_width()/2
        elif x < SCREEN_WIDTH/2-bar.get_width()/2-button.get_width()/2:
            x = SCREEN_WIDTH/2-bar.get_width()/2-button.get_width()/2
    volume = (x+button.get_width()/2-SCREEN_WIDTH/2+bar.get_width()/2)/(bar.get_width()/2)/2
    pygame.mixer.music.set_volume(volume)
    screen.fill((255, 255, 255))
    screen.blit(bar,(SCREEN_WIDTH/2-bar.get_width()/2, SCREEN_HEIGHT/2-90))
    screen.blit(button,(x, SCREEN_HEIGHT/2))
    pygame.display.flip()

pygame.quit()
sys.exit()