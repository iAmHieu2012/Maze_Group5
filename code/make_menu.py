import pygame, sys
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

        pygame.display.update()
        clock.tick(30)

def make_dialog(DISPLAYSURF, s: str, mode = 0, auto = 0):
    logbox = pygame.image.load('img/log.png').convert_alpha()
    logbox = pygame.transform.scale(logbox, (560, 400))
    logbox_rect = logbox.get_rect()
    logbox_rect.topleft = (1280//2 - 500, 200)
    x_button = pygame.image.load('img/xbutton.png').convert_alpha()
    x_button = pygame.transform.scale(x_button, (60, 60))    
    tick_button = pygame.image.load('img/tickbutton.png').convert_alpha()
    tick_button = pygame.transform.scale(tick_button, (60, 60))
    modebox = pygame.image.load('img/modebox.png').convert_alpha()
    modebox = pygame.transform.scale(modebox, (140,50))
    modebox_pressed = pygame.image.load('img/modeboxpressed.png').convert_alpha()
    modebox_pressed = pygame.transform.scale(modebox_pressed, (140,50))
    DISPLAYSURF.blit(logbox, logbox_rect)
    DISPLAYSURF.blit(x_button, (1280//2+50, 200))
    # pygame.draw.rect(DISPLAYSURF, WHITE, (1280//2 - 250, 300, 550, 240))
    # pygame.draw.rect(DISPLAYSURF, BLUE, (1280//2 - 250, 300, 550, 40))
    write_screen(s, GRAY, None, (1280//2 - 270, 250), -1, DISPLAYSURF, 30)
    # write_screen("  X  ", WHITE, RED, (1280//2 + 80, 320), -1, DISPLAYSURF, 20)
    x_button_rect = x_button.get_rect()
    x_button_rect.topleft = (1280//2+50, 200)
    tick_button_rect = tick_button.get_rect()
    tick_button_rect.center = (logbox_rect.centerx, logbox_rect.bottom)
    if mode == 0:
        DISPLAYSURF.blit(tick_button, (logbox_rect.centerx-30, logbox_rect.bottom-30))
        write_screen("LEVEL", BLACK, None, (1280//2 - 430, 320), -1, DISPLAYSURF, 20)
        lst = ["EASY", "MEDIUM", " HARD "]
        lst_level_rect = []
        for i in range(1, 4):
            DISPLAYSURF.blit(modebox, (1280//2 - 590 + 150 * i, 355))
            lst_level_rect.append(pygame.rect.Rect(1280//2 - 590 + 150 * i, 355,140,50))
            write_screen(lst[i - 1], BLACK, None, (1280//2 - 520 + 150 * i, 380), -1, DISPLAYSURF, 20)
        running = True
        hard = -1
        gm = -1
        if auto == 1:
            while running:
                mousePos = pygame.mouse.get_pos()
                for item in lst_level_rect:
                    if item.collidepoint(mousePos):
                        x1 = lst_level_rect.index(item)
                        break
                else: x1=-1
                for event in pygame.event.get(): 
                    if event.type == pygame.MOUSEBUTTONUP:
                        make_sound()
                        if x1 > -1:
                            for i in range(1, 4):
                                DISPLAYSURF.blit(modebox, (1280//2 - 590 + 150 * i, 355))
                                write_screen(lst[i - 1], BLACK, None, (1280//2 - 520 + 150 * i, 380), -1, DISPLAYSURF, 20)
                            DISPLAYSURF.blit(modebox_pressed, (1280//2 - 590 + 150 * (x1+1), 355))
                            write_screen(lst[x1], BLACK, None, (1280//2 - 520 + 150 * (x1+1), 380), -1, DISPLAYSURF, 20)
                            if x1 == 0: hard = 20
                            elif x1 == 1: hard = 40
                            else: hard = 100
                            player_choice =  [hard, 4]
                        if tick_button_rect.collidepoint(mousePos) and player_choice != []:
                            running = False
                            return player_choice
                        if x_button_rect.collidepoint(mousePos): #quit dialog
                            running = False
                            player_choice = []
                            return -1
                pygame.display.update()

        if auto == 0:
            write_screen("MODE", BLACK, None, (1280//2 - 430, 450), -1, DISPLAYSURF, 20)
            # pygame.time.delay(500)
            lstmode = ["NORMAL", "SPEEDRUN", "LIMIT"]
            lst_mode_rect = []
            for i in range(1, 4):
                DISPLAYSURF.blit(modebox, (1280//2 - 590 + 150 * i, 485))
                lst_mode_rect.append(pygame.rect.Rect(1280//2 - 590 + 150 * i, 485,140,50))
                write_screen(lstmode[i - 1], BLACK, None, (1280//2 - 520 + 150 * i, 510), -1, DISPLAYSURF, 20)
                
        player_choice = []
        x1 = -1
        x2 = -1
        x1_hover = -1
        x2_hover = -1
        while running:
            mousePos = pygame.mouse.get_pos()
            for item in lst_level_rect:
                if item.collidepoint(mousePos):
                    x1_hover = lst_level_rect.index(item)
                    break
            else: x1_hover = -1
            for item in lst_mode_rect:
                if item.collidepoint(mousePos):
                    x2_hover = lst_mode_rect.index(item)
                    break
            else: x2_hover = -1
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONUP:
                    make_sound()
                    if x1_hover > -1:
                        x1 = x1_hover
                        for i in range(1, 4):
                            DISPLAYSURF.blit(modebox, (1280//2 - 590 + 150 * i, 355))
                            write_screen(lst[i - 1], BLACK, None, (1280//2 - 520 + 150 * i, 380), -1, DISPLAYSURF, 20)
                        DISPLAYSURF.blit(modebox_pressed, (1280//2 - 590 + 150 * (x1+1), 355))
                        write_screen(lst[x1], BLACK, None, (1280//2 - 520 + 150 * (x1+1), 380), -1, DISPLAYSURF, 20)
                    if x1 == 0: hard = 20
                    elif x1 == 1: hard = 40
                    else: hard = 100
                    player_choice = [hard, gm]
                    if x2_hover>-1:
                        x2 = x2_hover
                        for i in range(1, 4):
                            DISPLAYSURF.blit(modebox, (1280//2 - 590 + 150 * i, 485))
                            write_screen(lstmode[i - 1], BLACK, None, (1280//2 - 520 + 150 * i, 510), -1, DISPLAYSURF, 20)
                        DISPLAYSURF.blit(modebox_pressed, (1280//2 - 590 + 150 * (x2+1), 485))
                        write_screen(lstmode[x2], BLACK, None, (1280//2 - 520 + 150 * (x2+1), 510), -1, DISPLAYSURF, 20)
                    if x2 == 0: gm = 0
                    elif x2 == 1: gm = 1
                    else: gm =2
                    player_choice = [hard, gm]
                    if tick_button_rect.collidepoint(mousePos) and (-1 not in player_choice):
                        running = False
                        return player_choice
                    if x_button_rect.collidepoint(mousePos): #quit dialog
                        running = False
                        player_choice = []
                        return -1
            pygame.display.update()

    elif mode == 1: #done sucess or failed
        while True:
            write_screen("Hope u enjoy!", BLACK, None, (1280//2 - 230, 450), -1, DISPLAYSURF, 50)
            pygame.display.update()
            pygame.time.delay(1000)
            return
            # for event in pygame.event.get(): 
            #     if event.type == pygame.MOUSEBUTTONUP:
            #         make_sound()
            #         if pygame.mouse.get_pressed()[0]:
                        # return
            # pygame.time.delay(1000)

    elif mode == 3:#quit game
        write_screen("Do u really want to log out?", BLACK, None, (1280//2 - 250, 380), -1, DISPLAYSURF, 30)
        lst = ["SURE","NO"]
        lst_rect = []
        for i in range(1,3):
            DISPLAYSURF.blit(modebox, (1280//2 - 590 + 200 * i, 500))
            lst_rect.append(pygame.rect.Rect(1280//2 - 590 + 200 * i, 500,140,50))
            write_screen(lst[i - 1], BLACK, None, (1280//2 - 520 + 200 * i, 525), -1, DISPLAYSURF, 20)
        while True:
            mousePos = pygame.mouse.get_pos()
            for item in lst_rect:
                x = lst_rect.index(item)
                if item.collidepoint(mousePos):
                    DISPLAYSURF.blit(modebox_pressed, (1280//2 - 590 + 200 * (x+1), 500))
                    write_screen(lst[x], BLACK, None, (1280//2 - 520 + 200 * (x+1), 525), -1, DISPLAYSURF, 20)
                else:
                    DISPLAYSURF.blit(modebox, (1280//2 - 590 + 200 * (x+1), 500))
                    write_screen(lst[x], BLACK, None, (1280//2 - 520 + 200 * (x+1), 525), -1, DISPLAYSURF, 20)
                    
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONUP:
                    make_sound()
                    if x_button_rect.collidepoint(mousePos) or lst_rect[1].collidepoint(mousePos): #quit dialog
                        return -1
                    elif lst_rect[0].collidepoint(mousePos):
                        return 0
            pygame.display.update()

    elif mode == 4:#setting
        write_screen(" KEY ", BLACK, None, (1280//2 - 240 + 30, 525), -1, DISPLAYSURF, 20)
        lst = ["AWSD", "ARROWKEY"]
        lst_rect = []
        for i in range(1, 3):
            DISPLAYSURF.blit(modebox, (1280//2 - 590 + 200 * i, 355))
            lst_rect.append(pygame.rect.Rect(1280//2 - 590 + 200 * i, 355,140,50))
            write_screen(lst[i - 1], BLACK, None, (1280//2 - 520 + 200 * i, 380), -1, DISPLAYSURF, 20)
        x = -1
        running = True
        key_mode = 0
        buttonrect = soundbar.sound_all(DISPLAYSURF,x_button_rect,logbox,logbox_rect)
        if buttonrect == -1:
            return -1
        while running:
            for i in range(1, 3):
                if not i - 1 ==x:
                    DISPLAYSURF.blit(modebox, (1280//2 - 590 + 200 * i, 355))
                    write_screen(lst[i - 1], BLACK, None, (1280//2 - 520 + 200 * i, 380), -1, DISPLAYSURF, 20)
                        
                else:        
                    DISPLAYSURF.blit(modebox_pressed, (1280//2 - 590 + 200 * i, 355))
                    write_screen(lst[i-1], BLACK, None, (1280//2 - 520 + 200 * i, 380), -1, DISPLAYSURF, 20)
            mousePos = pygame.mouse.get_pos()
            for item in lst_rect:
                if item.collidepoint(mousePos):
                    x = lst_rect.index(item)
                    if pygame.mouse.get_pressed()[0]:
                        fp = open('current_account.txt', 'r')
                        username = fp.readline().strip("\n")
                        fp.close()
                        f=  open("current_account.txt","w")
                        f.write(username)
                        f.write("\n")
                        f.write(str(x))
                        f.close()   
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONUP:
                    make_sound()
                    if x>-1:
                        for i in range(1, 3):
                            DISPLAYSURF.blit(modebox, (1280//2 - 590 + 200 * i, 355))
                            write_screen(lst[i - 1], BLACK, None, (1280//2 - 520 + 200 * i, 380), -1, DISPLAYSURF, 20)
                        DISPLAYSURF.blit(modebox_pressed, (1280//2 - 590 + 200 * (x+1), 355))
                        write_screen(lst[x], BLACK, None, (1280//2 - 520 + 200 * (x+1), 380), -1, DISPLAYSURF, 20)
                    if x_button_rect.collidepoint(mousePos):
                        running = False
                        return -1
                    if tick_button_rect.collidepoint(mousePos): 
                        return (key_mode, -1)
            if buttonrect.collidepoint(mousePos):
                return make_dialog(DISPLAYSURF,s,4)
            pygame.display.update()

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
        y = -1
        while running:
            mousePos = pygame.mouse.get_pos()
            for item in collide_rect_list:
                if item.collidepoint(mousePos):
                    DISPLAYSURF.blit(textbox_p, (item[0],item[1]))
                    write_screen(lst[collide_rect_list.index(item)], GRAY, None, (1280/2-300, collide_rect_list.index(item)*50 + 245), -1, DISPLAYSURF, 24)
                    y = collide_rect_list.index(item)
                else:
                    DISPLAYSURF.blit(textbox, (item[0],item[1]))
                    write_screen(lst[collide_rect_list.index(item)], WHITE, None, (1280/2-300, collide_rect_list.index(item)*50 + 245), -1, DISPLAYSURF, 24)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    make_sound()
                    if y > -1:
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
                            return 5
                        
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
    
