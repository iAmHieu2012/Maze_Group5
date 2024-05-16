from create_maze import *
from algorithm import *

class Food:
    def __init__(self):
        self.img = pygame.image.load('img/food.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
        self.rect = self.img.get_rect()
        self.set_pos()

    def set_pos(self):
        self.rect.topleft = randrange(cols) * TILE + 5, randrange(rows) * TILE + 5

    def draw(self):
        game_surface.blit(self.img, self.rect)

def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True

# def has_neighbor(x,y):
    
    

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
        player_rect.center = TILE // 2, TILE // 2
        [food.set_pos() for food in food_list]
        set_record(record, score)
        record = get_record()
        time, score, FPS = 150, 0, 60


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
            return 0


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


FPS = 60
#FPS tăng thì tốc độ quét màn hình tăng -> tốc độ nhân vật tăng

pygame.init()
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()

# images
bg_game = pygame.image.load('img/background.jpg').convert()
bg = pygame.image.load('img/bg_main.jpg').convert()

# game icon
pygame.display.set_caption('Maze')
pygame_icon = pygame.image.load('img/maze_icon.png')
pygame.display.set_icon(pygame_icon)


# get maze
maze = generate_maze()

maze = create_maze.generate_maze()
generateTomAndJerryPos(maze)
maze2D = getMaze2DArray(maze)
path1 = findPathBetween2Point(1, maze, algo=1)

path_cell_list_dfs = getPathCellList(path1,maze2D)
path2 = findPathBetween2Point(1, maze, algo=2)

path_cell_list_bfs = getPathCellList(path2,maze2D)


# get Jerry position
AimPos = findTomAndJerryPos(maze2D)[1]

# get Tom position
CurrentPos = findTomAndJerryPos(maze2D)[0]

# player settings
player_speed = 5
player_img = pygame.image.load('img/character.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
player_rect = player_img.get_rect()
player_rect.center = TILE // 2, TILE // 2
player_rect.topleft = CurrentPos[1] * TILE + 5, CurrentPos[0] * TILE + 5

dir_img = pygame.image.load('img/jerryface.png').convert_alpha()
dir_img = pygame.transform.scale(dir_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
dir_rect = dir_img.get_rect()
dir_rect.center = TILE // 2, TILE // 2
dir_rect.topleft = AimPos[1] * TILE + 5, AimPos[0] * TILE + 5
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
keys = {'a': pygame.K_LEFT, 'd': pygame.K_RIGHT, 'w': pygame.K_UP, 's': pygame.K_DOWN}
direction = (0, 0)

# food settings
food_list = [Food() for i in range(10)]

# collision list
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

# timer, score, record
pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 150
score = 0
record = get_record()


# fonts
font = pygame.font.SysFont('Impact', 150)
text_font = pygame.font.SysFont('Impact', 80)

while True:
    surface.blit(bg, (WIDTH, 0))
    surface.blit(game_surface, (0, 0))
    game_surface.blit(bg_game, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.USEREVENT:
            time -= 1

    # controls and movement
    pressed_key = pygame.key.get_pressed()

    #Kiểm tra xem có thể rẽ vào hướng nút bấm không (nếu không bị tường chặn)
    for key, key_value in keys.items():
        if pressed_key[key_value] and not is_collide(*directions[key]):
            direction = directions[key]
                   
            break
    #Nếu nút bấm đầu vào hợp lệ, di chuyển đến hướng đó
    if not is_collide(*direction):
        player_rect.move_ip(direction)


    # Press ESC to see path dfs
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pos = (((player_rect.top-5)//TILE),((player_rect.left-5)//TILE))
        if pos != CurrentPos:
            maze2D[pos[0]][pos[1]].make_tom_pos()
            maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
            CurrentPos = pos
            maze = list(maze2D.flatten())
            path1 = findPathBetween2Point(1, maze, algo=1)
            path_cell_list_dfs = getPathCellList(path1,maze2D)
            [cell.draw(game_surface) for cell in maze]
        [cell.color_cell(game_surface,'blue') for cell in path_cell_list_dfs]

    # Press TAB to see path bfs
    if pygame.key.get_pressed()[pygame.K_TAB]:
        pos = (((player_rect.top-5)//TILE),((player_rect.left-5)//TILE))
        if pos != CurrentPos:
            maze2D[pos[0]][pos[1]].make_tom_pos()
            maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
            CurrentPos = pos
            maze = list(maze2D.flatten())
            path2 = findPathBetween2Point(1, maze, algo=2)
            path_cell_list_bfs = getPathCellList(path2,maze2D)
            [cell.draw(game_surface) for cell in maze]
        [cell.color_cell(game_surface,'green') for cell in path_cell_list_bfs]

    # draw maze
    [cell.draw(game_surface) for cell in maze]

    # gameplay
    if eat_food():
        FPS += 10
        score += 1
    is_game_over()

    # draw player
    game_surface.blit(player_img, player_rect)
    game_surface.blit(dir_img, dir_rect)

    # draw food
    [food.draw() for food in food_list]

    # draw stats
    surface.blit(text_font.render('TIME', True, pygame.Color('cyan'), True), (WIDTH + 20, 10))
    surface.blit(font.render(f'{time}', True, pygame.Color('cyan')), (WIDTH + 20, 80))
    surface.blit(text_font.render('score:', True, pygame.Color('forestgreen'), True), (WIDTH + 20, 240))
    surface.blit(font.render(f'{score}', True, pygame.Color('forestgreen')), (WIDTH + 20, 310))
    surface.blit(text_font.render('record:', True, pygame.Color('magenta'), True), (WIDTH + 20, 470))
    surface.blit(font.render(f'{record}', True, pygame.Color('magenta')), (WIDTH + 20, 540))

    pygame.display.flip()
    clock.tick(FPS)

