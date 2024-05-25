from end_game import *
import Login
from make_menu import *
import subprocess

def reset_record(username : str):
    filename = 'player_record/' + username + '.txt'
    fp = open(filename, 'w')
    fp.write('150 150 150 0 0 0')
    fp.close()

def get_record(username : str):
    filename = 'player_record/' + username + '.txt'
    try:
        fp = open(filename, 'r')
        recordList = list(map(int, fp.readline().split()))
        fp.close()
        return recordList
    except:
        reset_record(username)
        get_record(username)

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
        fp1.write(s)
        fp1.close()

        # open('current_record.txt', 'w').close()
        # fp2 = open('current_record.txt', 'w')
        # recordList = get_record(s)
        # for i in range(len(recordList)):
        #     fp2.write(str(recordList[i]) + ' ')
        # fp2.close()
        while True:
            soundbar.set_sound(pygame.mixer.music.get_volume())
            n = make_menu(s) #list thong so game
            if n == -1:
                break
            elif n == 0:
                continue
            # elif n == 2:
            #     subprocess.run(['python', 'load_game.py'])
            #     result = open('result.txt', 'r')
            #     temp = int(result.read(2))
            #     result.close()
            #     if temp == -1:
            #         break
            #     if End_game(temp) == 0:
            #         soundbar.set_sound(pygame.mixer.music.get_volume())
            #         break
            #     else:
            #         soundbar.set_sound(pygame.mixer.music.get_volume())
            #         continue
            elif n == 3:
                subprocess.run(['python', 'code/leaderboard.py'])
            elif n == 4:
                subprocess.run(['python', 'code/instruction.py'])
            elif n == 6:
                subprocess.run(['python', 'code/about.py'])
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
            
                
