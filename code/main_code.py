from create_maze import *
from algorithm import *
import sys

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
        player_rect.center = create_maze.TILE // 2, create_maze.TILE // 2
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
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()

# images
bg_game = pygame.image.load("img/background.jpg").convert()
bg_game = pygame.transform.scale(bg_game, (WIDTH, HEIGHT))
bg = pygame.image.load("img/bg_main.jpg").convert()

# game icon
pygame.display.set_caption("Maze")
pygame_icon = pygame.image.load("img/maze_icon.png")
pygame.display.set_icon(pygame_icon)


# get maze
maze = create_maze.generate_maze()
generateTomAndJerryPos(maze)
maze2D = getMaze2DArray(maze)
path1 = findPathBetween2Point(1, maze, algo=1)
path_cell_list_dfs = getPathCellList(path1, maze2D)
path2 = findPathBetween2Point(1, maze, algo=2)
path_cell_list_bfs = getPathCellList(path2, maze2D)


# get Jerry position
AimPos = findTomAndJerryPos(maze2D)[1]

# get Tom position
CurrentPos = findTomAndJerryPos(maze2D)[0]

maze = create_maze.generate_maze()
generateTomAndJerryPos(maze)
maze2D = getMaze2DArray(maze)
path1 = findPathBetween2Point(1, maze, algo=1)

path_cell_list_dfs = getPathCellList(path1, maze2D)
path2 = findPathBetween2Point(1, maze, algo=2)

path_cell_list_bfs = getPathCellList(path2, maze2D)


# get Jerry position
AimPos = findTomAndJerryPos(maze2D)[1]

# get Tom position
CurrentPos = findTomAndJerryPos(maze2D)[0]

# player settings
player_speed = 10
player_img = pygame.image.load("img/tomface.png").convert_alpha()
player_img = pygame.transform.scale(
    player_img, (create_maze.TILE - 2 * maze[0].thickness, create_maze.TILE - 2 * maze[0].thickness)
)
player_rect = player_img.get_rect()
player_rect.topleft = (
    CurrentPos[1] * create_maze.TILE + maze[0].thickness,
    CurrentPos[0] * create_maze.TILE + maze[0].thickness,
)

dir_img = pygame.image.load("img/jerryface.png").convert_alpha()
dir_img = pygame.transform.scale(
    dir_img, (create_maze.TILE - 2 * maze[0].thickness, create_maze.TILE - 2 * maze[0].thickness)
)
dir_rect = dir_img.get_rect()
dir_rect.topleft = (
    AimPos[1] * create_maze.TILE + maze[0].thickness,
    AimPos[0] * create_maze.TILE + maze[0].thickness,
)
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

# save last position and the state of setting lastpos
lastpos = (-1, -1)
is_set = False
current_direction = None


