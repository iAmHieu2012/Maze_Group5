import pygame
from pygame.locals import *
 
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
rect1 = img_spr.get_rect()

img_clt = font.render("Collect", True, WHITE)
rect2 = img_clt.get_rect()

contentImg = []
contentFont = pygame.font.Font('font/Comic-Art.ttf', 25)

easy1   = contentFont.render("Easy     :               " + str(recordList[0]), True, WHITE)
rect_e1 = img_spr.get_rect()

medium1 = contentFont.render("Medium :              " + str(recordList[1]), True, WHITE)
rect_m1 = img_spr.get_rect()

hard1   = contentFont.render("Hard     :              " + str(recordList[2]), True, WHITE)
rect_h1 = img_spr.get_rect()

easy2   = contentFont.render("Easy     :               " + str(recordList[3]), True, WHITE)
rect_e2 = img_spr.get_rect()

medium2 = contentFont.render("Medium :              " + str(recordList[4]), True, WHITE)
rect_m2 = img_spr.get_rect()

hard2   = contentFont.render("Hard     :              " + str(recordList[5]), True, WHITE)
rect_h2 = img_spr.get_rect()

# fp = open('record.txt', 'r')
# data = fp.readlines()
# for i in range(len(data)):
#     try:
#         contentImg.append(contentFont.render(data[i], True, DARKBROWN))
#     except:
#         contentImg.append(contentFont.render(' ', True, DARKBROWN))
# fp.close()

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
    screen.blit(medium1, (50, 140))
    screen.blit(hard1, (50, 170))
    screen.blit(easy2, (50, 340))
    screen.blit(medium2, (50, 370))
    screen.blit(hard2, (50, 400))

    pygame.display.update()

pygame.quit()