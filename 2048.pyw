import pygame
from pygame.locals import *

import time
from math import log2
from random import choice

class Background:
    def __init__(self):
        self.empty = tile_shape((200, 200, 200))

    def update(self):
        screen.fill((150, 150, 150))
        for x in range(4):
            for y in range(4):
                screen.blit(self.empty, (5 + x * 160, 5 + y * 160))

class Tile:
    def __init__(self, pos):
        self.spawn_time = time.time()
        self.move_time = self.merge_time = 0
        self.value = choice([2, 4]) # the value can be 2 or 4
        self.image = tile_shape(color(self.value))
        self.pos = self.prev_pos = pos

    def draw(self):
        if time.time() - self.spawn_time < 0.1:
            size = min(150, int((time.time() - self.spawn_time) * 1600))
            image = pygame.transform.scale(self.image, (size, size))
        elif 0.1 < time.time() - self.merge_time < 0.2: # play this animation after the moving animation
            size = max(150, 150 + int((0.2 - time.time() + self.move_time) * 400))
            image = pygame.transform.scale(self.image, (size, size))
        else:
            image = self.image
        
        if time.time() - self.move_time < 0.1: # moving animation
            x_move = int((time.time() - self.move_time) * (self.pos[0] - self.prev_pos[0]) * 1600)
            y_move = int((time.time() - self.move_time) * (self.pos[1] - self.prev_pos[1]) * 1600)

            pos = [80 + self.prev_pos[0] * 160 + x_move, 80 + self.prev_pos[1] * 160 + y_move]
        else:
            pos = [80 + self.pos[0] * 160, 80 + self.pos[1] * 160]

        w, h = image.get_size()
            
        screen.blit(image, (int(pos[0] - w / 2), int(pos[1] - h / 2)))

        if time.time() - self.spawn_time >= 0.1: # display the text once completely spawned
            text = title.render(str(self.value), 0, (0, 0, 0))
            w, h = text.get_size()
            screen.blit(text, (int(pos[0] - w / 2), int(pos[1] - h / 2)))

    def move(self, pos, merge):
        self.move_time = time.time()
        if merge:
            self.merge_time = time.time()
        self.prev_pos = self.pos
        self.pos = pos

def find(pos):
    for tile in tiles:
        if tile.pos == pos:
            return tile

def add_tile(add=True): # add is to avoid adding another tile if nothig changed
    empty = []
    for x in range(4):
        for y in range(4):
            if find((x, y)) is None: # empty space
                empty.append((x, y))

    if len(empty):
        if add:
            tiles.append(Tile(choice(empty))) # add a tile
    else:
        can_merge = False # check for any possible move
        for x in range(4):
            for y in range(4):
                value = find((x, y)).value
                for x_, y_ in ([-1, 0], [0, -1], [1, 0], [0, 1]): # check for each tile if a neighbour has the same value
                    neighbour = find((x + x_, y + y_))
                    if neighbour:
                        if neighbour.value == value:
                            can_merge = True

        if not can_merge:
            global game_over
            game_over = True # no place to add another tile

def move_left():
    global score
    for y in range(4):
        for x in range(4):
            tile = find((x, y))
            if tile: # if there is a tile to move
                merge = False
                tiles_to_left = [find((x_, y)) for x_ in range(x) if find((x_, y))]
                if len(tiles_to_left):
                    tile_ = tiles_to_left[-1]
                    if tile_.value == tile.value: # merge together
                        tiles.remove(tile_)
                        tile.value *= 2
                        score += tile.value
                        merge = True
                        tile.image = tile_shape(color(tile.value))
                        final_pos = tile_.pos
                    else: # stop next to it
                        final_pos = (tile_.pos[0] + 1, tile_.pos[1])
                else: # no tiles: go to the left side of the screen
                    final_pos = (0, y)
                tile.move(final_pos, merge)

def move_right():
    global score
    for y in range(4):
        for x in range(3, -1, -1):
            tile = find((x, y))
            if tile:
                merge = False
                tiles_to_right = [find((x_, y)) for x_ in range(x + 1, 4) if find((x_, y))]
                if len(tiles_to_right):
                    tile_ = tiles_to_right[0]
                    if tile_.value == tile.value:
                        tiles.remove(tile_)
                        tile.value *= 2
                        score += tile.value
                        merge = True
                        tile.image = tile_shape(color(tile.value))
                        final_pos = tile_.pos
                    else:
                        final_pos = (tile_.pos[0] - 1, tile_.pos[1])
                else:
                    final_pos = (3, y)
                tile.move(final_pos, merge)

