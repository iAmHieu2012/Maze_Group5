import pygame, sys
from pygame.locals import *

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
def write_screen(s: str, color, color2, vt, custom_font: int, DISPLAYSURF, size):
    if custom_font == 0:
        custom_font = pygame.font.Font('AttackGraffiti.ttf', size)
    elif custom_font == -1:
        custom_font = pygame.font.Font('Retolia.ttf', size)
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
    background = pygame.image.load('nice3.png')
    picture = pygame.transform.scale(background, (1280, 720))
    DISPLAYSURF.blit(picture, (0, 0))

    #textsys
    write_screen("Account: "+s, BLACK, YELLOW, (1280/2, 650), 1, DISPLAYSURF, 20)
    #textcus
    write_screen("MAZE", RED, None, (1280/2, 130), 0, DISPLAYSURF, 90)
    for i in range(8):
        pygame.draw.rect(DISPLAYSURF, YELLOW, (1280//2 - 200,i*50 + 220, 400, 50), 6) #ve bang chon
    pygame.draw.rect(DISPLAYSURF, RED, (1280//2 - 200, 0*50 + 220, 400, 50), 6)
    lst = ["PLAY", "AUTOPLAY", "LOAD GAME", "LEADERBOARD", "INSTRUCTION", "SETTINGS", "ABOUT", "LOG OUT"]
    for i in range(8):
        write_screen(lst[i], BLUE, None, (1280/2, i*50 + 245), -1, DISPLAYSURF, 26)
    pygame.display.update()
    return DISPLAYSURF

def make_sound(mode = 0):
    if mode == 0:
        sound_1 = 'mouse.wav'
    else:
        sound_1 = 'key.wav'
    sound_1 = pygame.mixer.Sound(sound_1)
    sound_1.play()

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

def make_dialog(DISPLAYSURF, s: str, mode = 0):
    pygame.draw.rect(DISPLAYSURF, WHITE, (1280//2 - 250, 300, 550, 240))
    pygame.draw.rect(DISPLAYSURF, BLUE, (1280//2 - 250, 300, 550, 40))
    write_screen(s, WHITE, None, (1280//2 - 240 + 80, 320), 1, DISPLAYSURF, 20)
    write_screen("  X  ", WHITE, RED, (1280//2 + 280, 320), -1, DISPLAYSURF, 20)
    if mode == 0:
        write_screen("LEVEL", BLACK, None, (1280//2 - 240 + 30, 380), -1, DISPLAYSURF, 20)
        lst = ["VIETNAM", "MEDIUM", " HARD "]
        for i in range(1, 4):
            write_screen(lst[i - 1], BLACK, CYAN, (1280//2 - 210 + 150 * i, 380), -1, DISPLAYSURF, 20)
        x = -1
        running = True
        hard = 0
        auto = 0
        vt = []
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
                            if temp == 0: hard = 20
                            elif temp == 1: hard = 40
                            else: hard = 100
                            runner = 1
            elif runner == 1:#choose position for Tom and Giahuy
                if lst[0] != "RANDOM":
                    x = -1
                    write_screen("POSITION", BLACK, None, (1280//2 - 240 + 40, 450), -1, DISPLAYSURF, 20)
                    pygame.time.delay(500)
                    lst = ["RANDOM", "CHOOSE"]
                    for i in range(1, 3):
                        write_screen(lst[i - 1], BLACK, CYAN, (1280//2 - 210 + 200 * i, 450), -1, DISPLAYSURF, 20)
                for event in pygame.event.get(): 
                    if event.type == pygame.MOUSEBUTTONUP:
                        make_sound()
                        tempx = pygame.mouse.get_pos()[0]
                        tempy = pygame.mouse.get_pos()[1]
                        temp = (tempx - 588)//200
                        if 900 < tempx < 940 and 302 < tempy < 340: #quit dialog
                            running = False
                            return -1
                        elif (-1 < temp < 2 and 430 < tempy < 470 and x!= temp):
                            x>-1 and write_screen(lst[x], BLACK, CYAN, (1280//2 - 210 + 200 * (x + 1), 450), -1, DISPLAYSURF, 20)
                            write_screen(lst[temp], BLACK, BROWN, (1280//2 - 210 + 200 * (temp + 1), 450), -1, DISPLAYSURF, 20)
                            x = temp
                        elif temp == x:
                            auto = temp
                            if (auto == 0): 
                                running = False
                                return [hard, auto, (-1,-1)]
                            runner = 2
            elif runner == 2: #choose exact position
                lst = ["Tom_x=", "Tom_y=", "Jerry_x=", "Jerry_y="]
                write_screen("ENTER POSITION : ", BLACK, None, (1280//2 - 240 + 80, 500), -1, DISPLAYSURF, 20)
                for i in range(4):
                    write_screen(lst[i], BLACK, None, (1280//2 - 240 + 150 + 100*i, 530), 1, DISPLAYSURF, 20)
                    x_t = rec_input(DISPLAYSURF, 600, 480)
                    if x_t == 1000:
                        running = False
                        return -1
                    vt.append(x_t)
                    write_screen(str(vt[i]), BLACK, None, (1280//2 - 240 + 200 + 100*i, 530), 1, DISPLAYSURF, 20)
                return [hard, 1, vt]
            pygame.display.update((380, 300, 600, 250))

    elif mode in (1, 2): #done sucess or failed
        while True:
            mode == 1 and write_screen("Press X to start playing! Hope u enjoy =^.^=", BLACK, None, (1280//2, 380), 1, DISPLAYSURF, 18)
            mode == 2 and write_screen("Check if the position have exceeded map's size", BLACK, None, (1280//2, 380), 1, DISPLAYSURF, 18)
            mode == 2 and write_screen("Or the distance beetween Tom and Jerry is too small", BLACK, None, (1280//2, 420), 1, DISPLAYSURF, 18)
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
        write_screen("BACKGROUND", BLACK, None, (1280//2 - 100, 380), -1, DISPLAYSURF, 20)
        write_screen("SOUND", BLACK, None, (1280//2 - 100, 480), -1, DISPLAYSURF, 20)
        temp = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    tempx = pygame.mouse.get_pos()[0]
                    tempy = pygame.mouse.get_pos()[1]
                    make_sound()
                    if 900 < tempx < 940 and 302 < tempy < 340:
                        return -1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        make_sound(1)
                        temp = 1 - temp
            if temp == 0:
                write_screen("<<  ON  >>", BLACK, WHITE, (1280//2 + 50, 480), -1, DISPLAYSURF, 20)
            else:
                write_screen("<<  OFF >>", BLACK, WHITE, (1280//2 + 50, 480), -1, DISPLAYSURF, 20)
            pygame.display.update((380, 300, 600, 250))

def make_menu(s: str):
    DISPLAYSURF = set_all('ss')
    clock = pygame.time.Clock()
    running = True
    y = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                make_sound()
                tempx = pygame.mouse.get_pos()[0]
                tempy = pygame.mouse.get_pos()[1]
                temp = (tempy - 220) // 50
                if (-1< temp < 8 and 1280//2 - 200 < tempx < 1280//2 + 200 and temp!=y):
                    pygame.draw.rect(DISPLAYSURF, RED, (1280//2 - 200, temp*50 + 220, 400, 50), 6)
                    pygame.draw.rect(DISPLAYSURF, YELLOW, (1280//2 - 200, y*50 + 220, 400, 50), 6)
                    y = temp
                elif temp == y > -1:
                    if (y == 7):
                        n = make_dialog(DISPLAYSURF, "Log out", 3)
                        if n == -1:
                            return 0
                        if n == 0:
                            running = False
                            return -1
                    elif (y == 0 or y == 1):
                        while True:
                            lst = make_dialog(DISPLAYSURF, "Choose mode to play", 0)
                            if lst == -1:
                                return 0
                            if lst[2] == (-1, -1):
                                hard = lst[0]
                                make_dialog(DISPLAYSURF, "Sucess: " + str(hard) + " x " + str(hard), 1)
                                #play_game
                                return 0
                            else:
                                hard = lst[0]
                                vt = lst[2]
                                if abs(vt[0] - vt[2]) + abs(vt[1] - vt[3]) >= hard and min(tuple(vt)) > 0 and max(tuple(vt)) <= hard:
                                    make_dialog(DISPLAYSURF, "Sucess: " + str(hard) + " x " + str(hard), 1)
                                    #play_game
                                    return 0
                                else:
                                    make_dialog(DISPLAYSURF, "Failed: " + str(hard) + " x " + str(hard), 2)
                    elif y == 5:
                        n = make_dialog(DISPLAYSURF, "SETTINGS", 4)
                        if n == -1:
                            return 0

            elif event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
        pygame.display.update((380, 200, 600, 450))

if __name__=="__main__":
    pygame.init()
    while True:
        n = make_menu("ss")
        print(n)
        if n == -1:
            break
    
