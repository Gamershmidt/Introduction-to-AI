import copy

"""Class Cell contains information of type of cell
    ( "-" - not visited, "*' - visited, "P" - perception zone
        H,M,T - heroes, "I" - infinity stone, S - shield)
    path - ordered cells that were visited from 0, 0, to current    
"""


class Cell():
    def __init__(self, type, path):
        self.type = type
        self.path = path

    def __str__(self):
        return f'{self.type}'

    __repr__ = __str__


posX = posY = 0


def create_matrix(val, n):
    return [[val for _ in range(n)] for _ in range(n)]


# distances - array for heuristics calculation
distances = create_matrix(0, 9)
mapGame = [[Cell("-", []) for _ in range(9)] for _ in range(9)]


# check if coordinates in matrix
def val(x):
    if 0 <= x <= 8:
        return True
    return False


# calculate complete heuristic for point
def heuristic(tuple):
    x, y = tuple
    return len(mapGame[x][y].path) + distances[x][y]


# Following functions mark full perception zone for hero
def mark_hulk(x, y):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if val(new_x) and val(new_y):
            mapGame[new_x][new_y].type = "P"


def mark_thor(x, y):
    mark_hulk(x, y)
    directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if val(new_x) and val(new_y):
            mapGame[new_x][new_y].type = "P"


def mark_marvel(x, y):
    mark_thor(x, y)
    directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if val(new_x) and val(new_y):
            mapGame[new_x][new_y].type = "P"


""" 
    A* algorithm:
    1) make a move and then read all input information
    2) check all adjacent cells and add it to queue if it was not in queue(and safe)
    3) sort queue and check the cell with smallest heuristics
    4) repeat until queue is empty or I achieved
"""


def a_star(scenario):
    x = y = 0
    queue = []
    flag = False
    queue.append((0, 0))
    while (True):
        print("m", x, y)
        n = int(input())
        for i in range(n):
            temp_x, temp_y, type = input().split()
            temp_x = int(temp_x)
            temp_y = int(temp_y)
            if type == "S":
                type = "-"
            if scenario == 2:
                if type == "H":
                    mark_hulk(temp_x, temp_y)
                if type == "T":
                    mark_thor(temp_x, temp_y)
                if type == "M":
                    mark_marvel(temp_x, temp_y)

            mapGame[temp_x][temp_y].type = type
        mapGame[x][y].type = "*"
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if val(new_x) and val(new_y):
                if mapGame[new_x][new_y].type in "*-S":
                    mapGame[new_x][new_y].dist = distances[new_x][new_y]
                    if mapGame[new_x][new_y].type == "-":
                        queue.append((new_x, new_y))
                        mapGame[new_x][new_y].type = "*"
                    if len(mapGame[new_x][new_y].path) == 0 or len(mapGame[new_x][new_y].path) > len(
                            mapGame[x][y].path) + 1:
                        new_path = copy.deepcopy(mapGame[x][y].path)
                        new_path.append((x, y))
                        mapGame[new_x][new_y].path = new_path
                if new_x == posX and new_y == posY:
                    new_path = copy.deepcopy(mapGame[x][y].path)
                    new_path.append((x, y))
                    mapGame[new_x][new_y].path = new_path
                    flag = True

        if flag:
            break
        queue = queue[1:]

        if not len(queue):
            break
        queue.sort(key=heuristic)
        queue[::-1]
        for i in range(len(mapGame[x][y].path) - 1, 0, -1):
            temp_x, temp_y = mapGame[x][y].path[i]
            print("m", temp_x, temp_y)
            n = int(input())
            for _ in range(n):
                input()
        x, y = queue[0]
        for i in range(len(mapGame[x][y].path)):
            temp_x, temp_y = mapGame[x][y].path[i]
            print("m", temp_x, temp_y)
            n = int(input())
            for _ in range(n):
                input()


#calculate distance from point to i
def find_dist(x, y):
    for i in range(len(distances)):
        for j in range(len(distances)):
            distances[i][j] = abs(i - x) + abs(j - y)


if __name__ == '__main__':
    type = int(input())
    posX, posY = map(int, input().split())
    find_dist(posX, posY)
    a_star(type)
    print("e", len(mapGame[posX][posY].path) if len(mapGame[posX][posY].path) else -1)