def move_up():
    global score
    for x in range(4):
        for y in range(4):
            tile = find((x, y))
            if tile:
                merge = False
                tiles_to_top = [find((x, y_)) for y_ in range(y) if find((x, y_))]
                if len(tiles_to_top):
                    tile_ = tiles_to_top[-1]
                    if tile_.value == tile.value: # merge together
                        tiles.remove(tile_)
                        tile.value *= 2
                        score += tile.value
                        merge = True
                        tile.image = tile_shape(color(tile.value))
                        final_pos = tile_.pos
                    else:
                        final_pos = (tile_.pos[0], tile_.pos[1] + 1)
                else:
                    final_pos = (x, 0)
                tile.move(final_pos, merge)

def move_down():
    global score
    for x in range(4):
        for y in range(3, -1, -1):
            tile = find((x, y))
            if tile:
                merge = False
                tiles_to_bottom = [find((x, y_)) for y_ in range(y + 1, 4) if find((x, y_))]
                if len(tiles_to_bottom):
                    tile_ = tiles_to_bottom[0]
                    if tile_.value == tile.value:
                        tiles.remove(tile_)
                        tile.value *= 2
                        score += tile.value
                        merge = True
                        tile.image = tile_shape(color(tile.value))
                        final_pos = tile_.pos
                    else:
                        final_pos = (tile_.pos[0], tile_.pos[1] - 1)
                else:
                    final_pos = (x, 3)
                tile.move(final_pos, merge)

def user_control(events):
    for event in events:
        if event.type == KEYDOWN:
            grid = [tile.pos for tile in tiles]
            if event.key == K_LEFT:
                move_left()
            elif event.key == K_RIGHT:
                move_right()
            elif event.key == K_UP:
                move_up()
            elif event.key == K_DOWN:
                move_down()
            
            add_tile([tile.pos for tile in tiles] != grid)

def color(value):
    power = log2(value)
    
    r = max(0, 255 - (power - 1) * 51)
    g = 255
    b = max(0, 255 - (power - 1) * 51 - 255)
    
    return (int(r), int(g), int(b))

def tile_shape(color):
    tile = pygame.Surface((150, 150), SRCALPHA)
    
    pygame.draw.rect(tile, color, Rect((0, 10), (150, 130)))
    pygame.draw.rect(tile, color, Rect((10, 0), (130, 150)))
    pygame.draw.circle(tile, color, (10, 10), 10)
    pygame.draw.circle(tile, color, (140, 10), 10)
    pygame.draw.circle(tile, color, (10, 140), 10)
    pygame.draw.circle(tile, color, (140, 140), 10)

    return tile

pygame.init()

screen = pygame.display.set_mode((640, 640))
font = pygame.font.SysFont('comic sans ms', 20)
title = pygame.font.SysFont('comic sans ms', 50)
clock = pygame.time.Clock()

bg = Background()
tiles = []

game_over = False
time_passed = 0
score = 0

add_tile()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            exit()

    if game_over:
        black = pygame.Surface((640, 640), SRCALPHA)
        black.fill((0, 0, 0))

        time_died = time.time()
        respawn = False
        while not respawn or time.time() - time_died < 2: # respawn after at least 2 seconds
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN: # new game
                    respawn = True
            
            black.set_alpha(min(127, int((time.time() - time_died) * 63)))
            
            bg.update()
            for tile in tiles:
                tile.draw()
            screen.blit(black, (0, 0))
            
            text = title.render('You lost!', 0, (255, 255, 255))
            w = int(text.get_width() / 2)
            screen.blit(text, (320 - w, 200))
            text = font.render('Score: %d' %score, 0, (0, 0, 0))
            w = int(text.get_width() / 2)
            screen.blit(text, (320 - w, 260))

            pygame.display.flip()

        tiles = []
        add_tile()
        game_over = False
        score = 0
    else:
        user_control(events) # also send the events to player control

    bg.update()
    for tile in tiles:
        tile.draw()
    screen.blit(font.render('Score: %d' %score, 0, (0, 0, 0)), (10, 10))

    pygame.display.flip()
    time_passed = clock.tick(60)
