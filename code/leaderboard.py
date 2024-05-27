import pygame
from pygame.locals import *
from main_prg import reset_record
BLACK = (0, 0, 0)
GREEN = (1, 50, 32)
WHITE = (255, 255, 255)
DARKBROWN = (92, 64, 51)

fp = open('current_account.txt', 'r')
username = fp.readline()
fp.close()
filename = 'player_record/' + username + '.txt'
fp = open(filename, 'r')
recordList = list(map(int, fp.readline().split()))
fp.close()

pygame.init()

#Đặt tên cho cửa sổ game là Maze
pygame.display.set_caption('Record')

# #Hình ảnh tượng trưng cho game đặt bên trái tên cửa sổ game
icon = pygame.image.load('img/maze_icon.png')
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((478, 478))

font = pygame.font.Font('font/AGENTORANGE.TTF', 36)

img_spr = font.render("Speedrun", True, WHITE)
img_clt = font.render("Collect", True, WHITE)

contentImg = []
contentFont = pygame.font.Font('font/Comic-Art.ttf', 25)

easy1   = contentFont.render("Easy     :", True, WHITE)
medium1 = contentFont.render("Medium :", True, WHITE)
hard1   = contentFont.render("Hard     :", True, WHITE)
easy2   = contentFont.render("Easy     :", True, WHITE)
medium2 = contentFont.render("Medium :", True, WHITE)
hard2   = contentFont.render("Hard     :", True, WHITE)

reset   = contentFont.render("Reset", True, WHITE)
reset_rect = reset.get_rect()

# mouse_pos = pygame.mouse.get_pos()
# def is_over_reset_box(mouse_pos):
#     return reset_rect.collidepoint(mouse_pos)
# if is_over_reset_box(mouse_pos):
    

record_data = []
for i in range(3):
    if recordList[i] != 150:
        record_data.append(contentFont.render(str(recordList[i]), True, WHITE))
    else:
        record_data.append(contentFont.render('None', True, WHITE))
for i in range(3, 6, 1):
    record_data.append(contentFont.render(str(recordList[i]), True, WHITE))

running = True
background_image = pygame.image.load('img/lead_bg.png')
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Tô màu màn hình
    screen.fill(WHITE)
    # Vẽ ảnh nền
    screen.blit(background_image, (0, 0))
    screen.blit(img_spr, (20, 30))
    screen.blit(img_clt, (20, 260))

    screen.blit(easy1, (50, 110))
    screen.blit(record_data[0], (200, 110))

    screen.blit(medium1, (50, 140))
    screen.blit(record_data[1], (200, 140))

    screen.blit(hard1, (50, 170))
    screen.blit(record_data[2], (200, 170))

    screen.blit(easy2, (50, 340))
    screen.blit(record_data[3], (200, 340))

    screen.blit(medium2, (50, 370))
    screen.blit(record_data[4], (200, 370))

    screen.blit(hard2, (50, 400))
    screen.blit(record_data[5], (200, 400))

    screen.blit(reset, (400, 20))

    pygame.display.update()

pygame.quit()

