from create_maze import *
from algorithm import *
from make_menu import *
from main_prg import reset_record, get_record

from main_prg import reset_record, get_record


FPS = 60
pygame.init()
pygame.mixer.init()
game_surface = pygame.Surface(RES)
pause_surface = pygame.Surface((WIDTH + 300, HEIGHT))
end_game_surface = pygame.Surface((WIDTH + 300, HEIGHT))
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()

# images
bg_game = pygame.image.load("img/background.jpg").convert()
bg_game = pygame.transform.scale(bg_game, (WIDTH, HEIGHT))
bg_pause = pygame.image.load("img/bg_pause.png").convert()
bg = pygame.image.load("img/bg_main.jpg").convert()

# game icon
pygame.display.set_caption("Maze")
pygame_icon = pygame.image.load("img/maze_icon.png")
pygame.display.set_icon(pygame_icon)
nums_food = 0
# take level and mode from mode.txt
inp = open('mode.txt', 'r')
lst = inp.readlines()
inp.close()
if int(lst[1]) == 1:
    auto =1
else: auto =0
if int(lst[1]) != 2:
    game_level = int(lst[2])
    game_mode = int(lst[3])

    #Set level
    if game_level == 20:
        create_maze.TILE = 60
        create_maze.cols, create_maze.rows = create_maze.WIDTH // 60, create_maze.HEIGHT // 60
        algorithm.MODE = 50
        create_maze.THICK = 4
        nums_food = 10
    elif game_level == 40:
        create_maze.TILE = 40
        create_maze.cols, create_maze.rows = create_maze.WIDTH // 40, create_maze.HEIGHT // 40
        algorithm.MODE = 50
        create_maze.THICK = 2
        nums_food = 30
    elif game_level == 100:
        create_maze.TILE = 20
        create_maze.cols, create_maze.rows = create_maze.WIDTH // 20, create_maze.HEIGHT // 20
        create_maze.THICK = 2
        algorithm.MODE = 300
        nums_food = 60

