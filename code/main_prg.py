from end_game import *
import Login
from make_menu import *
import subprocess

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    Login.screen_width = 1280
    Login.screen_height = 720
    Login.screen = pygame.display.set_mode((Login.screen_width, Login.screen_height)) 
    Login.clock = pygame.time.Clock()
    pygame.display.set_caption('Tom and Jerry')
    img = pygame.image.load('img/maze_icon.png')
    pygame.display.set_icon(img)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        s = Login.start_all()

        open('current_account.txt', 'w').close()
        fp1 = open('current_account.txt', 'w')
        fp1.writelines(s)
        fp1.close()

        while True:
            soundbar.set_sound(pygame.mixer.music.get_volume())
            n = make_menu(s) #list thong so game
            if n == -1:
                break
            elif n == 0:
                continue
            elif n == 2:
                subprocess.run(['python', 'load_game.py'])
                result = open('result.txt', 'r')
                temp = int(result.read(2))
                result.close()
                if temp == -1:
                    break
                if End_game(temp) == 0:
                    soundbar.set_sound(pygame.mixer.music.get_volume())
                    break
                else:
                    soundbar.set_sound(pygame.mixer.music.get_volume())
                    continue
            elif n == 4:
                subprocess.run(['python', 'code/instruction.py'])
            elif n == 6:
                subprocess.run(['python', 'code/about.py'])
            else:
                while True:
                    inp = open('mode.txt', 'w')
                    for i in range(4):
                        inp.write(str(n[i]) + '\n')
                    inp.close() 
                    subprocess.run(["python", "code/main_code.py"])
                    result = open('result.txt', 'r')
                    temp = int(result.read(2))
                    result.close()
                    if temp == -1:
                        break
                    if End_game(temp) == 0:
                        soundbar.set_sound(pygame.mixer.music.get_volume())
                        break
                    else:
                        soundbar.set_sound(pygame.mixer.music.get_volume())
                        continue
            
                
