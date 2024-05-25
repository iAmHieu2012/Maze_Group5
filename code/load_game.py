from create_maze import *
from algorithm import *
def read_saved_game(username : str):
    filename = 'saved_game/' + username + '.txt'
    fp = open(filename, 'r')
    game_mode = int(fp.readline())
    if game_mode == 0:
        game_level = int(fp.readline())
        #Vị trí Jerry
        Aimpos = fp.readline().split()
        Aimpos[0] = int(Aimpos[0])
        Aimpos[1] = int(Aimpos[1])
        #Vị trí Tom
        Currentpos = fp.readline().split()
        Currentpos[0] = int(Currentpos[0])
        Currentpos[1] = int(Currentpos[1])
        maze = []
        if game_level == 20:
            create_maze.TILE = 60
            create_maze.cols, create_maze.rows = create_maze.WIDTH // 60, create_maze.HEIGHT // 60
            create_maze.THICK = 4
            for i in range(216): # col = 18, row = 12
                pos = fp.readline().split()
                x, y = int(pos[0]), int(pos[1])
                cell = Cell(x, y)
                wall = fp.readline().split()
                if wall[0] == '0':
                    cell.walls['top'] = False
                if wall[1] == '0':
                    cell.walls['right'] = False
                if wall[2] == '0':
                    cell.walls['bottom'] = False
                if wall[3] == '0':
                    cell.walls['left'] = False  
                maze.append(cell)
        elif game_level == 40:
            create_maze.TILE = 40
            create_maze.cols, create_maze.rows = create_maze.WIDTH // 40, create_maze.HEIGHT // 40
            create_maze.THICK = 3
            for i in range(486): # col = 27, row = 18
                pos = fp.readline().split()
                x, y = int(pos[0]), int(pos[1])
                cell = Cell(x, y)
                wall = fp.readline().split()
                if wall[0] == '0':
                    cell.walls['top'] = False
                if wall[1] == '0':
                    cell.walls['right'] = False
                if wall[2] == '0':
                    cell.walls['bottom'] = False
                if wall[3] == '0':
                    cell.walls['left'] = False  
                maze.append(cell)
        elif game_level == 100:
            create_maze.TILE = 60
            create_maze.cols, create_maze.rows = create_maze.WIDTH // 20, create_maze.HEIGHT // 20
            create_maze.THICK = 2
            for i in range(1944): #col = 54, row = 36
                pos = fp.readline().split()
                x, y = int(pos[0]), int(pos[1])
                cell = Cell(x, y)
                wall = fp.readline().split()
                if wall[0] == '0':
                    cell.walls['top'] = False
                if wall[1] == '0':
                    cell.walls['right'] = False
                if wall[2] == '0':
                    cell.walls['bottom'] = False
                if wall[3] == '0':
                    cell.walls['left'] = False  
                maze.append(cell)
        return game_mode, game_level, maze, Currentpos, Aimpos
    elif game_mode == 1:
        time = int(fp.readline())
        game_level = int(fp.readline())
        #Vị trí Jerry
        Aimpos = fp.readline().split()
        Aimpos[0] = int(Aimpos[0])
        Aimpos[1] = int(Aimpos[1])
        #Vị trí Tom
        Currentpos = fp.readline().split()
        Currentpos[0] = int(Currentpos[0])
        Currentpos[1] = int(Currentpos[1])
        maze = []
        if game_level == 20:
            create_maze.TILE = 60
            create_maze.cols, create_maze.rows = create_maze.WIDTH // 60, create_maze.HEIGHT // 60
            create_maze.THICK = 4
            for i in range(216): # col = 18, row = 12
                pos = fp.readline().split()
                x, y = int(pos[0]), int(pos[1])
                cell = Cell(x, y)
                wall = fp.readline().split()
                if wall[0] == '0':
                    cell.walls['top'] = False
                if wall[1] == '0':
                    cell.walls['right'] = False
                if wall[2] == '0':
                    cell.walls['bottom'] = False
                if wall[3] == '0':
                    cell.walls['left'] = False  
                maze.append(cell)
        elif game_level == 40:
            create_maze.TILE = 40
            create_maze.cols, create_maze.rows = create_maze.WIDTH // 40, create_maze.HEIGHT // 40
            create_maze.THICK = 3
            for i in range(486): # col = 27, row = 18
                pos = fp.readline().split()
                x, y = int(pos[0]), int(pos[1])
                cell = Cell(x, y)
                wall = fp.readline().split()
                if wall[0] == '0':
                    cell.walls['top'] = False
                if wall[1] == '0':
                    cell.walls['right'] = False
                if wall[2] == '0':
                    cell.walls['bottom'] = False
                if wall[3] == '0':
                    cell.walls['left'] = False  
                maze.append(cell)
        elif game_level == 100:
            create_maze.TILE = 20
            create_maze.cols, create_maze.rows = create_maze.WIDTH // 20, create_maze.HEIGHT // 20
            create_maze.THICK = 2
            for i in range(1944): #col = 54, row = 36
                pos = fp.readline().split()
                x, y = int(pos[0]), int(pos[1])
                cell = Cell(x, y)
                wall = fp.readline().split()
                if wall[0] == '0':
                    cell.walls['top'] = False
                if wall[1] == '0':
                    cell.walls['right'] = False
                if wall[2] == '0':
                    cell.walls['bottom'] = False
                if wall[3] == '0':
                    cell.walls['left'] = False  
                maze.append(cell)
        return game_mode, game_level, maze, Currentpos, Aimpos, time
    elif game_mode == 2:
        score = int(fp.readline())
        time = int(fp.readline())
        game_level = int(fp.readline())
        #Vị trí Tom
        Currentpos = fp.readline().split()
        Currentpos[0] = int(Currentpos[0])
        Currentpos[1] = int(Currentpos[1])
        maze = []
        if game_level == 20:
            create_maze.TILE = 60
            create_maze.cols, create_maze.rows = create_maze.WIDTH // 60, create_maze.HEIGHT // 60
            create_maze.THICK = 4
            for i in range(216): # col = 18, row = 12
                pos = fp.readline().split()
                x, y = int(pos[0]), int(pos[1])
                cell = Cell(x, y)
                wall = fp.readline().split()
                if wall[0] == '0':
                    cell.walls['top'] = False
                if wall[1] == '0':
                    cell.walls['right'] = False
                if wall[2] == '0':
                    cell.walls['bottom'] = False
                if wall[3] == '0':
                    cell.walls['left'] = False  
                maze.append(cell)
        elif game_level == 40:
            create_maze.TILE = 40
            create_maze.cols, create_maze.rows = create_maze.WIDTH // 40, create_maze.HEIGHT // 40
            create_maze.THICK = 3
            for i in range(486): # col = 27, row = 18
                pos = fp.readline().split()
                x, y = int(pos[0]), int(pos[1])
                cell = Cell(x, y)
                wall = fp.readline().split()
                if wall[0] == '0':
                    cell.walls['top'] = False
                if wall[1] == '0':
                    cell.walls['right'] = False
                if wall[2] == '0':
                    cell.walls['bottom'] = False
                if wall[3] == '0':
                    cell.walls['left'] = False  
                maze.append(cell)
        elif game_level == 100:
            create_maze.TILE = 20
            create_maze.cols, create_maze.rows = create_maze.WIDTH // 20, create_maze.HEIGHT // 20
            create_maze.THICK = 2
            for i in range(1944): #col = 54, row = 36
                pos = fp.readline().split()
                x, y = int(pos[0]), int(pos[1])
                cell = Cell(x, y)
                wall = fp.readline().split()
                if wall[0] == '0':
                    cell.walls['top'] = False
                if wall[1] == '0':
                    cell.walls['right'] = False
                if wall[2] == '0':
                    cell.walls['bottom'] = False
                if wall[3] == '0':
                    cell.walls['left'] = False       
                maze.append(cell)
        return game_mode, game_level, maze, Currentpos, time, score
    fp.close()

# print(read_saved_game('easynormal'))
def load_game(username: str):
    game_mode = read_saved_game[0]
    game_level = read_saved_game[1]
    # get maze
    maze = read_saved_game(username)[2]
    maze2D = getMaze2DArray(maze)
    # get Tom position
    CurrentPos = read_saved_game(username)[3]

    if game_mode == 0:
        # get Jerry position
        AimPos = read_saved_game(username)[4]
    elif game_mode == 1:
        AimPos = read_saved_game(username)[4]
        time = read_saved_game(username)[5]
    elif game_mode == 2:
        time = read_saved_game(username)[4]
        score = read_saved_game(username)[5]

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
    return maze, maze2D, walls_collide_list, player_rect.topleft, des_rect.topleft







