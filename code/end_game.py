import pygame
import sys

#result = 1 nếu thắng và 0 nếu thua
def End_game(result = 0):
    # Khởi tạo Pygamepygame.init()
    
    # pygame.mixer.init()

    SCREEN_WIDTH=1280
    SCREEN_HEIGHT=720
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

    screen = pygame.display.set_mode(SCREEN_SIZE)

    tom_bg=pygame.transform.scale(pygame.image.load('img/tom.jpg'),SCREEN_SIZE)
    jerry_bg=pygame.transform.scale(pygame.image.load('img/jerry.jpg'),SCREEN_SIZE)

    font = pygame.font.Font('font/custom_font.ttf',96)
    Font = pygame.font.Font('font/custom_font.ttf',128)
    TOM_WIN=Font.render('TOM WIN',True,'blue')
    JERRY_WIN=Font.render('JERRY WIN',True,'yellow')
    YES=Font.render('YES',True,'red')
    NO=font.render('NO',True,'black')
    YES_rect = pygame.Rect(SCREEN_WIDTH/3-YES.get_width()//2,SCREEN_HEIGHT*6/9-YES.get_height()//2,YES.get_width(),YES.get_height())
    NO_rect = pygame.Rect(SCREEN_WIDTH*2/3-NO.get_width()//2,SCREEN_HEIGHT*6/9-NO.get_height()//2,NO.get_width(),NO.get_height())
    choice=1
    change=1

    if result == 1:
        pygame.mixer.music.load('sound/win.mp3')
        pygame.mixer.music.play()
    else :
        pygame.mixer.music.load('sound/lose.mp3')
        pygame.mixer.music.play()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    choice=0
                elif event.key == pygame.K_LEFT:
                    choice=1
                elif event.key == pygame.K_RETURN:
                    running = False
                    print(choice)
                    return choice
                elif event.key == pygame.K_SPACE:
                    result=1-result
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if YES_rect.collidepoint(pygame.mouse.get_pos()) or NO_rect.collidepoint(pygame.mouse.get_pos()):
                        print(choice)
                        running = False
                        return choice
        
        screen.fill((255, 255, 255))
        
        if change != choice:
            pygame.mixer.music.load('sound/mouse_new.wav')
            pygame.mixer.music.play()
        change = choice
        
        # Kiểm tra xem con trỏ chuột có nằm trong vùng YES/NO không
        mouse_pos = pygame.mouse.get_pos()
        if YES_rect.collidepoint(mouse_pos):
            choice=1
        elif NO_rect.collidepoint(mouse_pos):
            choice=0
        
        if choice==1:
            YES=Font.render('YES',True,'red')
            NO=font.render('NO',True,'black')
        elif choice==0 :
            NO=Font.render('NO',True,'red')
            YES=font.render('YES',True,'black')
        
        if result ==1 :
            screen.blit(tom_bg,(0,0))
            PLAY_AGAIN=Font.render('PLAY AGAIN?', True, 'blue')
            screen.blit(TOM_WIN,(SCREEN_WIDTH/2-TOM_WIN.get_width()/2,SCREEN_HEIGHT*2/9-TOM_WIN.get_height()/2))
        else :
            screen.blit(jerry_bg,(0,0))
            PLAY_AGAIN=Font.render('PLAY AGAIN?', True, 'yellow')
            screen.blit(JERRY_WIN,(SCREEN_WIDTH/2-JERRY_WIN.get_width()/2,SCREEN_HEIGHT*2/9-JERRY_WIN.get_height()/2))
        
        screen.blit(YES,(SCREEN_WIDTH/3-YES.get_width()//2,SCREEN_HEIGHT*6/9-YES.get_height()//2))
        screen.blit(NO,(SCREEN_WIDTH*2/3-NO.get_width()//2,SCREEN_HEIGHT*6/9-NO.get_height()//2))
        screen.blit(PLAY_AGAIN,(SCREEN_WIDTH/2-PLAY_AGAIN.get_width()/2,SCREEN_HEIGHT*4/9-PLAY_AGAIN.get_height()/2))
            
        pygame.display.flip()


# pygame.quit()
# sys.exit()
