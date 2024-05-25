import pygame
from pygame.locals import *
 
BLACK = (0, 0, 0)
GREEN = (1, 50, 32)
WHITE = (255, 255, 255)
DARKBROWN = (92, 64, 51)
pygame.init()

#Đặt tên cho cửa sổ game là Maze
pygame.display.set_caption('Instruction')

# #Hình ảnh tượng trưng cho game đặt bên trái tên cửa sổ game
img = pygame.image.load('img/maze_icon.png')
pygame.display.set_icon(img)

screen = pygame.display.set_mode((400, 400))

font = pygame.font.Font('font/AGENTORANGE.TTF', 48)
img = font.render("ABOUT US", True, GREEN)
rect = img.get_rect()
# pygame.draw.rect(img, WHITE, rect, 1)

contentImg = []
contentFont = pygame.font.Font('font/Comic-Art.ttf', 18)
fp = open('about.txt', 'r')
data = fp.readlines()
for i in range(len(data)):
    try:
        contentImg.append(contentFont.render(data[i], True, DARKBROWN))
    except:
        contentImg.append(contentFont.render(' ', True, DARKBROWN))
fp.close()

running = True
background_image = pygame.image.load('img/ins_bg.png')
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Tô màu màn hình
    screen.fill(WHITE)
    # Vẽ ảnh nền
    screen.blit(background_image, (0, 0))
    screen.blit(img, (20, 20))
    for i in range(len(data)):
        screen.blit(contentImg[i], (20, 120 + i*20))

    pygame.display.update()

pygame.quit()