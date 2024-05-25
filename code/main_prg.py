#from create_maze import *
from end_game import *
#from main_code import *
import Login
from Make_menu import *
import subprocess

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    Login.screen_width = 1280
    Login.screen_height = 720
    Login.screen = pygame.display.set_mode((Login.screen_width, Login.screen_height)) 
    Login.clock = pygame.time.Clock()
    pygame.display.set_caption('Tom and Jerry')
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
            #print(n)
            if n == -1:
                break
            elif n == 0:
                continue
            else:
                while True:
                    inp = open('mode.txt', 'w')
                    for i in range(len(n)):
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
            
                
