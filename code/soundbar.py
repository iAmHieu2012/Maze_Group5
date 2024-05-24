import pygame
import sys
def set_sound(volume):
    pygame.mixer.init()
    pygame.mixer.music.load('sound/ingame.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume)

def sound_all(screen):
    result = 1
    # Khởi tạo Pygame
    # pygame.init()
    # # pygame.mixer.init()

    SCREEN_WIDTH=1280
    SCREEN_HEIGHT=720
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

    #screen = pygame.display.set_mode(SCREEN_SIZE)

    font = pygame.font.Font('font/VNF-Comic Sans.ttf',30)
    bar =  font.render('________',True,'black')
    button=pygame.transform.scale(pygame.image.load('img/button.png'),(20, 20))
    background = pygame.image.load('img/background.jpg')
    picture = pygame.transform.scale(background, (1280, 720))
    # screen.blit(picture, (0, 0))
    x=SCREEN_WIDTH/2-button.get_width()/2
    mouse_held=False
    button_X = pygame.Rect((900, 302, 40, 38))

    # pygame.mixer.music.load('sound/ingame.mp3')
    # pygame.mixer.music.play(-1)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect((x, SCREEN_HEIGHT/2 + 100),(20, 20))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_X.collidepoint(mouse_pos):
                    running = False
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
        screen.fill('white')
        screen.blit(bar,(SCREEN_WIDTH/2-bar.get_width()/2, SCREEN_HEIGHT/2 + 75))
        screen.blit(button,(x, SCREEN_HEIGHT/2 + 100))
        pygame.display.update((SCREEN_WIDTH/2-bar.get_width()/2 - 10, SCREEN_HEIGHT/2 + 60, 250, 100))

    # pygame.quit()
    # sys.exit()
