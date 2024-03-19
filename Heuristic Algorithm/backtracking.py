"""
    Class Cell contains information of type of cell
    ( "-" - not visited, "*' - visited, "P" - perception zone
        H,M,T - heroes, "I" - infinity stone, S - shield)
    way - number of cells visited
    x, y - coordinates of previous cells
"""
class Cell():
    def __init__(self, type, way, x, y):
        self.type = type  # Type of the cell ('-', 'P', 'I', '*', etc.)
        self.way = way    # Way attribute for pathfinding
        self.x = x        # X coordinate of the cell
        self.y = y        # Y coordinate of the cell

    def __str__(self):
        return f'| {self.type} ({self.way},{self.x},{self.y})|'

    __repr__ = __str__


# Create a matrix for the game map
def create_matrix(n):
    return [[Cell("-", -1, -1, -1) for _ in range(n)] for _ in range(n)]

# Function to check if a coordinate is within the valid range
def val(x):
    if 0 <= x <= 8:
        return True
    return False

# Initialize the game map
mapGame = create_matrix(9)

# Function to mark neighboring cells with '*'
def check(x, y):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if val(new_x) and val(new_y) and mapGame[new_x][new_y].type == "-":
            mapGame[new_x][new_y].type = "*"

# Functions to mark cells for Hulk, Thor, and Marvel
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
    Backtracking algorithm:
    1) make a move and then read all input information
    2) check all adjacent cells and do backtracking from this points
    3) if there are no other ways - return to previous cell
"""
def backtracking(x, y, scenario):
    print("m", x, y)
    mapGame[x][y].type = "*"
    n = int(input())
    for i in range(n):
        posX, posY, type = input().split()
        posX = int(posX)
        posY = int(posY)
        if type == "S":
            type = "-"
        if scenario == 2:
            if type == "H":
                mark_hulk(posX, posY)
            if type == "T":
                mark_thor(posX, posY)
            if type == "M":
                mark_marvel(posX, posY)
        mapGame[posX][posY].type = type
    check(x, y)
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if val(new_x) and val(new_y) and mapGame[new_x][new_y].type in "*-":
            if mapGame[new_x][new_y].way > mapGame[x][y].way + 1 or mapGame[new_x][new_y].way == -1:
                mapGame[new_x][new_y].way = mapGame[x][y].way + 1
                mapGame[new_x][new_y].x = x
                mapGame[new_x][new_y].y = y
                backtracking(new_x, new_y, scenario)
    if mapGame[x][y].x != -1:
        print("m", mapGame[x][y].x, mapGame[x][y].y)
        for _ in range(int(input())):
            input()



if __name__ == "__main__":
    type = int(input())
    posX, posY = map(int, input().split())
    mapGame[posX][posY].type = "I"
    mapGame[0][0].way = 0
    if type == 1 or type == 2:
        backtracking(0, 0, type)
    else:
        print("Wrong input")
    ans = 1000
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for dx, dy in directions:
        new_x, new_y = posX + dx, posY + dy
        if val(new_x) and val(new_y) and mapGame[new_x][new_y].way + 1 < ans and mapGame[new_x][new_y].way != -1:
            ans = mapGame[new_x][new_y].way + 1
    print("e", -1 if ans == 1000 else ans)
