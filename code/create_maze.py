import pygame
from random import choice, randint, randrange
import numpy as np
import algorithm

RES = WIDTH, HEIGHT = 1080, 720
TILE = 60
THICK = 4

cols, rows = WIDTH // TILE, HEIGHT // TILE

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = THICK
        self.status = 1

    def draw(self, sc):
        x, y = self.x * TILE, self.y * TILE
        if self.walls['top']:
            pygame.draw.rect(sc, pygame.Color('green4'), pygame.Rect(x-self.thickness,y-self.thickness,TILE+2*self.thickness,self.thickness))
        if self.walls['right']:
            pygame.draw.rect(sc, pygame.Color('green4'), pygame.Rect(x+TILE,y-self.thickness,self.thickness,TILE+2*self.thickness))
        if self.walls['bottom']:
            pygame.draw.rect(sc, pygame.Color('green4'), pygame.Rect(x-self.thickness,y+TILE,TILE+2*self.thickness,self.thickness))
        if self.walls['left']:
            pygame.draw.rect(sc, pygame.Color('green4'), pygame.Rect(x-self.thickness,y-self.thickness,self.thickness,TILE+2*self.thickness))
            
    def color_cell(self, sc, color):
        pygame.draw.rect(sc, pygame.Color(color),((self.x*TILE), (self.y*TILE), TILE, TILE))
        self.draw(sc)


    # def draw(self, sc):
    #     x, y = self.x * TILE, self.y * TILE
    #     if self.walls['top']:
    #         pygame.draw.line(sc, pygame.Color('black'), (x - 1, y), (x + TILE + 1, y), self.thickness)
    #     if self.walls['right']:
    #         pygame.draw.line(sc, pygame.Color('black'), (x + TILE, y - 1), (x + TILE, y + TILE + 1), self.thickness)
    #     if self.walls['bottom']:
    #         pygame.draw.line(sc, pygame.Color('black'), (x + TILE - 1, y + TILE), (x + 1, y + TILE), self.thickness)
    #     if self.walls['left']:
    #         pygame.draw.line(sc, pygame.Color('black'), (x, y + TILE - 1), (x, y + 1), self.thickness)

    def get_rects(self):
        rects = []
        x, y = self.x * TILE, self.y * TILE
        if self.walls['top']:
            rects.append(pygame.Rect(x-self.thickness,y-self.thickness,TILE+2*self.thickness,self.thickness))
        if self.walls['right']:
            rects.append(pygame.Rect(x+TILE,y-self.thickness,self.thickness,TILE+2*self.thickness))
        if self.walls['bottom']:
            rects.append(pygame.Rect(x-self.thickness,y+TILE,TILE+2*self.thickness,self.thickness))
        if self.walls['left']:
            rects.append(pygame.Rect(x-self.thickness,y-self.thickness,self.thickness,TILE+2*self.thickness))
        return rects

    
    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]
        
    def check_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
    
    def rand_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top:
            neighbors.append(top)
        if right:
            neighbors.append(right)
        if bottom:
            neighbors.append(bottom)
        if left:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
    
    def make_tom_pos(self):
        self.status = 2
    def make_jerry_pos(self):
        self.status = 3
    def make_blank(self):
        self.status = 1

    def make_blank(self):
        self.status = 1

def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

def generate_maze():
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    array = []
    break_count = 1
    while break_count != len(grid_cells):
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells)
        if next_cell:
            next_cell.visited = True
            break_count += 1
            array.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif array:
            current_cell = array.pop()
    for i in range(40):
        current_cell = choice(grid_cells)
        next_cell = grid_cells[grid_cells.index(current_cell)].rand_neighbors(grid_cells)
        if next_cell == False:
            continue
        remove_walls(current_cell, next_cell)
    print(rows,cols)
    return grid_cells
