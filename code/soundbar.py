import pygame
import sys
def set_sound(volume):
    pygame.mixer.init()
    pygame.mixer.music.load('sound/ingame.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume)

def sound_all(screen, x_button_rect, logbox, logbox_rect):
    result = 1
    # Khởi tạo Pygame
    # pygame.init()
    # # pygame.mixer.init()

    SCREEN_WIDTH=850
    SCREEN_HEIGHT=720
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

    #screen = pygame.display.set_mode(SCREEN_SIZE)

    font = pygame.font.Font('font/VNF-Comic Sans.ttf',40)
    bar =  font.render('________',True,'black')
    button=pygame.transform.scale(pygame.image.load('img/button.png'),(40, 40))
    # screen.blit(picture, (0, 0))
    x=SCREEN_WIDTH/2-button.get_width()/2
    mouse_held=False
    button_X = x_button_rect

    # pygame.mixer.music.load('sound/ingame.mp3')
    # pygame.mixer.music.play(-1)

    running = True
    while running:
        screen.blit(logbox,logbox_rect)
        screen.blit(bar,(SCREEN_WIDTH/2-bar.get_width()/2, SCREEN_HEIGHT/2 + 75))
        screen.blit(button,(x, SCREEN_HEIGHT/2 + 100))
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect((x, SCREEN_HEIGHT/2 + 100),(20, 20))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_X.collidepoint(mouse_pos):
                    running = False
                    return -1
                elif event.button == 1:
                    if button_rect.collidepoint(mouse_pos):
                        mouse_held=True
                    else: running = False
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
        pygame.display.flip()
        # pygame.display.update(pygame.rect.Rect(SCREEN_WIDTH/2-bar.get_width()/2-button.get_width()/2, SCREEN_HEIGHT/2 + 100,bar.get_width()+button.get_width(),button.get_height()))
    return button_rect
    # pygame.quit()
    # sys.exit()
