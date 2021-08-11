# pathfinder.py
# A path finding program to find a path on a grid
# using an A* algorithm

import math
from os import readv
import pygame
from pygame.locals import *
import pygame_widgets
from pygame_widgets import button
from pygame_widgets.button import Button

white = [255,255,255]
black = [0,0,0]
blue = [0,128,255]
red = [204,0,0]
green = [0,204,0]
grey = [96,96,96]


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blocked = False


class Graph:
    grid = []

    def __init__(self, n: int):
        for i in range(n):
            temp = []
            for j in range(n):
                temp.append(Node(i,j))
            self.grid.append(temp)


    def get_neighbors(self, node: Node) -> list:
        # return a list of nodes for given neighbor
        neighbors = []
        x = node.x
        y = node.y

        i = x - 1
        j = y - 1

        for n in range(3):
            if i >= 0 and i < len(self.grid):
                if j >= 0 and j < len(self.grid[0]):
                    if self.grid[i][j].blocked == False: 
                        neighbors.append(self.grid[i][j])
            j += 1
    
        i = x + 1
        j = y - 1
        for n in range(3):
            if i >= 0 and i < len(self.grid):
                if j >= 0 and j < len(self.grid[0]):
                    if self.grid[i][j].blocked == False: 
                        neighbors.append(self.grid[i][j])
            j += 1     

        i = x
        j = y - 1
        if i >= 0 and i < len(self.grid):
            if j >= 0 and j < len(self.grid[0]):
                if self.grid[i][j].blocked == False: 
                    neighbors.append(self.grid[i][j])

        j = y + 1
        if i >= 0 and i < len(self.grid):
            if j >= 0 and j < len(self.grid[0]):
                if self.grid[i][j].blocked == False: neighbors.append(self.grid[i][j])

        return neighbors   


def reconstruct_path(came_from: dict, current: Node) -> list:
    total_path = []
    while current in came_from.keys():
        total_path.insert(0, current)
        current = came_from[current]
    return total_path


def a_star(graph: Graph, start: Node, goal: Node):
    # taken from https://en.wikipedia.org/wiki/A*_search_algorithm
    open_set = [start]
    came_from = {}
    g_scores = {}
    f_scores = {}

    for row in graph.grid:
        for n in row:
            g_scores[n] = math.inf
            f_scores[n] = math.inf
            came_from[n] = None

    g_scores[start] = 0
    f_scores[start] = distance(start, goal)

    while open_set != []:
        f_scores_sorted = sorted(f_scores.items(), key=lambda x:x[1])
        current = f_scores_sorted[0][0]

        if current == goal:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        f_scores.pop(current)
        neighbors = graph.get_neighbors(current)
        for item in neighbors:
            tentative_g_score = g_scores[current] + distance(current, item)

            if tentative_g_score < g_scores[item]:
                came_from[item] = current
                g_scores[item] = tentative_g_score
                f_scores[item] = g_scores[item] + distance(item, goal)
                
                if item not in open_set:
                    open_set.append(item)    
    
    return print("No path")


def distance(p1: Node, p2: Node):
    # heuristic is simply distance formula for coordinates
    return (math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2))


def sort_func(node: Node):
    return node["score"]


def set_flag(flag: list, val: int):
    flag[0] = val


def print_path(screen, path: list):
    for item in path:
        pygame.draw.rect(screen, [9,255,0], (item.x*20, item.y*20 + 40, 20, 20), width=0)


def main():
    pygame.init()
    screen_width = 600
    screen_height = 640
    offset = 40
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption("A* Pathfinder")

    graph = Graph(30)
    start = None
    goal = None
    path = []
    flag = [0]
    
    screen.fill(white)
    for i in range(len(graph.grid)):
        for j in range(len(graph.grid[0])):
            pygame.draw.rect(screen, black, (i*20, j*20 + 40, 20, 20), width=1)
 
    start_button = Button(screen, 50, 10, 60, 25, text='start', textColour=white, fontsize=16, 
    inactiveColour=blue, pressedColour=(0,255,0), radius=10, onClick=set_flag, onClickParams=(flag, 1))

    goal_button = Button(screen, 150, 10, 60, 25, text='goal', textColour=white, fontsize=16, 
    inactiveColour=red, pressedColour=(0,255,0), radius=10, onClick=set_flag, onClickParams=(flag, 2))

    run_button = Button(screen, 250, 10, 60, 25, text='run', textColour=white, fontsize=16, 
    inactiveColour=green, pressedColour=(0,255,0), radius=10, onClick=set_flag, onClickParams=(flag, 3))

    reset_button = Button(screen, 350, 10, 60, 25, text='reset', textColour=white, fontsize=16, 
    inactiveColour=grey, pressedColour=(0,255,0), radius=10, onClick=set_flag, onClickParams=(flag, 4))

    pygame.display.update()
    
    game_loop = True
    while game_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                pos = [(int)(x / 20), (int)((y-offset) / 20)]
                x = pos[0]
                y = pos[1]

                if flag[0] == 0:
                    if y > 0:
                        pygame.draw.rect(screen, black, (x*20, y*20 + offset, 20, 20), width=0)
                        graph.grid[x][y].blocked = True

                if flag[0] == 1:
                    # set starting node
                    if start != None:
                        pygame.draw.rect(screen, white, (start.x*20, start.y*20 + offset, 20, 20), width=0)
                        pygame.draw.rect(screen, black, (start.x*20, start.y*20 + offset, 20, 20), width=1)

                    pygame.draw.rect(screen, blue, (x*20, y*20 + offset, 20, 20), width=0)
                    start = graph.grid[x][y]
                    flag[0] = 0

                if flag[0] == 2:
                    # set goal node
                    if goal != None:
                        pygame.draw.rect(screen, white, (goal.x*20, goal.y*20 + offset, 20, 20), width=0)
                        pygame.draw.rect(screen, black, (goal.x*20, goal.y*20 + offset, 20, 20), width=1)

                    pygame.draw.rect(screen, red, (x*20, y*20 + offset, 20, 20), width=0)
                    goal = graph.grid[x][y]
                    flag[0] = 0

                if flag[0] == 3:
                    # perform pathfinding
                    if start != None and goal != None:
                        path = a_star(graph, start, goal)
                        print_path(screen, path)
                    flag[0] = 0
    
                if flag[0] == 4:
                    # reset screen
                    graph = Graph(30)
                    start = None
                    goal = None
                    path = []
                    flag[0] = 0
                    screen.fill(white)
                    for i in range(len(graph.grid)):
                        for j in range(len(graph.grid[0])):
                            pygame.draw.rect(screen, black, (i*20, j*20 + 40, 20, 20), width=1)    

        pygame_widgets.update(event)
        pygame.display.update()
            

if __name__ == '__main__':
    main()