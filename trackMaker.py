import pygame as p
import os

direct = os.getcwd()
p.init()

width = 1000
height = 1000
win = p.display.set_mode((width, height))

green = (0,250,0)
grey = (100,100,100)
yellow = (255,250,0)
black = (0,0,0)
grid_slot_color = (170,170,170)
finish_line_color = (255,255,255)
check_point_color = (110,110,110)

grid_length = 150
grid_height = 150

tile_length = width / grid_length
tile_height = tile_length


def check_event():
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            #quit()

        if event.type == p.KEYDOWN:
            return (True, event.key)

    return (p.mouse.get_pos(), p.mouse.get_pressed())


def write_text(txt ,x, y, size, color):
    
    text = p.font.SysFont('timesnewroman', size)
    textsurface = text.render(txt, False, color)
    win.blit(textsurface, (x, y))


def fill_square(grid, pos, color, pencil_size):
    for i in range(pencil_size):
        for j in range(pencil_size):
            grid[pos[1] + i][pos[0] + j] = color

    
def update_grid(grid, event, color, pencil_size):

    if not event:
        return
    
    if event[1] != (1, 0, 0):
        return

    for y in range(grid_height):
        if y * tile_height < event[0][1] < y * tile_height + tile_height:
            for x in range(grid_length):
                if x * tile_length < event[0][0] < x * tile_length + tile_length:
                    fill_square(grid, (x, y), color, pencil_size)
                    

def draw_grid(grid):

    win.fill(green)

    for y in range(grid_height):
        for x in range(grid_length):
            if grid[y][x] != None:
                p.draw.rect(win, grid[y][x], (x * tile_length, y * tile_height, tile_length, tile_height))


def save_file(grid):

    file_name = raw_input("filename(xyz.txt): ")

    with open(direct + "\\tracks\\" + file_name, "w") as open_file:
        for row in grid:
            for character in row:
                
                if character == green:
                    open_file.write("green ")
                    
                elif character == yellow:
                    open_file.write("yellow ")
                    
                elif character == grey:
                    open_file.write("grey ")

                elif character == black:
                    open_file.write("black ")

                elif character == grid_slot_color:
                    open_file.write("slot ")

                elif character == finish_line_color:
                    open_file.write("finish ")

                elif character == check_point_color:
                    open_file.write("checkpoint ")
                    
                else:
                    open_file.write(str(character) + " ")
                
            open_file.write("\n")


def load_file():
    
    file_name = raw_input("file name (xyz.txt):" )
    grid = []

    with open(direct + "\\tracks\\" + file_name, "r") as open_file:
        for row in open_file:
            grid.append([row])

    new_grid = []
    
    for row in grid:
        for char in row:
            temp = char.split(" ")
            
        new_grid.append(temp)

    for row in range(len(new_grid)):
        for obj in range(len(new_grid[row])):
            
            if new_grid[row][obj] == "None":
                new_grid[row][obj] = None

            elif new_grid[row][obj] == "grey":
                new_grid[row][obj] = grey

            elif new_grid[row][obj] == "yellow":
                new_grid[row][obj] = yellow

            elif new_grid[row][obj] == "black":
                new_grid[row][obj] = black

            elif new_grid[row][obj] == "slot":
                new_grid[row][obj] = grid_slot_color

            elif new_grid[row][obj] == "finish":
                new_grid[row][obj] = finish_line_color

            elif new_grid[row][obj] == "checkpoint":
                new_grid[row][obj] = check_point_color

    for row in range(len(new_grid)):
        new_grid[row].remove("\n")

    return new_grid


def print_choices():
    
    print "1 = grey"
    print "2 = green"
    print "3 = yellow"
    print "4 = black"
    print "5 = grid slot"
    print "6 = finish line"
    print "7 = checkpoint"
    print "8 = save track"
    print "9 = load track"


def update_settings_list(event, settings_list, grid, pencil_size):

    if event[0] != True:
        return grid
    
    if event[1] == p.K_1:
        print "color = grey"
        settings_list[0] = grey
            
    elif event[1] == p.K_2:
        print "color = green"
        settings_list[0] = None
            
    elif event[1] == p.K_3:
        print "color = yellow"
        settings_list[0] = yellow

    elif event[1] == p.K_4:
        print "color = black"
        settings_list[0] = black

    elif event[1] == p.K_5:
        print "grid slot"
        settings_list[0] = grid_slot_color

    elif event[1] == p.K_6:
        print "finish line"
        settings_list[0] = finish_line_color

    elif event[1] == p.K_7:
        print "checkpoint"
        settings_list[0] = check_point_color

    elif event[1] == p.K_8:
        print "saving file"
        save_file(grid)

    elif event[1] == p.K_9:
        print "loadig file"
        grid = load_file()

    """elif event[1] == p.K_Q:
        pencil_size += 1

    elif event[1] == p.K_A:
        pencil_size -= 1

    if pencil_size < 1:
        pencil_size = 1"""
        
    print_choices()
    return grid

    
def main():

    print_choices()
    settings_list = [grey]
    grid = [[None for i in range(grid_length)] for j in range(grid_height)]
    pencil_size = 1

    while True:

        event = check_event()
        update_grid(grid, event, settings_list[0], pencil_size)
        grid = update_settings_list(event, settings_list, grid, pencil_size)
        draw_grid(grid)
        
        
        p.display.update()

main()













