import numpy as np


def findTomAndJerryPos(maze):
    TomPos = (-1, -1)
    JerryPos = (-1, -1)
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i][j] == 2:
                TomPos = (i, j)
                continue
            elif maze[i][j] == 3:
                JerryPos = (i, j)
                continue
    return TomPos, JerryPos


def findPathBetween2Point(n, maze, algo: int):

    TomPos, JerryPos = findTomAndJerryPos(maze)

    def isAbleToEnter(row, col):
        """
        Kiểm tra các ô bên cạnh có thể đi vào hay không
        """
        return (
            (0 <= row < maze.shape[0])
            and (0 <= col < maze.shape[1])
            and (maze[row][col] >= 1)
        )

    def dfs(row, col, path):
        """
        Thuật toán DFS
        """

        if (row, col) == JerryPos:
            return path + [(row, col)]

        visited.add((row, col))

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighRow, neighCol = row + dr, col + dc
            if (neighRow, neighCol) not in visited and isAbleToEnter(
                neighRow, neighCol
            ):
                result = dfs(neighRow, neighCol, path + [(row, col)])
                if result:
                    return result

        return None

    def bfs(row, col):
        """
        Thuật toán BFS
        """
        queue = []
        path = [(row, col)]
        queue += [((row, col), path)]
        visited.add((row,col))
        while queue != []:
            currQP = queue[0]
            queue.remove(currQP)
            visited.add(currQP[0])
            if currQP[0] == JerryPos:
                return currQP[1]
            for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, 1)]:
                neighRow, neighCol = (
                    currQP[0][0] + dr,
                    currQP[0][1] + dc,
                )
                if isAbleToEnter(neighRow, neighCol):
                    if (neighRow,neighCol) not in visited:
                        newPos = (neighRow, neighCol)
                        newPath = currQP[1] + [(newPos)]
                        queue.append((newPos, newPath))
                        visited.add(newPos)

        return None

    if algo == 1:
        visited = set()
        return dfs(TomPos[0], TomPos[1], [])
    elif algo == 2:
        visited = set()
        return bfs(TomPos[0], TomPos[1])


maze = np.array([
[1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 2, 1, 0, 0, 1, 0, 1, 0],
[0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
[1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
[0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
[0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
[0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
[0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0],
[1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 3],
[1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0],
[0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1],
[0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
[1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
[0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1],
[0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0],
[0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
])
path = findPathBetween2Point(1, maze, algo=1)
if path:
    print("Lối đi:\n", path)
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if (i, j) in path:
                print("○", end="")
            elif maze[i][j] == 1:
                print(" ", end="")
            else:
                print("■", end="")
        print()
else:
    print("Tâm cook, Gia Huy không thể bị bắt.")
path = findPathBetween2Point(1, maze, algo=2)
if path:
    print("Lối đi:\n", path)
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if (i, j) in path:
                print("○", end="")
            elif maze[i][j] == 1:
                print(" ", end="")
            else:
                print("■", end="")
        print()
else:
    print("Tâm cook, Gia Huy không thể bị bắt.")
