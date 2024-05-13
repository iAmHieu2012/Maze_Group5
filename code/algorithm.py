import numpy as np
import create_maze


def getMaze2DArray(maze):
    '''
    Chuyển listCell thành ma trận 2 chiều
    '''
    return np.array(maze).reshape(create_maze.rows, create_maze.cols)


def isAbleToEnter(row, col, maze2DArray, wall):
    """
    Kiểm tra các ô bên cạnh có thể đi vào hay không
    """
    return (
        (0 <= row < maze2DArray.shape[0])
        and (0 <= col < maze2DArray.shape[1])
        and (maze2DArray[row][col].walls[wall])
    )


def dfs(srcPoint, destPoint, maze2DArray, path, visited):
    """
    Thuật toán DFS
    """
    if srcPoint == destPoint:
        return path + [srcPoint]

    visited.add(srcPoint)

    for dr, dc, wall in [
        (-1, 0, "top"),
        (1, 0, "bottom"),
        (0, -1, "left"),
        (0, 1, "right"),
    ]:
        neighRow, neighCol = srcPoint[0] + dr, srcPoint[1] + dc
        if (neighRow, neighCol) not in visited and isAbleToEnter(neighRow, neighCol,maze2DArray, wall):
            result = dfs((neighRow,neighCol),destPoint,maze2DArray, path + [srcPoint], visited)
            if result:
                return result

    return None


def bfs(srcPoint, destPoint, maze2DArray,visited):
    """
    Thuật toán BFS
    """
    queue = []
    path = [srcPoint]
    queue += [(srcPoint, path)]
    visited.add(srcPoint)
    while queue != []:
        curr = queue[0]
        queue.remove(curr)
        visited.add(curr[0])
        if curr[0] == destPoint:
            return curr[1]
        for dr, dc, wall in [
            (-1, 0, "top"),
            (1, 0, "bottom"),
            (0, -1, "left"),
            (0, 1, "right"),
        ]:
            neighRow, neighCol = (curr[0][0] + dr, curr[0][1] + dc)
            if isAbleToEnter(neighRow, neighCol, maze2DArray, wall):
                if (neighRow, neighCol) not in visited:
                    newPos = (neighRow, neighCol)
                    newPath = curr[1] + [(newPos)]
                    queue.append((newPos, newPath))
                    visited.add(newPos)

    return None


def generateTomAndJerryPos(maze):
    '''
    Random vị trí tom và jerry
    '''
    tom = (
        np.random.randint(0, create_maze.rows),
        np.random.randint(0, create_maze.cols),
    )
    jerry = (
        np.random.randint(0, create_maze.rows),
        np.random.randint(0, create_maze.cols),
    )
    maze2DArray = getMaze2DArray(maze)

    while not bfs(tom, jerry,maze2DArray, visited=set()):
        tom = (
            np.random.randint(0, create_maze.rows),
            np.random.randint(0, create_maze.cols)
        )
        jerry = (
            np.random.randint(0, create_maze.rows),
            np.random.randint(0, create_maze.cols)
        )
    maze2DArray[tom[0]][tom[1]].make_tom_pos()
    maze2DArray[jerry[0]][jerry[1]].make_jerry_pos()
    return list(maze2DArray.flatten())



def findTomAndJerryPos(maze2DArray):
    '''
    Lấy vị trí của tom và jerry
    '''
    TomPos = (-1, -1)
    JerryPos = (-1, -1)
    for i in range(maze2DArray.shape[0]):
        for j in range(maze2DArray.shape[1]):
            if maze2DArray[i][j].status == 2:
                TomPos = (i, j)
                continue
            elif maze2DArray[i][j].status == 3:
                JerryPos = (i, j)
                continue
            
    return (TomPos, JerryPos)


def findPathBetween2Point(n, maze, algo: int):
    '''
    Tỉm đường đi theo 2 thuật toán
    '''
    maze2DArray = getMaze2DArray(maze)

    tom, jerry = findTomAndJerryPos(maze2DArray)
    if algo == 1:
        visited = set()
        return dfs(tom, jerry, maze2DArray, [], visited)
    elif algo == 2:
        visited = set()
        return bfs(tom, jerry, maze2DArray, visited)
    
def getPathCellList(path, maze2DArray):
    '''
    Chuyển list vị trí thành list các Cell
    '''
    result = []
    for cell in path:
        result.append(maze2DArray[cell[0]][cell[1]])
    return result

if __name__ == "__main__":
    maze = create_maze.generate_maze()
    generateTomAndJerryPos(maze)

    path = findPathBetween2Point(1, maze, algo=1)
    path_cell_list = getPathCellList(path)
    if path:
        print("Lối đi:\n", path)
