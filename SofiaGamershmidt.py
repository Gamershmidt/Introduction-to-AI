import copy
import random
import os

#For gene was implemented Python class which contains following attributes:
    #  Content - the word itself
    # X - x-coordinate of the beginning of the word
    #Y - y-coordinate of the beginning of the word
    #position - 0 for horizontal and 1 for vertical
class Word:
    def __init__(self, content, x, y, position):
        self.content = content
        self.x = x
        self.y = y
        self.position = position

    def __str__(self):
        return f'{self.content} {self.x} {self.y} {self.position}'

    __repr__ = __str__


def read_input(name):
    file = open(name, "r")
    library = [line.strip() for line in file]
    return library

#Checks the intersection of words
def do_intersect(word1, word2):
    if word1.position == word2.position:
        return -1, -1

    if word1.position:
        word1, word2 = word2, word1

    if word1.y <= word2.y <= word1.y + len(word1.content) - 1 and word2.x <= word1.x <= word2.x + len(
            word2.content) - 1:
        return word1.x, word2.y
    return -1, -1

#Using two words and coordinates of intersection, i check whether they intersect at the same letter.
def letter_check(word1, word2, x, y):
    if word1.position:
        word1, word2 = word2, word1
    if word1.content[y - word1.y] == word2.content[x - word2.x]:
        return True
    return False

#That means that each gene will have mutation(random change) of x-coordinate,
# y-coordinate and position (independently, each with probability 0.5).
def mutation(crword):
    for word in crword:
        if random.randint(0, 10) % 2:
            word.position = random.randint(0, 1)
            word.x = random.randint(0, 20 - len(word.content))
            word.y = random.randint(0, 20 - len(word.content))
    return crword

#I use uniform order crossover( Swap all with Probability of 0.5)
def crossover(cross1, cross2):
    temp = []
    for i in range(len(cross1)):
        if random.randint(0, 10) % 2:
            temp.append(cross1[i])
        else:
            temp.append(cross2[i])
    return temp


# def fitness_function(population):
def print_crossword(init):
    crossword = [['.' for _ in range(20)] for _ in range(20)]

    for word in init:
        place_word(word, crossword)
    print('    ' + ' '.join(f'{i:^2}' for i in range(len(crossword[0]))))
    for i, row in enumerate(crossword):
        print(f'{i:<3}', end=' ')
        print(' '.join(f'{cell:^2}' for cell in row))

#Check parallel horizontal/vertical words’ symbols which existing for neighbour
#rows/columns( which is violation of rules)
def adj_check(word1, word2):
    x1, y1 = (word1.x, word1.y)
    x2, y2 = (word2.x, word2.y)
    if do_intersect(word1, word2) != (-1, -1):
        return False
    if word1.position == 1 and word2.position == 0:
        word1, word2 = word2, word1
    if word1.position == 0 and word2.position == 1:

        if do_intersect(Word(word1.content, word1.x + 1, word1.y, 0), word2) != (-1, -1):
            return True
        if do_intersect(Word(word1.content, word1.x - 1, word1.y, 0), word2) != (-1, -1):
            return True
        if do_intersect(Word(word1.content, word1.x, word1.y + 1, 0), word2) != (-1, -1):
            return True
        if do_intersect(Word(word1.content, word1.x, word1.y - 1, 0), word2) != (-1, -1):
            return True
    if word1.position == word2.position:
        if len(word1.content) > len(word2.content):
            word1, word2 = word2, word1
        if word1.position:
            if abs(y1 - y2) <= 1:
                if (x1 < x2) and (x1 + len(word1.content) <= x2 + len(word2.content)):
                    return True
                if (x2 - 1 + len(word2.content) >= x1 >= x2) or (
                        x2 - 1 + len(word2.content) >= x1 + len(word1.content) >= x2):
                    return True
        else:

            if abs(x1 - x2) <= 1:
                if (y1 < y2) and (y1 + len(word1.content) <= y2 + len(word2.content)):
                    return True
                if (y2 - 1 + len(word2.content) >= y1 >= y2) or (
                        y2 - 1 + len(word2.content) >= y1 + len(word1.content) - 1 >= y2):
                    return True
    return False

