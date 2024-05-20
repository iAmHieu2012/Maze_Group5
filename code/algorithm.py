import numpy as np
import create_maze

MODE = 50


def getMaze2DArray(maze):
    """
    Chuyển listCell thành ma trận 2 chiều
    """
    return np.array(maze).reshape(create_maze.rows, create_maze.cols)


def isAbleToEnter(currP, neighP, maze2DArray, wall):
    """
    Kiểm tra các ô bên cạnh có thể đi vào hay không
    neighP nằm theo hướng của wall
    """
    return (
        (0 <= neighP[0] < maze2DArray.shape[0])
        and (0 <= neighP[1] < maze2DArray.shape[1])
        and (not maze2DArray[currP[0]][currP[1]].walls[wall])
    )


def dfs(srcPoint, destPoint, maze2DArray, path, visited):
    """
    Thuật toán DFS
    """
    visited.add(srcPoint)
    if srcPoint == destPoint:
        return path + [srcPoint]
    for dr, dc, wall in [
        (-1, 0, "top"),
        (1, 0, "bottom"),
        (0, -1, "left"),
        (0, 1, "right"),
    ]:
        neighRow, neighCol = srcPoint[0] + dr, srcPoint[1] + dc
        neighPoint = (neighRow, neighCol)
        if neighPoint not in visited and isAbleToEnter(
            srcPoint, neighPoint, maze2DArray, wall
        ):
            result = dfs(neighPoint, destPoint, maze2DArray, path + [srcPoint], visited)
            if result:
                return result

    return None


def bfs(srcPoint, destPoint, maze2DArray, visited):
    """
    Thuật toán BFS
    """
    queue = []
    path = [srcPoint]
    queue.append((srcPoint, path))
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
            neighPoint = (neighRow, neighCol)
            if isAbleToEnter(curr[0], neighPoint, maze2DArray, wall):
                if neighPoint not in visited:
                    newPath = curr[1] + [neighPoint]
                    queue.append((neighPoint, newPath))
                    visited.add(neighPoint)

    return None


def generateTomAndJerryPos(maze):
    """
    Random vị trí tom và jerry
    """
    tom = (
        np.random.randint(0, create_maze.rows),
        np.random.randint(0, create_maze.cols),
    )
    jerry = (
        np.random.randint(0, create_maze.rows),
        np.random.randint(0, create_maze.cols),
    )
    maze2DArray = getMaze2DArray(maze)

    while (
        not bfs(tom, jerry, maze2DArray, visited=set())
        or len(bfs(tom, jerry, maze2DArray, visited=set())) < MODE
    ):
        tom = (
            np.random.randint(0, create_maze.rows),
            np.random.randint(0, create_maze.cols),
        )
        jerry = (
            np.random.randint(0, create_maze.rows),
            np.random.randint(0, create_maze.cols),
        )
    maze2DArray[tom[0]][tom[1]].make_tom_pos()
    maze2DArray[jerry[0]][jerry[1]].make_jerry_pos()
    return list(maze2DArray.flatten())


def findTomAndJerryPos(maze2DArray):
    """
    Lấy vị trí của tom và jerry
    """
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


def findPathBetween2Point(maze, algo: int):
    """
    Tỉm đường đi theo 2 thuật toán
    """
    maze2DArray = getMaze2DArray(maze)

    tom, jerry = findTomAndJerryPos(maze2DArray)
    if tom == (-1, -1) or jerry == (-1, -1):
        return None
    if algo == 1:
        visited = set()
        return dfs(tom, jerry, maze2DArray, [], visited)
    elif algo == 2:
        visited = set()
        return bfs(tom, jerry, maze2DArray, visited)


def getPathCellList(path, maze2DArray):
    """
    Chuyển list vị trí thành list các Cell
    """
    result = []
    if path:
        for cell in path:
            result.append(maze2DArray[cell[0]][cell[1]])
    return result


if __name__ == "__main__":
    maze = create_maze.generate_maze()
    generateTomAndJerryPos(maze)

    path = findPathBetween2Point(maze, algo=1)
    path_cell_list = getPathCellList(path, maze2DArray=getMaze2DArray(maze))
    if path:
        print("Lối đi:\n", path)
    # print(path_cell_list)
    for cell in path_cell_list:
        print(cell.x, cell.y, cell.walls)