#Normal mode
if game_mode == 1:
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
        if current_direction == "w" or current_direction == "a":
            pos = (
                ((player_rect.top - 2* maze[0].thickness) // create_maze.TILE),
                ((player_rect.left - 2* maze[0].thickness) // create_maze.TILE),
            )
        else:
            pos = (
                ((player_rect.top - maze[0].thickness) // create_maze.TILE),
                ((player_rect.left - maze[0].thickness) // create_maze.TILE),
            )
        pressed_key = pygame.key.get_pressed()
        # Kiểm tra xem có thể rẽ vào hướng nút bấm không (nếu không bị tường chặn)
        for key, key_value in keys.items():
            if pressed_key[key_value] and not is_collide(*directions[key]):
                direction = directions[key]
                if not is_set:
                    is_set = True
                    current_direction = key
                    if key == "w" or key == "a":
                        lastpos = (
                            ((player_rect.top - 2*maze[0].thickness) // create_maze.TILE),
                            ((player_rect.left-2*maze[0].thickness) // create_maze.TILE),
                        )
                    else:
                        lastpos = (
                            ((player_rect.top - maze[0].thickness) // create_maze.TILE),
                            ((player_rect.left - maze[0].thickness) // create_maze.TILE),
                        )
                break

        if pos == lastpos and not is_collide(*direction):
            player_rect.move_ip(direction)
        else:
            is_set = False

        # Press ESC to see path dfs
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pos = (
                ((player_rect.top - maze[0].thickness) // create_maze.TILE),
                round((player_rect.left - maze[0].thickness) // create_maze.TILE),
            )
            maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
            maze2D[pos[0]][pos[1]].make_tom_pos()
            CurrentPos = pos
            maze = list(maze2D.flatten())
            path1 = findPathBetween2Point(1, maze, algo=1)
            path_cell_list_dfs = getPathCellList(path1, maze2D)
            [cell.draw(game_surface) for cell in maze]
            [cell.color_cell(game_surface, "blue") for cell in path_cell_list_dfs]

        # Press TAB to see path bfs
        if pygame.key.get_pressed()[pygame.K_TAB]:
            pos = (
                ((player_rect.top - maze[0].thickness) // create_maze.TILE),
                ((player_rect.left - maze[0].thickness) // create_maze.TILE),
            )
            maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
            maze2D[pos[0]][pos[1]].make_tom_pos()
            CurrentPos = pos
            maze = list(maze2D.flatten())
            path2 = findPathBetween2Point(1, maze, algo=2)
            path_cell_list_bfs = getPathCellList(path2, maze2D)
            [cell.draw(game_surface) for cell in maze]
            [cell.color_cell(game_surface, "green") for cell in path_cell_list_bfs]

        if pygame.key.get_pressed()[pygame.K_m]:
            print(
                (
                    ((player_rect.top - maze[0].thickness) // create_maze.TILE),
                    ((player_rect.left - maze[0].thickness) // create_maze.TILE),
                )
            )
            print(((player_rect.top - maze[0].thickness) / create_maze.TILE),
                    ((player_rect.left - maze[0].thickness) / create_maze.TILE))
            print(player_rect)

        # draw maze
        [cell.draw(game_surface) for cell in maze]

        # draw player
        game_surface.blit(player_img, player_rect)
        game_surface.blit(dir_img, dir_rect)

        pygame.display.flip()
        clock.tick(FPS)

#Speedrun mode
elif game_mode == 2:
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
        if current_direction == "w" or current_direction == "a":
            pos = (
                ((player_rect.top - 2* maze[0].thickness) // create_maze.TILE),
                ((player_rect.left - 2* maze[0].thickness) // create_maze.TILE),
            )
        else:
            pos = (
                ((player_rect.top - maze[0].thickness) // create_maze.TILE),
                ((player_rect.left - maze[0].thickness) // create_maze.TILE),
            )
        pressed_key = pygame.key.get_pressed()
        # Kiểm tra xem có thể rẽ vào hướng nút bấm không (nếu không bị tường chặn)
        for key, key_value in keys.items():
            if pressed_key[key_value] and not is_collide(*directions[key]):
                direction = directions[key]
                if not is_set:
                    is_set = True
                    current_direction = key
                    if key == "w" or key == "a":
                        lastpos = (
                            ((player_rect.top - 2*maze[0].thickness) // create_maze.TILE),
                            ((player_rect.left-2*maze[0].thickness) // create_maze.TILE),
                        )
                    else:
                        lastpos = (
                            ((player_rect.top - maze[0].thickness) // create_maze.TILE),
                            ((player_rect.left - maze[0].thickness) // create_maze.TILE),
                        )
                break

        if pos == lastpos and not is_collide(*direction):
            player_rect.move_ip(direction)
        else:
            is_set = False

        # Press ESC to see path dfs
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pos = (
                ((player_rect.top - maze[0].thickness) // create_maze.TILE),
                round((player_rect.left - maze[0].thickness) // create_maze.TILE),
            )
            maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
            maze2D[pos[0]][pos[1]].make_tom_pos()
            CurrentPos = pos
            maze = list(maze2D.flatten())
            path1 = findPathBetween2Point(1, maze, algo=1)
            path_cell_list_dfs = getPathCellList(path1, maze2D)
            [cell.draw(game_surface) for cell in maze]
            [cell.color_cell(game_surface, "blue") for cell in path_cell_list_dfs]

        # Press TAB to see path bfs
        if pygame.key.get_pressed()[pygame.K_TAB]:
            pos = (
                ((player_rect.top - maze[0].thickness) // create_maze.TILE),
                ((player_rect.left - maze[0].thickness) // create_maze.TILE),
            )
            maze2D[CurrentPos[0]][CurrentPos[1]].make_blank()
            maze2D[pos[0]][pos[1]].make_tom_pos()
            CurrentPos = pos
            maze = list(maze2D.flatten())
            path2 = findPathBetween2Point(1, maze, algo=2)
            path_cell_list_bfs = getPathCellList(path2, maze2D)
            [cell.draw(game_surface) for cell in maze]
            [cell.color_cell(game_surface, "green") for cell in path_cell_list_bfs]

        if pygame.key.get_pressed()[pygame.K_m]:
            print(
                (
                    ((player_rect.top - maze[0].thickness) // create_maze.TILE),
                    ((player_rect.left - maze[0].thickness) // create_maze.TILE),
                )
            )
            print(((player_rect.top - maze[0].thickness) / create_maze.TILE),
                    ((player_rect.left - maze[0].thickness) / create_maze.TILE))
            print(player_rect)

        # draw maze
        [cell.draw(game_surface) for cell in maze]

        # draw player
        game_surface.blit(player_img, player_rect)
        game_surface.blit(dir_img, dir_rect)

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

        pygame.display.flip()
        clock.tick(FPS)

#Collect mode
elif game_mode == 3:
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
        if current_direction == "w" or current_direction == "a":
            pos = (
                ((player_rect.top - 2* maze[0].thickness) // create_maze.TILE),
                ((player_rect.left - 2* maze[0].thickness) // create_maze.TILE),
            )
        else:
            pos = (
                ((player_rect.top - maze[0].thickness) // create_maze.TILE),
                ((player_rect.left - maze[0].thickness) // create_maze.TILE),
            )
        pressed_key = pygame.key.get_pressed()
        # Kiểm tra xem có thể rẽ vào hướng nút bấm không (nếu không bị tường chặn)
        for key, key_value in keys.items():
            if pressed_key[key_value] and not is_collide(*directions[key]):
                direction = directions[key]
                if not is_set:
                    is_set = True
                    current_direction = key
                    if key == "w" or key == "a":
                        lastpos = (
                            ((player_rect.top - 2*maze[0].thickness) // create_maze.TILE),
                            ((player_rect.left-2*maze[0].thickness) // create_maze.TILE),
                        )
                    else:
                        lastpos = (
                            ((player_rect.top - maze[0].thickness) // create_maze.TILE),
                            ((player_rect.left - maze[0].thickness) // create_maze.TILE),
                        )
                break

        if pos == lastpos and not is_collide(*direction):
            player_rect.move_ip(direction)
        else:
            is_set = False

        if pygame.key.get_pressed()[pygame.K_m]:
            print(
                (
                    ((player_rect.top - maze[0].thickness) // create_maze.TILE),
                    ((player_rect.left - maze[0].thickness) // create_maze.TILE),
                )
            )
            print(((player_rect.top - maze[0].thickness) / create_maze.TILE),
                    ((player_rect.left - maze[0].thickness) / create_maze.TILE))
            print(player_rect)

        # draw maze
        [cell.draw(game_surface) for cell in maze]

        # gameplay
        if eat_food():
            # FPS += 10
            score += 1
        is_game_over()

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

        pygame.display.flip()
        clock.tick(FPS)