#supplementary function for prunting crossword
def place_word(word, grid):
    x, y = word.x, word.y
    for letter in word.content:
        grid[x][y] = letter
        if word.position == 0:  # Horizontal
            y += 1
        else:  # Vertical
            x += 1

#I create a hundred of new chromosomes using mutation and crossover.
def make_population(init):
    for i in range(100):
        temp = copy.deepcopy(crossover(init[random.randint(0, len(init) - 1)], init[random.randint(0, len(init) - 1)]))
        if random.randint(0, 1):
            mutation(temp)
        init.append(temp)
    return init


#In this algorithm, fitness function calculates violations of crossword rules
# (each word has to be crossed by at least one another perpendicular word,
# any pair of same orientation words cannot be intersecting,
# Parallel horizontal/vertical words’ symbols shouldn’t be existing for neighbour rows/columns, etc).
# For each violation fitness function decreases total value(higher point means better crossword).
# Therefore, the highest fitness function is 0 for the correct crossword.
def fitness_function(elem):
    point = 0
    point -= (is_connected(elem) - 1) * 2
    for i in range(len(elem) - 1):
        for j in range(i + 1, len(elem)):
            x, y = do_intersect(elem[i], elem[j])
            if (x, y) != (-1, -1):
                if not letter_check(elem[i], elem[j], x, y):
                    point -= 2.5
            if adj_check(elem[i], elem[j]):
                    point -= 5
    return point

#I consider crossword as a graph. To check the connectivity
# i calculate connective components of a graph(two words are connected if they intersect and not parallel) using dfs.
def is_connected(population):
    # Create an adjacency list to represent connections between words
    adjacency_list = {}

    # Populate adjacency_list based on intersections
    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            intersect_x, intersect_y = do_intersect(population[i], population[j])
            if intersect_x != -1 and intersect_y != -1:
                if i not in adjacency_list:
                    adjacency_list[i] = set()
                if j not in adjacency_list:
                    adjacency_list[j] = set()
                adjacency_list[i].add(j)
                adjacency_list[j].add(i)

    # Count connectivity components using Depth-First Search (DFS)
    def dfs(node, visited):
        visited.add(node)
        if node in adjacency_list:
            for neighbor in adjacency_list[node]:
                if neighbor not in visited:
                    dfs(neighbor, visited)

    num_components = 0
    visited = set()

    # Traverse through each word if not visited to count components
    for i in range(len(population)):
        if i not in visited:
            num_components += 1
            dfs(i, visited)

    return num_components


if __name__ == '__main__':
    os.mkdir("outputs")
    size = len(os.listdir('inputs'))
    for k in range(1, size + 1):
        name = "inputs/input" + str(k) + ".txt"
        words = read_input(name)
        init_population = [[Word(words[i], random.randint(0, 20 - len(words[i])),
                                 random.randint(0, 20 - len(words[i])), random.randint(0, 1))
                            for i in range(len(words))] for j in range(len(words))]
        i = 0
        outp = open("outputs/output" + str(k) + ".txt", "w")
        while True:
            i += 1
            make_population(init_population)
            init_population.sort(key=fitness_function)
            if fitness_function(init_population[-1]) == 0:
                for w in (init_population[-1]):
                    outp.write(str(w.x) + " " + str(w.y) + " " + str(w.position) + "\n")
                break
            init_population = copy.deepcopy(init_population[-len(words):])
            if i % (len(words)*1000) == 0:
                init_population = copy.deepcopy([[Word(words[i], random.randint(0, 20 - len(words[i])),
                                         random.randint(0, 20 - len(words[i])), random.randint(0, 1))
                                    for i in range(len(words))] for j in range(len(words))])