class Food:
    def __init__(self):
        self.img = pygame.image.load("img/cheese.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (create_maze.TILE - 10, create_maze.TILE - 10))
        self.rect = self.img.get_rect()
        self.set_pos()

    def set_pos(self):
        self.rect.topleft = randrange(create_maze.cols) * create_maze.TILE + 5, randrange(create_maze.rows) * create_maze.TILE + 5

    def draw(self):
        game_surface.blit(self.img, self.rect)

class Button:
    def __init__(self, img_path, col, row):
        self.img = pygame.image.load(img_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (60, 60))
        self.rect = self.img.get_rect()
        self.rect.topleft = (col, row)
        self.pos = (col,row)
    
    def draw(self,sc):
        sc.blit(self.img, self.rect)

def is_collide(x, y, walls_collide_list, player_rect):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True

def eat_food():
    for food in food_list:
        if player_rect.collidepoint(food.rect.center):
            food.set_pos()
            return True
    return False

def is_game_over():
    global time, score, FPS
    if time < 0:
        pygame.time.wait(700)
        [food.set_pos() for food in food_list]
        time, score, FPS = 150, 0, 60
        return False

def new_game():
    # get maze
    maze = create_maze.generate_maze()
    maze = generateTomAndJerryPos(maze)
    maze2D = getMaze2DArray(maze)

    # get Jerry position
    AimPos = findTomAndJerryPos(maze2D)[1]

    # get Tom position
    CurrentPos = findTomAndJerryPos(maze2D)[0]

    player_rect.topleft = (
        CurrentPos[1] * create_maze.TILE + create_maze.THICK,
        CurrentPos[0] * create_maze.TILE + create_maze.THICK,
    )
    
    des_rect.topleft = (
        AimPos[1] * create_maze.TILE + create_maze.THICK,
        AimPos[0] * create_maze.TILE + create_maze.THICK,
    )
    walls_collide_list = sum(
        [cell.get_rects() for cell in maze],
        [
            pygame.Rect(0, 0, create_maze.TILE * create_maze.cols, create_maze.THICK),
            pygame.Rect(0, 0, create_maze.THICK, create_maze.TILE * create_maze.rows),
            pygame.Rect(create_maze.cols * create_maze.TILE - create_maze.THICK, 0, create_maze.THICK, create_maze.TILE * create_maze.rows),
            pygame.Rect(0, create_maze.rows * create_maze.TILE - create_maze.THICK, create_maze.TILE * create_maze.cols, create_maze.THICK)
        ]
    )
    lastpos = (-1, -1)
    food_list = [Food() for i in range(nums_food)]
    return maze, maze2D, walls_collide_list, player_rect.topleft,des_rect.topleft, lastpos, CurrentPos, AimPos, food_list

#phần save game
def create_user_saved_game(username : str):
    # get Jerry position
    AimPos = findTomAndJerryPos(maze2D)[1]
    # get Tom position
    CurrentPos = get_player_current_cell()

    filename = 'saved_game/' + username + '.txt'
    # open(filename, 'w').close()
    try:
        fp = open(filename, 'w')
        fp.write(str(game_mode)+'\n')
        fp.write(str(game_level) + '\n')
        fp.write(str(AimPos[0])+" "+str(AimPos[1])+'\n')
        fp.write(str(CurrentPos[0])+" "+str(CurrentPos[1])+'\n')
        if game_mode == 1:
            fp.write(str(time) + '\n')

        if game_mode == 2:
            fp.write(str(time) + '\n')
            fp.write(str(score) + '\n')

        for cell in maze:
            fp.write(str(cell.y))
            fp.write(' ')
            fp.write(str(cell.x))
            fp.write('\n')
            for wall,status in cell.walls.items():
                if status == False:
                    fp.write('0 ')
                else:
                    fp.write('1 ')
            fp.write('\n')  
        fp.close()
    except:
        f = open(filename, 'w')
        f.close()
        create_user_saved_game(username)


# Phần load game:
def read_saved_game(username : str):
    filename = 'saved_game/' + username + '.txt'
    try:
        fp = open(filename, 'r')
    except: return None
    game_mode = int(fp.readline())
    game_level = int(fp.readline())
    #Vị trí Jerry
    AimPos = tuple(map(int,fp.readline().split()))
    #Vị trí Tom
    CurrentPos = tuple(map(int,fp.readline().split()))
    if game_mode == 1:
        time = int(fp.readline())
        score = 0
    elif game_mode == 2:
        time = int(fp.readline())
        score = int(fp.readline())
    else:
        time = 0
        score = 0
    maze = []
    #Set level
    if game_level == 20:
        create_maze.TILE = 60
        create_maze.cols, create_maze.rows = create_maze.WIDTH // 60, create_maze.HEIGHT // 60
        algorithm.MODE = 50
        create_maze.THICK = 4
        nums_food = 10
    elif game_level == 40:
        create_maze.TILE = 40
        create_maze.cols, create_maze.rows = create_maze.WIDTH // 40, create_maze.HEIGHT // 40
        algorithm.MODE = 50
        create_maze.THICK = 2
        nums_food = 30
    elif game_level == 100:
        create_maze.TILE = 20
        create_maze.cols, create_maze.rows = create_maze.WIDTH // 20, create_maze.HEIGHT // 20
        create_maze.THICK = 2
        algorithm.MODE = 300
        nums_food = 60
    for i in range(create_maze.cols* create_maze.rows):
        row, col = tuple(map(int,fp.readline().split()))
        cell = Cell(col,row)
        temp_walls = fp.readline().split()
        for item in range(4):
            if item ==0:
                cell.walls['top'] = False if temp_walls[item] == "0" else True
            if item ==1:
                cell.walls['right'] = False if temp_walls[item] == "0" else True
            if item ==2:
                cell.walls['bottom'] = False if temp_walls[item] == "0" else True
            if item ==3:
                cell.walls['left'] = False if temp_walls[item] == "0" else True
        maze.append(cell)
    maze2D = getMaze2DArray(maze)
    maze2D[AimPos[0]][AimPos[1]].make_jerry_pos()
    maze2D[CurrentPos[0]][CurrentPos[1]].make_tom_pos()
    maze = list(maze2D.flatten())
    return game_mode, game_level, AimPos, CurrentPos, maze, time, score
           
def load_game(username: str):
    if read_saved_game(username) == None:
        return None
    game_mode, game_level, AimPos, CurrentPos, maze, time, score = read_saved_game(username)
    maze2D = getMaze2DArray(maze)
    #Set level
    if game_level == 20:
        create_maze.TILE = 60
        create_maze.cols, create_maze.rows = create_maze.WIDTH // 60, create_maze.HEIGHT // 60
        algorithm.MODE = 50
        create_maze.THICK = 4
        nums_food = 10
    elif game_level == 40:
        create_maze.TILE = 40
        create_maze.cols, create_maze.rows = create_maze.WIDTH // 40, create_maze.HEIGHT // 40
        algorithm.MODE = 50
        create_maze.THICK = 2
        nums_food = 30
    elif game_level == 100:
        create_maze.TILE = 20
        create_maze.cols, create_maze.rows = create_maze.WIDTH // 20, create_maze.HEIGHT // 20
        create_maze.THICK = 2
        algorithm.MODE = 300
        nums_food = 60
    walls_collide_list = sum(
        [cell.get_rects() for cell in maze],
        [
            pygame.Rect(0, 0, create_maze.TILE * create_maze.cols, create_maze.THICK),
            pygame.Rect(0, 0, create_maze.THICK, create_maze.TILE * create_maze.rows),
            pygame.Rect(create_maze.cols * create_maze.TILE - create_maze.THICK, 0, create_maze.THICK, create_maze.TILE * create_maze.rows),
            pygame.Rect(0, create_maze.rows * create_maze.TILE - create_maze.THICK, create_maze.TILE * create_maze.cols, create_maze.THICK)
        ]
    )
    return maze, maze2D, walls_collide_list, CurrentPos, AimPos, time, score, game_mode, game_level
    
# # get maze
# maze = create_maze.generate_maze()
# maze = generateTomAndJerryPos(maze)
# maze2D = getMaze2DArray(maze)

# # get Jerry position
# AimPos = findTomAndJerryPos(maze2D)[1]

# # get Tom position
# CurrentPos = findTomAndJerryPos(maze2D)[0]

# player settings
player_speed = 5  # TILE must be divided by player_speed
player_img = pygame.image.load("img/tomface.png").convert_alpha()
player_img = pygame.transform.scale(
    player_img, (create_maze.TILE - 2 * create_maze.THICK, create_maze.TILE - 2 * create_maze.THICK)
)
player_rect = player_img.get_rect()
# player_rect.topleft = (
#     CurrentPos[1] * create_maze.TILE + create_maze.THICK,
#     CurrentPos[0] * create_maze.TILE + create_maze.THICK,
# )

# destination settings
des_img = pygame.image.load("img/jerryface.png").convert_alpha()
des_img = pygame.transform.scale(
    des_img, (create_maze.TILE - 2 * create_maze.THICK, create_maze.TILE - 2 * create_maze.THICK)
)
des_rect = des_img.get_rect()
# des_rect.topleft = (
#     AimPos[1] * create_maze.TILE + create_maze.THICK,
#     AimPos[0] * create_maze.TILE + create_maze.THICK,
# )
maze, maze2D, walls_collide_list, player_rect.topleft,des_rect.topleft, lastpos, CurrentPos, AimPos, food_list = new_game()
#hint
hint_img = pygame.image.load("img/star.png").convert_alpha()
hint_img = pygame.transform.scale(
    hint_img, (create_maze.TILE - 2 * create_maze.THICK, create_maze.TILE - 2 * create_maze.THICK)
)
hint_rect = hint_img.get_rect()

directions = {
    "a": (-player_speed, 0),
    "d": (player_speed, 0),
    "w": (0, -player_speed),
    "s": (0, player_speed),
}
fp = open('current_account.txt', 'r')
username = fp.readline().strip("\n")
typekeys = int(fp.readline())
fp.close()
if typekeys == 0:
    keys = {"a": pygame.K_a, "d": pygame.K_d, "w": pygame.K_w, "s": pygame.K_s}
elif typekeys ==1:
    keys = {"a": pygame.K_LEFT, "d": pygame.K_RIGHT, "w": pygame.K_UP, "s": pygame.K_DOWN}
direction = (0, 0)

def get_way_between_2point(currp, nextp, maze2D):
    if currp[0] == nextp[0]:
        if (currp[1]+1 == nextp[1]) and not maze2D[currp].walls['right'] and not maze2D[nextp].walls['left']:
            return 'd'
        if (currp[1]-1== nextp[1]) and not maze2D[currp].walls['left'] and not maze2D[nextp].walls['right']:
            return 'a'
    if currp[1] == nextp[1]:
        if (currp[0]+1== nextp[0]) and not maze2D[currp].walls['bottom'] and not maze2D[nextp].walls['top']:
            return 's'
        if (currp[0]-1== nextp[0]) and not maze2D[currp].walls['top'] and not maze2D[nextp].walls['bottom']:
            return 'w'  
    return None          
    
def pause_game(auto=0):
    surface.blit(pause_surface,(0,0))
    pause_surface.blit(bg_pause, (0,0))
    pause_surface.blit(text_font.render("CONTINUE?", True, pygame.Color("white")), (880, 400))
    play_button.draw(pause_surface)
    home_button.draw(pause_surface)
    if pygame.mouse.get_pressed()[0]:
        if play_button.rect.collidepoint(pygame.mouse.get_pos()):
            return 0
        if auto != 0:
            if home_button.rect.collidepoint(pygame.mouse.get_pos()):
                return 1
        else:
            if home_button.rect.collidepoint(pygame.mouse.get_pos()):
                write_screen('Leave Game', GRAY, None, (1280//2 - 270, 250), -1, surface, 30)
                logbox = pygame.image.load('img/log.png').convert_alpha()
                logbox = pygame.transform.scale(logbox, (560, 400))
                logbox_rect = logbox.get_rect()
                logbox_rect.topleft = (1280//2 - 500, 200)
                modebox = pygame.image.load('img/modebox.png').convert_alpha()
                modebox = pygame.transform.scale(modebox, (140,50))
                modebox_pressed = pygame.image.load('img/modeboxpressed.png').convert_alpha()
                modebox_pressed = pygame.transform.scale(modebox_pressed, (140,50))
                surface.blit(logbox, logbox_rect)
                write_screen("Do u wanna save your game?", BLACK, None, (1280//2 - 250, 380), -1, surface, 30)
                lst = ["SURE","NO"]
                lst_rect = []
                for i in range(1,3):
                    surface.blit(modebox, (1280//2 - 590 + 200 * i, 500))
                    lst_rect.append(pygame.rect.Rect(1280//2 - 590 + 200 * i, 500,140,50))
                    write_screen(lst[i - 1], BLACK, None, (1280//2 - 520 + 200 * i, 525), -1, surface, 20)
                while True:
                    mousePos = pygame.mouse.get_pos()
                    for item in lst_rect:
                        x = lst_rect.index(item)
                        if item.collidepoint(mousePos):
                            surface.blit(modebox_pressed, (1280//2 - 590 + 200 * (x+1), 500))
                            write_screen(lst[x], BLACK, None, (1280//2 - 520 + 200 * (x+1), 525), -1, surface, 20)
                        else:
                            surface.blit(modebox, (1280//2 - 590 + 200 * (x+1), 500))
                            write_screen(lst[x], BLACK, None, (1280//2 - 520 + 200 * (x+1), 525), -1, surface, 20)
                            
                    for event in pygame.event.get(): 
                        if event.type == pygame.MOUSEBUTTONUP:
                            make_sound()
                            if lst_rect[1].collidepoint(mousePos): #quit dialog
                                return 1
                            elif lst_rect[0].collidepoint(mousePos): # save
                                f = open('current_account.txt', 'r')
                                username = f.readline().strip("\n")
                                f.close()
                                create_user_saved_game(username)
                                return 1
                        if event.type == pygame.QUIT:
                            return 1
                    pygame.display.update()
    # continue to pause
    return 2

def get_player_current_cell():
    # Get player position (Tom's Position)
    if current_direction == "w" or current_direction == "a":
        pos = (
            np.ceil((player_rect.top - create_maze.THICK) / create_maze.TILE),
            np.ceil((player_rect.left -  create_maze.THICK) / create_maze.TILE),
        )
    else:
        pos = (
            np.floor((player_rect.top - create_maze.THICK) / create_maze.TILE),
            np.floor((player_rect.left - create_maze.THICK) / create_maze.TILE),
        )
    pos = (int(pos[0]),int(pos[1]))
    return pos

# def reset_record(username : str):
#     filename = 'player_record/' + username + '.txt'
#     f = open(filename,'w')
#     f.write('150 150 150 0 0 0')
#     f.close()

# def get_record(username : str):
#     filename = 'player_record/' + username + '.txt'
#     try:
#         fp = open(filename, 'r')
#         recordList = list(map(int, fp.readline().split()))
#         fp.close()
#         return recordList
#     except:
#         reset_record(username)
#         return get_record(username)

# timer, score, record
pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 150
score = 0

# fonts
font = pygame.font.Font(r"./font/Shermlock.ttf", 150)
text_font = pygame.font.Font(r"./font/Shermlock.ttf", 80)
mini_text_font = pygame.font.Font(r"./font/Shermlock.ttf", 40)

# save last position and the state of setting lastpos
lastpos = (-1, -1)
is_set = False
current_direction = None
default_algo = 2
incoming_algo = 1
# pause status, win status
autoplay_pause = False
pause = False
finish = False
# hint status
hint = False
hint_1 = False
hint_2 = False

# button
play_button = Button("img/playbutton.png", 900, 520)
home_button = Button("img/menubutton.png", 1100, 520)
pause_button = Button("img/pausebutton.png", 1300,50)
hint_button_1 = Button("img/hintbutton.png", 1300,300)
hint_button_2 = Button("img/hintbutton.png", 1300,500)


f = open("mode.txt",'r')
f.readline()
temp = int(f.readline())
loadgamestatus = True if temp == 2 else False
f.close()
    
#main    
count = 0
times_move = 0
running = True

recordList = get_record(username)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inp = open('result.txt', 'w')
            inp.write('-1')
            inp.close()
            running = False
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = False if pause else True
            if event.key == pygame.K_h:
                autoplay_pause = False if autoplay_pause else True
        if event.type == pygame.USEREVENT and not pause:
            time -= 1
    # Menu pause game
    if loadgamestatus:
        surface.blit(bg, (WIDTH, 0))
        surface.blit(game_surface, (0, 0))
        game_surface.blit(bg_game, (0, 0))
        fp1 = open('current_account.txt', 'r')
        user = fp1.readline().strip("\n")
        fp1.close()
        
        if load_game(username) == None:
            make_dialog(surface,"You haven't got any saved games!",1,0)
            break
        maze, maze2D, walls_collide_list, CurrentPos, AimPos, time, score, game_mode, game_level  = load_game(user)
        loadgamestatus = False
        #Set level
        if game_level == 20:
            create_maze.TILE = 60
            create_maze.cols, create_maze.rows = create_maze.WIDTH // 60, create_maze.HEIGHT // 60
            algorithm.MODE = 50
            create_maze.THICK = 4
            nums_food = 10
        elif game_level == 40:
            create_maze.TILE = 40
            create_maze.cols, create_maze.rows = create_maze.WIDTH // 40, create_maze.HEIGHT // 40
            algorithm.MODE = 50
            create_maze.THICK = 2
            nums_food = 30
        elif game_level == 100:
            create_maze.TILE = 20
            create_maze.cols, create_maze.rows = create_maze.WIDTH // 20, create_maze.HEIGHT // 20
            create_maze.THICK = 2
            algorithm.MODE = 300
            nums_food = 60
        # player settings
        if game_mode == 2:
            food_list = [Food() for i in range(nums_food)]
        player_speed = 10  # TILE must be divided by player_speed
        if game_level == 100:
            player_speed = 5
        player_img = pygame.image.load("img/tomface.png").convert_alpha()
        player_img = pygame.transform.scale(
            player_img, (create_maze.TILE - 2 * create_maze.THICK, create_maze.TILE - 2 * create_maze.THICK)
        )
        player_rect = player_img.get_rect()
        player_rect.topleft = (
            CurrentPos[1] * create_maze.TILE + create_maze.THICK,
            CurrentPos[0] * create_maze.TILE + create_maze.THICK,
        )

        # destination settings
        des_img = pygame.image.load("img/jerryface.png").convert_alpha()
        des_img = pygame.transform.scale(
            des_img, (create_maze.TILE - 2 * create_maze.THICK, create_maze.TILE - 2 * create_maze.THICK)
        )
        des_rect = des_img.get_rect()
        des_rect.topleft = (
            AimPos[1] * create_maze.TILE + create_maze.THICK,
            AimPos[0] * create_maze.TILE + create_maze.THICK,
        )
        surface.blit(bg, (WIDTH, 0))
        surface.blit(game_surface, (0, 0))
        game_surface.blit(bg_game, (0, 0))
        # draw maze
        [cell.draw(game_surface) for cell in maze]

        # draw player
        game_surface.blit(player_img, player_rect)
        game_surface.blit(des_img, des_rect)
        
        is_set = False
        last_pos = (-1,-1)
        direction = (0,0)        
        current_direction = None
        pause = False
        f = open("mode.txt",'w')
        f.write(str(username))
        f.write("\n")
        f.write("0\n")
        f.write(str(game_level))
        f.write("\n")
        f.write(str(game_mode))
        f.write("\n")
        f.close()

    elif pause:
        f = pause_game(auto)
        if f == 1:
            inp = open('result.txt', 'w')
            inp.write('-1')
            inp.close()
            running = False
            exit()
        elif f == 0:
            pause = False
        else:
            pause = True
    else:
        pos = get_player_current_cell()
        #Normal mode
        if game_mode == 0:
            # Action when player won
            if player_rect.colliderect(des_rect):
                result = open('result.txt', 'w')
                result.write('1')
                result.close()
                hint1, hint_2, hint = False, False, False
                is_set = False
                finish = True
                # End game
                running = False
                break

            else:
                surface.blit(bg, (WIDTH, 0))
                surface.blit(game_surface, (0, 0))
                game_surface.blit(bg_game, (0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        inp = open('result.txt', 'w')
                        inp.write('-1')
                        inp.close()
                        running = False
                        exit()
                    if event.type == pygame.USEREVENT:
                        time -= 1

                # controls and movement
                pos = get_player_current_cell()
                pressed_key = pygame.key.get_pressed()
                # Kiểm tra xem có thể rẽ vào hướng nút bấm không (nếu không bị tường chặn)
                for key, key_value in keys.items():
                    if pressed_key[key_value] and not is_collide(*directions[key], walls_collide_list, player_rect):
                        direction = directions[key]
                        if not is_set:
                            is_set = True
                            current_direction = key
                            lastpos = pos
                        break

                if pos == lastpos and not is_collide(*direction, walls_collide_list, player_rect):
                    player_rect.move_ip(direction)
                else:
                    is_set = False

                # Press ESC to see path dfs
                if hint_1 and not hint:
                    hint = True
                    maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
                    maze2D[pos[0]][pos[1]].make_tom_pos()
                    CurrentPos = pos
                    maze = list(maze2D.flatten())
                    path1 = findPathBetween2Point(maze, algo=1)
                    path_cell_list_dfs = getPathCellList(path1, maze2D)
                    five_first_step = path_cell_list_dfs[1:6].copy() if len(path1) > 6 else path_cell_list_dfs[1:].copy()
                    [cell.draw(game_surface) for cell in maze]

                if hint_2 and not hint:
                    hint = True
                    maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
                    maze2D[pos[0]][pos[1]].make_tom_pos()
                    CurrentPos = pos
                    maze = list(maze2D.flatten())
                    path2 = findPathBetween2Point(maze, algo=2)
                    path_cell_list_bfs = getPathCellList(path2, maze2D)
                    five_first_step = path_cell_list_bfs[1:6].copy() if len(path2) > 6 else path_cell_list_bfs[1:].copy()
                    [cell.draw(game_surface) for cell in maze]

                if hint:
                    for i in range(5):
                        hint_rect.topleft = (create_maze.THICK + five_first_step[i].x*create_maze.TILE,create_maze.THICK + five_first_step[i].y*create_maze.TILE)
                        game_surface.blit(hint_img, hint_rect)
                # draw maze
                [cell.draw(game_surface) for cell in maze]

                # draw player
                game_surface.blit(player_img, player_rect)
                game_surface.blit(des_img, des_rect)

                clock.tick(FPS)

        #Speedrun mode
        elif game_mode == 1:
            # Action when player won
            if player_rect.colliderect(des_rect):
                finish = True
                result = open('result.txt', 'w')
                result.write('1')
                result.close()
                # End game
                hint1, hint_2, hint = False, False, False
                is_set = False
                running = False
                if game_level == 20 and 150 - time < recordList[0]:
                    recordList[0] = 150 - time
                if game_level == 40 and 150 - time < recordList[1]:
                    recordList[1] = 150 - time
                if game_level == 100 and 150 - time < recordList[2]:
                    recordList[2] = 150 - time
                fp = open('current_account.txt', 'r')
                username = fp.readline().strip("\n")
                filename = 'player_record/' + username + '.txt'
                fp.close()
                fp = open(filename, 'w').close()
                fp = open(filename, 'w')
                for i in range(6):
                    fp.write(str(recordList[i]) + ' ')
                fp.close()
                break

            # Action when player failed
            elif time < 0:
                finish = True
                result = open('result.txt', 'w')
                result.write('0')
                result.close()
                hint1, hint_2, hint = False, False, False
                is_set = False
                running = False
                break
            else:
                surface.blit(bg, (WIDTH, 0))
                surface.blit(game_surface, (0, 0))
                game_surface.blit(bg_game, (0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        inp = open('result.txt', 'w')
                        inp.write('-1')
                        inp.close()
                        running = False
                        exit()
                    if event.type == pygame.USEREVENT:
                        time -= 1

                # controls and movement
                pos = get_player_current_cell()
                pressed_key = pygame.key.get_pressed()
                # Kiểm tra xem có thể rẽ vào hướng nút bấm không (nếu không bị tường chặn)
                for key, key_value in keys.items():
                    if pressed_key[key_value] and not is_collide(*directions[key], walls_collide_list,player_rect):
                        direction = directions[key]
                        if not is_set:
                            is_set = True
                            current_direction = key
                            lastpos = pos
                        break
                if pos == lastpos and not is_collide(*direction, walls_collide_list,player_rect):
                    player_rect.move_ip(direction)
                else:
                    is_set = False
                # path dfs
                if hint_1 and not hint:
                    hint = True
                    maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
                    maze2D[pos[0]][pos[1]].make_tom_pos()
                    CurrentPos = pos
                    maze = list(maze2D.flatten())
                    path1 = findPathBetween2Point(maze, algo=1)
                    path_cell_list_dfs = getPathCellList(path1, maze2D)
                    five_first_step = path_cell_list_dfs[1:6].copy() if len(path1)>6 else path_cell_list_dfs[1:].copy()
                    [cell.draw(game_surface) for cell in maze]

                if hint_2 and not hint:
                    hint = True
                    maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
                    maze2D[pos[0]][pos[1]].make_tom_pos()
                    CurrentPos = pos
                    maze = list(maze2D.flatten())
                    path2 = findPathBetween2Point(maze, algo=2)
                    path_cell_list_bfs = getPathCellList(path2, maze2D)
                    five_first_step = path_cell_list_bfs[1:6].copy() if len(path2)>6 else path_cell_list_bfs[1:].copy()
                    [cell.draw(game_surface) for cell in maze]

                if hint:
                    for i in range(5):
                        hint_rect.topleft = (create_maze.THICK + five_first_step[i].x*create_maze.TILE,create_maze.THICK + five_first_step[i].y*create_maze.TILE)
                        game_surface.blit(hint_img, hint_rect)
                # draw maze
                [cell.draw(game_surface) for cell in maze]

                # draw player
                game_surface.blit(player_img, player_rect)
                game_surface.blit(des_img, des_rect)

                # draw stats
                surface.blit(
                    text_font.render("TIME", True, pygame.Color("cyan")), (WIDTH + 20, 10)
                )
                surface.blit(font.render(f"{time}", True, pygame.Color("cyan")), (WIDTH + 20, 80))
                clock.tick(FPS)

        #Collect mode
        elif game_mode == 2:
            surface.blit(bg, (WIDTH, 0))
            surface.blit(game_surface, (0, 0))
            game_surface.blit(bg_game, (0, 0))
            maze2D[AimPos].make_blank()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    inp = open('result.txt', 'w')
                    inp.write('-1')
                    inp.close()
                    running = False
                    exit()
                if event.type == pygame.USEREVENT:
                    time -= 1

            # controls and movement
            pos = get_player_current_cell()
            pressed_key = pygame.key.get_pressed()
            # Kiểm tra xem có thể rẽ vào hướng nút bấm không (nếu không bị tường chặn)
            for key, key_value in keys.items():
                if pressed_key[key_value] and not is_collide(*directions[key], walls_collide_list, player_rect):
                    direction = directions[key]
                    if not is_set:
                        is_set = True
                        current_direction = key
                        lastpos = pos
                    break

            if pos == lastpos and not is_collide(*direction, walls_collide_list, player_rect):
                player_rect.move_ip(direction)
            else:
                is_set = False

            # draw maze
            [cell.draw(game_surface) for cell in maze]

            # gameplay
            if eat_food():
                score += 1

            # Kiem tra game da ket thuc hay chua
            if is_game_over() == False:
                running = False
                finish = True
                result = open('result.txt', 'w')
                result.write('1')
                result.close()
                break

            else:
                if game_level == 20 and score > recordList[3]:
                    recordList[3] = score
                if game_level == 40 and score > recordList[4]:
                    recordList[4] = score
                if game_level == 100 and score > recordList[5]:
                    recordList[5] = score
                fp = open('current_account.txt', 'r')
                username = fp.readline().strip('\n')
                filename = 'player_record/' + username + '.txt'
                fp.close()
                fp = open(filename, 'w').close()
                fp = open(filename, 'w')
                for i in range(6):
                    fp.write(str(recordList[i]) + ' ')
                fp.close()

            # draw player
            game_surface.blit(player_img, player_rect)

            # draw food
            [food.draw() for food in food_list]

            # draw stats
            surface.blit(
                text_font.render("TIME", True, pygame.Color("cyan")), (WIDTH + 20, 10)
            )
            surface.blit(font.render(f"{time}", True, pygame.Color("cyan")), (WIDTH + 20, 80))
            surface.blit(
                text_font.render("score", True, pygame.Color("forestgreen")),
                (WIDTH + 20, 240),
            )
            surface.blit(
                font.render(f"{score}", True, pygame.Color("forestgreen")), (WIDTH + 20, 310)
            )
            surface.blit(
                text_font.render("record", True, pygame.Color("magenta")),
                (WIDTH + 20, 470),
            )
            # surface.blit(
            #     font.render(f"{record}", True, pygame.Color("magenta")), (WIDTH + 20, 540)
            # )

            clock.tick(FPS)
        
        #draw pause button
        elif game_mode == 4:
            surface.blit(bg, (WIDTH, 0))
            surface.blit(game_surface, (0, 0))
            game_surface.blit(bg_game, (0, 0))
            if not autoplay_pause:
                walls_collide_list = sum(
                    [cell.get_rects() for cell in maze],
                    [
                        pygame.Rect(0, 0, create_maze.TILE * create_maze.cols, create_maze.THICK),
                        pygame.Rect(0, 0, create_maze.THICK, create_maze.TILE * create_maze.rows),
                        pygame.Rect(create_maze.cols * create_maze.TILE - create_maze.THICK, 0, create_maze.THICK, create_maze.TILE * create_maze.rows),
                        pygame.Rect(0, create_maze.rows * create_maze.TILE - create_maze.THICK, create_maze.TILE * create_maze.cols, create_maze.THICK)
                    ]
                )
                if incoming_algo != default_algo:
                    default_algo = incoming_algo
                    path = findPathBetween2Point(maze, algo=default_algo) if findPathBetween2Point(maze, algo=default_algo) else []
                pos = get_player_current_cell()
                if not is_set:
                    is_set = True
                    lastpos = pos
                if lastpos == pos:
                    if len(path)>=2:
                        pA = path[0]
                        pB = path[1]
                        current_direction = get_way_between_2point(pA,pB,maze2D)
                        player_rect.move_ip(directions[current_direction])
                    if not len(path):
                        # finish = True
                        if pygame.mouse.get_pressed()[0]:
                            maze, maze2D, walls_collide_list, player_rect.topleft,des_rect.topleft, lastpos, CurrentPos, AimPos, food_list= new_game()
                            time = -1
                            is_game_over()
                            finish = False
                            hint1, hint_2, hint = False, False, False
                            is_set = False
                            pygame.display.update()
                        else:
                            bg.blit(mini_text_font.render("Click to restart!", True, pygame.Color("white")), (0, 0))
                else:
                    path.pop(0)
                    maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
                    maze2D[pos[0]][pos[1]].make_tom_pos()
                    CurrentPos = pos
                    maze = list(maze2D.flatten())                    
                    is_set = False
            if hint_1:
                incoming_algo = 1
                path = findPathBetween2Point(maze, algo=incoming_algo) if findPathBetween2Point(maze, algo=incoming_algo) else []
                [cell.draw(game_surface) for cell in maze]
                [cell.color_cell(game_surface, "blue") for cell in getPathCellList(path,maze2D)[1:]]
                
            if hint_2:
                incoming_algo = 2
                path = findPathBetween2Point(maze, algo=incoming_algo) if findPathBetween2Point(maze, algo=incoming_algo) else []
                [cell.draw(game_surface) for cell in maze]
                [cell.color_cell(game_surface, "green") for cell in getPathCellList(path,maze2D)[1:]]
            game_surface.blit(des_img,des_rect)
            game_surface.blit(player_img, player_rect)
            [cell.draw(game_surface) for cell in maze]
            clock.tick(FPS)

        if not finish:
            #draw pause button
            pause_button.draw(surface)
            if pygame.mouse.get_pressed()[0]:
                if pause_button.rect.collidepoint(pygame.mouse.get_pos()):
                    pause = True
            #draw hint button
            if (game_mode == 0 or game_mode == 1 or game_mode == 4) and not pause:
                hint_button_1.draw(surface)
                surface.blit(mini_text_font.render("HINT 1", True, pygame.Color("white")), (1200, 400))

                hint_button_2.draw(surface)
                surface.blit(mini_text_font.render("HINT 2", True, pygame.Color("white")), (1200, 600))
                if pygame.mouse.get_pressed()[0]:
                    if hint_button_1.rect.collidepoint(pygame.mouse.get_pos()):
                        if not hint_1:
                            hint_1 = True
                            hint_2 = False
                            
                if pygame.mouse.get_pressed()[0]:
                    if hint_button_2.rect.collidepoint(pygame.mouse.get_pos()):
                        if not hint_2:
                            hint_2 = True
                            hint_1 = False
        else: 
            maze, maze2D, walls_collide_list, player_rect.topleft,des_rect.topleft, lastpos, CurrentPos, AimPos, food_list = new_game()
            finish = False
    pygame.display.update()
