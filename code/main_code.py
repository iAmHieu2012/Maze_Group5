from create_maze import *
from algorithm import *
from autoplay import *
from time import sleep


class Food:
    def __init__(self):
        self.img = pygame.image.load("img/cheese.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (create_maze.TILE - 10, create_maze.TILE - 10))
        
game_level = int(input("Nhap do kho cua game: "))
game_mode = int(input("Nhap che do choi: "))

#Set level
if game_level == 1:
    create_maze.TILE = 60
    create_maze.cols, create_maze.rows = create_maze.WIDTH // 60, create_maze.HEIGHT // 60
    algorithm.MODE = 50
elif game_level == 2:
    create_maze.TILE = 40
    create_maze.cols, create_maze.rows = create_maze.WIDTH // 40, create_maze.HEIGHT // 40
    algorithm.MODE = 150
    create_maze.THICK = 3
elif game_level == 3:
    create_maze.TILE = 20
    create_maze.cols, create_maze.rows = create_maze.WIDTH // 20, create_maze.HEIGHT // 20
    create_maze.THICK = 2
    algorithm.MODE = 300

class Food:
    def __init__(self):
        self.img = pygame.image.load("img/food.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (create_maze.TILE - 10, create_maze.TILE - 10))
        self.rect = self.img.get_rect()
        self.set_pos()

    def set_pos(self):
        self.rect.topleft = randrange(cols) * create_maze.TILE + 5, randrange(rows) * create_maze.TILE + 5

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

def is_collide(x, y):
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
    global time, score, record, FPS
    if time < 0:
        pygame.time.wait(700)
        [food.set_pos() for food in food_list]
        set_record(record, score)
        record = get_record()
        time, score, FPS = 150, 0, 60


def get_record():
    try:
        with open("record") as f:
            return f.readline()
    except FileNotFoundError:
        with open("record", "w") as f:
            f.write("0")
            return 0


def set_record(record, score):
    rec = max(int(record), score)
    with open("record", "w") as f:
        f.write(str(rec))


FPS = 60
# FPS tăng thì tốc độ quét màn hình tăng -> tốc độ nhân vật tăng

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

bg_tom_win = pygame.image.load("img/tomwin.png").convert()
bg_tom_win = pygame.transform.scale(bg_tom_win, (WIDTH+300, HEIGHT))
bg_jerry_win = pygame.image.load("img/jerrywin.png").convert()
bg_jerry_win = pygame.transform.scale(bg_jerry_win, (WIDTH+300, HEIGHT))



bg = pygame.image.load("img/bg_main.jpg").convert()

# game icon
pygame.display.set_caption("Maze")
pygame_icon = pygame.image.load("img/maze_icon.png")
pygame.display.set_icon(pygame_icon)


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
        CurrentPos[1] * create_maze.TILE + maze[0].thickness,
        CurrentPos[0] * create_maze.TILE + maze[0].thickness,
    )
    
    des_rect.topleft = (
        AimPos[1] * create_maze.TILE + maze[0].thickness,
        AimPos[0] * create_maze.TILE + maze[0].thickness,
    )
    walls_collide_list = sum(
        [cell.get_rects() for cell in maze],
        [
            pygame.Rect(0, 0, create_maze.TILE * create_maze.cols, maze[0].thickness),
            pygame.Rect(0, 0, maze[0].thickness, create_maze.TILE * create_maze.rows),
            pygame.Rect(create_maze.cols * create_maze.TILE - maze[0].thickness, 0, maze[0].thickness, create_maze.TILE * create_maze.rows),
            pygame.Rect(0, create_maze.rows * create_maze.TILE - maze[0].thickness, create_maze.TILE * create_maze.cols, maze[0].thickness)
        ]
    )
    return maze, maze2D, walls_collide_list, player_rect.topleft,des_rect.topleft
    
# get maze
maze = create_maze.generate_maze()
generateTomAndJerryPos(maze)
maze2D = getMaze2DArray(maze)

# get Jerry position
AimPos = findTomAndJerryPos(maze2D)[1]

# get Tom position
CurrentPos = findTomAndJerryPos(maze2D)[0]

# player settings
player_speed = 4  # TILE must be divided by player_speed
player_img = pygame.image.load("img/tomface.png").convert_alpha()
player_img = pygame.transform.scale(
    player_img, (create_maze.TILE - 2 * maze[0].thickness, create_maze.TILE - 2 * maze[0].thickness)
)
player_rect = player_img.get_rect()
player_rect.topleft = (
    CurrentPos[1] * create_maze.TILE + maze[0].thickness,
    CurrentPos[0] * create_maze.TILE + maze[0].thickness,
)

# destination settings
des_img = pygame.image.load("img/jerryface.png").convert_alpha()
des_img = pygame.transform.scale(
    des_img, (create_maze.TILE - 2 * maze[0].thickness, create_maze.TILE - 2 * maze[0].thickness)
)
des_rect = des_img.get_rect()
des_rect.topleft = (
    AimPos[1] * create_maze.TILE + maze[0].thickness,
    AimPos[0] * create_maze.TILE + maze[0].thickness,
)
# hint starlight
hint_img = pygame.image.load("img/star.png").convert_alpha()
hint_img = pygame.transform.scale(
    hint_img, (create_maze.TILE - 2 * maze[0].thickness, create_maze.TILE - 2 * maze[0].thickness)
)
hint_rect = hint_img.get_rect()
# directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
# keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
directions = {
    "a": (-player_speed, 0),
    "d": (player_speed, 0),
    "w": (0, -player_speed),
    "s": (0, player_speed),
}
keys = {"a": pygame.K_j, "d": pygame.K_l, "w": pygame.K_i, "s": pygame.K_k}
direction = (0, 0)

# food settings
food_list = [Food() for i in range(10)]

# collision list
walls_collide_list = sum(
    [cell.get_rects() for cell in maze],
    [

        pygame.Rect(0, 0, create_maze.TILE * create_maze.cols, maze[0].thickness),
        pygame.Rect(0, 0, maze[0].thickness, create_maze.TILE * create_maze.rows),
        pygame.Rect(
            create_maze.cols * create_maze.TILE - maze[0].thickness,
            0,
            maze[0].thickness,
            create_maze.TILE * create_maze.rows,
        ),
        pygame.Rect(
            0,
            create_maze.rows * create_maze.TILE - maze[0].thickness,
            create_maze.TILE * create_maze.cols,
            maze[0].thickness,
        ),
    ],
)

# timer, score, record
pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 150
score = 0
record = get_record()


# fonts
font = pygame.font.Font(r"./font/Shermlock.ttf", 150)
text_font = pygame.font.Font(r"./font/Shermlock.ttf", 80)
mini_text_font = pygame.font.Font(r"./font/Shermlock.ttf", 40)

# save last position and the state of setting lastpos
lastpos = (-1, -1)
is_set = False
current_direction = None
default_algo = 1
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
# sound_button = Button("img/resumebutton.png", 1200,570)
    
def pause_game():
    surface.blit(pause_surface,(0,0))
    pause_surface.blit(bg_pause, (0,0))
    pause_surface.blit(text_font.render("CONTINUE?", True, pygame.Color("white")), (880, 400))
    play_button.draw(pause_surface)
    home_button.draw(pause_surface)
    if pygame.mouse.get_pressed()[0]:
        if play_button.rect.collidepoint(pygame.mouse.get_pos()):
            return False
        if home_button.rect.collidepoint(pygame.mouse.get_pos()):
            # Go back home()
            return False
    return True

def get_player_current_cell():
    # Get player position (Tom's Position)
    if current_direction == "w" or current_direction == "a":
        pos = (
            np.ceil((player_rect.top - maze[0].thickness) / create_maze.TILE),
            np.ceil((player_rect.left -  maze[0].thickness) / create_maze.TILE),
        )
    else:
        pos = (
            np.floor((player_rect.top - maze[0].thickness) / create_maze.TILE),
            np.floor((player_rect.left - maze[0].thickness) / create_maze.TILE),
        )
    pos = (int(pos[0]),int(pos[1]))
    return pos

count = 0
times_move = 0
#main    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
    if pause:
        pause = pause_game()
    else:
        pos = get_player_current_cell()
        #Normal mode
        if game_mode == 1:
            # Action when player won
            if player_rect.colliderect(des_rect):
                finish = True
                # End game
                surface.blit(end_game_surface,(0,0))
                end_game_surface.blit(bg_tom_win,(0,0))
                end_game_surface.blit(mini_text_font.render("Click on the screen to restart!", True, pygame.Color("white")), (850, 500))
                if pygame.mouse.get_pressed()[0]:
                    maze, maze2D,walls_collide_list, player_rect.topleft,des_rect.topleft = new_game()
                    # get Jerry position
                    AimPos = findTomAndJerryPos(maze2D)[1]
                    # get Tom position
                    CurrentPos = findTomAndJerryPos(maze2D)[0]
                    print(AimPos,CurrentPos)
                    time = -1
                    is_game_over()
                    finish = False
                    hint1, hint_2, hint = False, False, False
                    is_set = False
                    continue
            else:
                surface.blit(bg, (WIDTH, 0))
                surface.blit(game_surface, (0, 0))
                game_surface.blit(bg_game, (0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.USEREVENT:
                        time -= 1

                # controls and movement
                pos = get_player_current_cell()
                pressed_key = pygame.key.get_pressed()
                # Kiểm tra xem có thể rẽ vào hướng nút bấm không (nếu không bị tường chặn)
                for key, key_value in keys.items():
                    if pressed_key[key_value] and not is_collide(*directions[key]):
                        direction = directions[key]
                        if not is_set:
                            is_set = True
                            current_direction = key
                            lastpos = pos
                        break

                if pos == lastpos and not is_collide(*direction):
                    player_rect.move_ip(direction)
                else:
                    is_set = False

                if hint_1 and not hint:
                    hint = True
                    maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
                    maze2D[pos[0]][pos[1]].make_tom_pos()
                    CurrentPos = pos
                    maze = list(maze2D.flatten())
                    path1 = findPathBetween2Point(maze, algo=1)
                    path_cell_list_dfs = getPathCellList(path1, maze2D)
                    five_first_step = path_cell_list_dfs[1:6].copy()
                    [cell.draw(game_surface) for cell in maze]

                if hint_2 and not hint:
                    hint = True
                    maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
                    maze2D[pos[0]][pos[1]].make_tom_pos()
                    CurrentPos = pos
                    maze = list(maze2D.flatten())
                    path2 = findPathBetween2Point(maze, algo=2)
                    path_cell_list_bfs = getPathCellList(path2, maze2D)
                    five_first_step = path_cell_list_bfs[1:6].copy()
                    [cell.draw(game_surface) for cell in maze]

                if hint:
                    for i in range(5):
                        hint_rect.topleft = (maze[0].thickness + five_first_step[i].x*create_maze.TILE,maze[0].thickness + five_first_step[i].y*create_maze.TILE)
                        game_surface.blit(hint_img, hint_rect)
                # draw maze
                [cell.draw(game_surface) for cell in maze]

                # draw player
                game_surface.blit(player_img, player_rect)
                game_surface.blit(des_img, des_rect)

                clock.tick(FPS)

        #Speedrun mode
        elif game_mode == 2:
            # Action when player won
            if player_rect.colliderect(des_rect):
                finish = True
                # End game
                surface.blit(end_game_surface,(0,0))
                end_game_surface.blit(bg_tom_win,(0,0))
                end_game_surface.blit(mini_text_font.render("Click on the screen to restart!", True, pygame.Color("white")), (850, 500))
                if pygame.mouse.get_pressed()[0]:
                    maze, maze2D,walls_collide_list ,player_rect.topleft,des_rect.topleft= new_game()
                    # get Jerry position
                    AimPos = findTomAndJerryPos(maze2D)[1]
                    # get Tom position
                    CurrentPos = findTomAndJerryPos(maze2D)[0]
                    time = -1
                    is_game_over()
                    finish = False
                    hint1, hint_2, hint = False, False, False
                    is_set = False
                    continue
            # Action when player failed
            elif time < 0:
                finish = True
                surface.blit(end_game_surface,(0,0))
                end_game_surface.blit(bg_jerry_win,(0,0))
                end_game_surface.blit(mini_text_font.render("Click on the screen to restart!", True, pygame.Color("white")), (850, 500))
                if pygame.mouse.get_pressed()[0]:
                    maze, maze2D,walls_collide_list ,player_rect.topleft,des_rect.topleft= new_game()
                    # get Jerry position
                    AimPos = findTomAndJerryPos(maze2D)[1]
                    # get Tom position
                    CurrentPos = findTomAndJerryPos(maze2D)[0]
                    is_game_over()
                    finish = False
                    hint1, hint_2, hint = False, False, False
                    is_set = False
                    continue
            else:
                surface.blit(bg, (WIDTH, 0))
                surface.blit(game_surface, (0, 0))
                game_surface.blit(bg_game, (0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.USEREVENT:
                        time -= 1

                # controls and movement
                pos = get_player_current_cell()
                pressed_key = pygame.key.get_pressed()
                # Kiểm tra xem có thể rẽ vào hướng nút bấm không (nếu không bị tường chặn)
                for key, key_value in keys.items():
                    if pressed_key[key_value] and not is_collide(*directions[key]):
                        direction = directions[key]
                        if not is_set:
                            is_set = True
                            current_direction = key
                            lastpos = pos
                        break

                if pos == lastpos and not is_collide(*direction):
                    player_rect.move_ip(direction)
                else:
                    is_set = False
                if hint_1 and not hint:
                    hint = True
                    maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
                    maze2D[pos[0]][pos[1]].make_tom_pos()
                    CurrentPos = pos
                    maze = list(maze2D.flatten())
                    path1 = findPathBetween2Point(maze, algo=1)
                    path_cell_list_dfs = getPathCellList(path1, maze2D)
                    five_first_step = path_cell_list_dfs[1:6].copy()
                    [cell.draw(game_surface) for cell in maze]

                if hint_2 and not hint:
                    hint = True
                    maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
                    maze2D[pos[0]][pos[1]].make_tom_pos()
                    CurrentPos = pos
                    maze = list(maze2D.flatten())
                    path2 = findPathBetween2Point(maze, algo=2)
                    path_cell_list_bfs = getPathCellList(path2, maze2D)
                    five_first_step = path_cell_list_bfs[1:6].copy()
                    [cell.draw(game_surface) for cell in maze]

                if hint:
                    for i in range(5):
                        hint_rect.topleft = (maze[0].thickness + five_first_step[i].x*create_maze.TILE,maze[0].thickness + five_first_step[i].y*create_maze.TILE)
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
                # surface.blit(
                #     text_font.render("score", True, pygame.Color("forestgreen")),
                #     (WIDTH + 20, 240),
                # )
                # surface.blit(
                #     font.render(f"{score}", True, pygame.Color("forestgreen")), (WIDTH + 20, 310)
                # )
                # surface.blit(
                #     text_font.render("record", True, pygame.Color("magenta")),
                #     (WIDTH + 20, 470),
                # )
                # surface.blit(
                #     font.render(f"{record}", True, pygame.Color("magenta")), (WIDTH + 20, 540)
                # )

                clock.tick(FPS)

        #Collect mode
        elif game_mode == 3:
            if time < 0:
                finish = True
                bg.blit(mini_text_font.render("Click on the screen to restart!", True, pygame.Color("white")), (0, 500))
                if pygame.mouse.get_pressed()[0]:
                    maze, maze2D,walls_collide_list ,player_rect.topleft,des_rect.topleft= new_game()
                    # get Jerry position
                    AimPos = findTomAndJerryPos(maze2D)[1]
                    # get Tom position
                    CurrentPos = findTomAndJerryPos(maze2D)[0]
                    is_game_over()
                    finish = False
                    is_set = False
                    continue
            else:
                surface.blit(bg, (WIDTH, 0))
                surface.blit(game_surface, (0, 0))
                game_surface.blit(bg_game, (0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.USEREVENT:
                        time -= 1

                # controls and movement
                pos = get_player_current_cell()
                pressed_key = pygame.key.get_pressed()
                # Kiểm tra xem có thể rẽ vào hướng nút bấm không (nếu không bị tường chặn)
                for key, key_value in keys.items():
                    if pressed_key[key_value] and not is_collide(*directions[key]):
                        direction = directions[key]
                        if not is_set:
                            is_set = True
                            current_direction = key
                            lastpos = pos
                        break

                if pos == lastpos and not is_collide(*direction):
                    player_rect.move_ip(direction)
                else:
                    is_set = False

                # draw maze
                [cell.draw(game_surface) for cell in maze]

                # gameplay
                if eat_food():
                    # FPS += 10
                    score += 1

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
                surface.blit(
                    font.render(f"{record}", True, pygame.Color("magenta")), (WIDTH + 20, 540)
                )

            clock.tick(FPS)
        
        elif game_mode == 4:
            surface.blit(bg, (WIDTH, 0))
            surface.blit(game_surface, (0, 0))
            game_surface.blit(bg_game, (0, 0))
            if not autoplay_pause:
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
                        bg.blit(text_font.render("FINISH", True, pygame.Color("pink")),(0,0))
                        bg.blit(mini_text_font.render("Click on the screen to restart!", True, pygame.Color("white")), (850, 500))
                        if pygame.mouse.get_pressed()[0]:
                            maze, maze2D,walls_collide_list ,player_rect.topleft,des_rect.topleft= new_game()
                            # get Jerry position
                            AimPos = findTomAndJerryPos(maze2D)[1]
                            # get Tom position
                            CurrentPos = findTomAndJerryPos(maze2D)[0]
                            time = -1
                            is_game_over()
                            finish = False
                            hint1, hint_2, hint = False, False, False
                            is_set = False
                else:
                    maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
                    maze2D[pos[0]][pos[1]].make_tom_pos()
                    CurrentPos = pos
                    maze = list(maze2D.flatten())                    
                    is_set = False
            if hint_1:
                default_algo = 1
                [cell.draw(game_surface) for cell in maze]
                [cell.color_cell(game_surface, "blue") for cell in getPathCellList(path,maze2D)[1:]]
                
            if hint_2:
                default_algo = 2
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
            if (game_mode == 1 or game_mode == 2 or game_mode == 4) and not pause:
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
    pygame.display.update()
