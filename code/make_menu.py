import pygame, sys
import Login
import json
from pygame.locals import *
import soundbar

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGNETA = (255, 0, 255)
MUSTARD_YELLOW = (139, 128, 0)
BROWN = (150, 75, 0)
GRAY = (128, 128, 128)
DARK_ORANGE = (255, 140, 0)

def write_screen(s: str, color, color2, vt, custom_font: int, DISPLAYSURF, size):
    if custom_font == 0:
        custom_font = pygame.font.Font('font/AttackGraffiti.ttf', size)
    elif custom_font == -1:
        custom_font = pygame.font.Font('font/Shermlock.ttf', size)
    else:
        custom_font = pygame.font.SysFont('calibri', size)
    custom_text = custom_font.render(s, True, color, color2)
    custom_text_rect = custom_text.get_rect()
    custom_text_rect.center = vt
    DISPLAYSURF.blit(custom_text, custom_text_rect)

def set_all(s: str):
        #create surface
    DISPLAYSURF = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Tom and Jerry')
    
    #DISPLAYSURF.fill(BLUE)
    #pygame.draw.line(DISPLAYSURF, RED, (0, 0), (100, 100), 10)
    background = pygame.image.load('img/menu.jpg')
    picture = pygame.transform.scale(background, (1280, 720))
    textbox = pygame.image.load('img/board.png').convert_alpha()
    textbox = pygame.transform.scale(textbox,(200,50))
    DISPLAYSURF.blit(picture, (0, 0))

    #textsys
    write_screen("Hi "+s+" !", BLACK, None, (1280/2-100, 100), -1, DISPLAYSURF, 60)
    #textcus
    collide_rect_list =[]
    for i in range(8):
        DISPLAYSURF.blit(textbox, (1280//2 - 400,i*50+220))
        collide_rect_list.append(pygame.rect.Rect(1280//2 - 400,i*50+220,200,50))
        # pygame.draw.rect(DISPLAYSURF, BROWN, (1280//2 - 200,i*50 + 220, 400, 50), 6) #ve bang chon
    # pygame.draw.rect(DISPLAYSURF, RED, (1280//2 - 200, 0*50 + 220, 400, 50), 6)
    lst = ["PLAY", "AUTOPLAY", "LOAD GAME", "LEADERBOARD", "HELP", "SETTINGS", "ABOUT", "LOG OUT"]
    for i in range(8):
        write_screen(lst[i], WHITE, None, (1280/2-300, i*50 + 245), -1, DISPLAYSURF, 24)
    pygame.display.update()
    return DISPLAYSURF, collide_rect_list

def make_sound(mode = 0):
    if mode == 0:
        sound_1 = 'sound/mouse.wav'
    else:
        sound_1 = 'sound/key.wav'
    sound_1 = pygame.mixer.Sound(sound_1)
    sound_1.play()
    sound_1.set_volume(0.2)

def rec_input(DISPLAYSURF, x, y) -> int:
    font = pygame.font.SysFont('calibri', 20)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(x, y, 140, 32)
    color_inactive = GRAY
    color_active = BLACK
    color = color_inactive
    active = False
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                tempx = pygame.mouse.get_pos()[0]
                tempy = pygame.mouse.get_pos()[1]
                if 900 < tempx < 940 and 302 < tempy < 340: #quit dialog
                        return 1000
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                make_sound(1)
                if active:
                    if event.key == pygame.K_RETURN:
                        return int(text)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if event.unicode in list("0123456789") and len(text) < 3:
                            text += event.unicode
        pygame.draw.rect(DISPLAYSURF, WHITE, input_box)
            # Render the current text.
        txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
            # Blit the text.
        DISPLAYSURF.blit(txt_surface, (input_box.x+5, input_box.y+5))
            # Blit the input_box rect.
        pygame.draw.rect(DISPLAYSURF, color, input_box, 4)

        pygame.display.flip()
        clock.tick(30)

def make_dialog(DISPLAYSURF, s: str, mode = 0, auto = 0):
    # logbox = pygame.image.load('img/log.png').convert_alpha()
    # logbox = pygame.transform.scale(logbox, (600, 480))
    pygame.draw.rect(DISPLAYSURF, WHITE, (1280//2 - 250, 300, 550, 240))
    pygame.draw.rect(DISPLAYSURF, BLUE, (1280//2 - 250, 300, 550, 40))
    write_screen(s, WHITE, None, (1280//2 - 240 + 80, 320), 1, DISPLAYSURF, 20)
    write_screen("  X  ", WHITE, RED, (1280//2 + 280, 320), -1, DISPLAYSURF, 20)
    button_X = pygame.Rect((900, 302, 40, 38))
    if mode == 0:
        write_screen("LEVEL", BLACK, None, (1280//2 - 240 + 30, 380), -1, DISPLAYSURF, 20)
        lst = ["EASY", "MEDIUM", " HARD "]
        for i in range(1, 4):
            write_screen(lst[i - 1], BLACK, CYAN, (1280//2 - 210 + 150 * i, 380), -1, DISPLAYSURF, 20)
        x = -1
        running = True
        hard = 0
        runner = 0
        while running:
            if runner == 0:#choose map 
                for event in pygame.event.get(): 
                    if event.type == pygame.MOUSEBUTTONUP:
                        make_sound()
                        tempx = pygame.mouse.get_pos()[0]
                        tempy = pygame.mouse.get_pos()[1]
                        temp = (tempx - 538)//150
                        if (-1 < temp < 3 and 360 < tempy < 400 and temp != x):
                            x>-1 and write_screen(lst[x], BLACK, CYAN, (1280//2 - 210 + 150 * (x + 1), 380), -1, DISPLAYSURF, 20)
                            write_screen(lst[temp], BLACK, BROWN, (1280//2 - 210 + 150 * (temp + 1), 380), -1, DISPLAYSURF, 20)
                            x = temp
                        elif button_X.collidepoint((tempx, tempy)): #quit dialog
                            running = False
                            return -1
                        elif temp == x > -1:
                            if temp == 0: hard = 20
                            elif temp == 1: hard = 40
                            else: hard = 100
                            runner = 1
                            if auto == 1:
                                return [hard, 4]
            elif runner == 1 and auto == 0:#choose mode play
                if lst[0] != "NORMAL":
                    x = -1
                    write_screen("MODE", BLACK, None, (1280//2 - 240 + 40, 450), -1, DISPLAYSURF, 20)
                    pygame.time.delay(500)
                    lst = ["NORMAL", "SPEEDRUN", "LIMIT"]
                    for i in range(1, 4):
                        write_screen(lst[i - 1], BLACK, CYAN, (1280//2 - 210 + 150 * i, 450), -1, DISPLAYSURF, 20)
                for event in pygame.event.get(): 
                    if event.type == pygame.MOUSEBUTTONUP:
                        make_sound()
                        tempx = pygame.mouse.get_pos()[0]
                        tempy = pygame.mouse.get_pos()[1]
                        temp = (tempx - 538)//150
                        if 900 < tempx < 940 and 302 < tempy < 340: #quit dialog
                            running = False
                            return -1
                        elif (-1 < temp < 3 and 430 < tempy < 470 and x!= temp):
                            x>-1 and write_screen(lst[x], BLACK, CYAN, (1280//2 - 210 + 150 * (x + 1), 450), -1, DISPLAYSURF, 20)
                            write_screen(lst[temp], BLACK, BROWN, (1280//2 - 210 + 150 * (temp + 1), 450), -1, DISPLAYSURF, 20)
                            x = temp
                        elif temp == x:
                            mode2 = temp
                            running = False
                            return [hard, mode2]
            pygame.display.update((380, 300, 600, 250))

    elif mode == 1: #done sucess or failed
        while True:
            mode == 1 and write_screen("Press X to start playing! Hope u enjoy =^.^=", BLACK, None, (1280//2, 380), 1, DISPLAYSURF, 18)
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONUP:
                    make_sound()
                    tempx = pygame.mouse.get_pos()[0]
                    tempy = pygame.mouse.get_pos()[1]
                    temp = (tempx - 588)//200
                    if 900 < tempx < 940 and 302 < tempy < 340: #quit dialog
                        return
            pygame.display.update((380, 300, 600, 250))

    elif mode == 3:#quit game
        write_screen("Do u really want to log out? We will miss u =^.^=", BLACK, None, (1280//2, 380), 1, DISPLAYSURF, 18)
        write_screen("SURE                                     NO", BLACK, WHITE, (1280//2, 500), 1, DISPLAYSURF, 18)
        while True:
            for event in pygame.event.get(): 
                tempx = pygame.mouse.get_pos()[0]
                tempy = pygame.mouse.get_pos()[1]
                if event.type == pygame.MOUSEBUTTONUP:
                    make_sound()
                    if (900 < tempx < 940 and 302 < tempy < 340) or (724 < tempx < 748 and 490 < tempy < 506): #quit dialog
                        return -1
                    elif 542 < tempx < 567 and 489 < tempy < 506:
                        return 0
                else:
                    if 542 < tempx < 567 and 489 < tempy < 506:
                        write_screen("SURE", BLACK, BROWN, ((542+568)//2, 500), 1, DISPLAYSURF, 18)
                    elif 724 < tempx < 748 and 490 < tempy < 506:
                        write_screen("NO", BLACK, BROWN, ((720 + 746)//2, 500), 1, DISPLAYSURF, 18)
                    else:
                        write_screen("SURE                                     NO", BLACK, WHITE, (1280//2, 500), 1, DISPLAYSURF, 18)
            pygame.display.update((380, 300, 600, 250))

    elif mode == 4:#setting
        write_screen(" KEY ", BLACK, None, (1280//2 - 240 + 30, 380), -1, DISPLAYSURF, 20)
        lst = ["AWSD", "ARROWKEY", "JIKL"]
        for i in range(1, 4):
            write_screen(lst[i - 1], BLACK, CYAN, (1280//2 - 210 + 150 * i, 380), -1, DISPLAYSURF, 20)
        x = -1
        running = True
        key_mode = 0
        runner = 0
        while running:
            if runner == 0:#choose map 
                for event in pygame.event.get(): 
                    if event.type == pygame.MOUSEBUTTONUP:
                        make_sound()
                        tempx = pygame.mouse.get_pos()[0]
                        tempy = pygame.mouse.get_pos()[1]
                        temp = (tempx - 538)//150
                        if (-1 < temp < 3 and 360 < tempy < 400 and temp != x):
                            x>-1 and write_screen(lst[x], BLACK, CYAN, (1280//2 - 210 + 150 * (x + 1), 380), -1, DISPLAYSURF, 20)
                            write_screen(lst[temp], BLACK, BROWN, (1280//2 - 210 + 150 * (temp + 1), 380), -1, DISPLAYSURF, 20)
                            x = temp
                        elif 900 < tempx < 940 and 302 < tempy < 340: #quit dialog
                            running = False
                            return -1
                        elif temp == x > -1:
                            key_mode = temp
                            runner = -1
            pygame.display.update()
            if runner == -1:
                soundbar.sound_all(DISPLAYSURF)
                return (key_mode, -1)

def make_menu(s: str):
    textbox = pygame.image.load('img/board.png').convert_alpha()
    textbox = pygame.transform.scale(textbox,(200,50))
    textbox_p = pygame.image.load('img/board_pressed.png').convert_alpha()
    textbox_p = pygame.transform.scale(textbox_p,(200,50))
    lst = ["PLAY", "AUTOPLAY", "LOAD GAME", "LEADERBOARD", "HELP", "SETTINGS", "ABOUT", "LOG OUT"]
    while True:
        DISPLAYSURF, collide_rect_list = set_all(s)
        clock = pygame.time.Clock()
        running = True
        y = 0
        while running:
            mousePos = pygame.mouse.get_pos()
            for item in collide_rect_list:
                if item.collidepoint(mousePos):
                    DISPLAYSURF.blit(textbox_p, (item[0],item[1]))
                    write_screen(lst[collide_rect_list.index(item)], GRAY, None, (1280/2-300, collide_rect_list.index(item)*50 + 245), -1, DISPLAYSURF, 24)
                    # y = lst[collide_rect_list.index(item)]
                else:
                    DISPLAYSURF.blit(textbox, (item[0],item[1]))
                    write_screen(lst[collide_rect_list.index(item)], WHITE, None, (1280/2-300, collide_rect_list.index(item)*50 + 245), -1, DISPLAYSURF, 24)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    make_sound()
                    tempx = pygame.mouse.get_pos()[0]
                    tempy = pygame.mouse.get_pos()[1]
                    temp = (tempy - 220) // 50
                    if (-1< temp < 8 and 1280//2 - 300 < tempx < 1280//2 - 100 and temp!=y):
                        y = temp
                    elif temp == y > -1:
                        if (y == 0 or y == 1):
                            while True:
                                lst = make_dialog(DISPLAYSURF, "Choose mode to play", 0, y)
                                if lst == -1:
                                    return 0
                                if True:
                                    hard_mode = [s, y] + lst
                                    hard = hard_mode[2]
                                    make_dialog(DISPLAYSURF, "Sucess: " + str(hard) + " x " + str(hard), 1)
                                    #play_game with mode 0 (play), 1(autoplay)
                                    return hard_mode
                        elif y == 2:
                            return [s,2]
                            
                        elif y == 3:
                            return 3

                        elif y == 4:
                            return 4
                        
                        elif y == 5:
                            n = make_dialog(DISPLAYSURF, "SETTINGS", 4)
                            return 0
                        
                        elif y == 6:
                            return 6
                        
                        elif (y == 7):
                            n = make_dialog(DISPLAYSURF, "Log out", 3)
                            if n == -1:
                                return 0
                            if n == 0:
                                running = False
                                return -1 

                elif event.type == QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

# if __name__=="__main__":
#     pygame.init()
#     Login.screen_width = 1280
#     Login.screen_height = 720
#     Login.screen = pygame.display.set_mode((Login.screen_width, Login.screen_height)) 
#     Login.clock = pygame.time.Clock()
#     soundbar.set_sound(0.5)
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#         s = Login.start_all()
#         while True:
#             n = make_menu(s) #list thong so game
#             print(n)
#             if n == -1:
#                 break
#             elif n == 0:
#                 continue
#             else:
#                 continue
#                 #play game [name, auto, hard, mode]
#                 #auto == 0 tu choi, auto == 1 bot choi
#                 #hard: 20,40,100
#                 #mode: 0,1,2 (normal, speed, limit)
    
