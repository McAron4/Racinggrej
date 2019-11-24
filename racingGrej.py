import pygame as p
import os
import math
import time
import physics

direct = os.getcwd()
p.init()
p.mixer.init()
clock = p.time.Clock()

UP = 119
DOWN = 115
LEFT = 97
RIGHT = 100
ESC = 27
ENTER = 13

fullscreen = True

if fullscreen:
    width = 1920
    height = 1080
    win = p.display.set_mode((width, height), p.FULLSCREEN)

else:
    width = 1000
    height = 800
    win = p.display.set_mode((width, height))
    
visible_screen_length = 20
visible_screen_height = visible_screen_length * height / float(width)

green = (0,250,0)
grey = (100,100,100)
yellow = (255,250,0)
black = (0,0,0)
grid_slot_color = (170,170,170)
finish_line_color = (255,255,255)
check_point_color = (110,110,110)

original_p_car_surface = None 
car_size = int(0.6 * (width /visible_screen_length))
original_p_car_surface = None 
mini_map_surface = None

track_list = os.listdir(direct + "/tracks")
track_index = None
car_list = os.listdir(direct + "/cars")

draw_square_numbers = False

grid = None
p_car = None
tile_length = None
screen_tile_length = None
coordinate_ratio = None

engine_sound = p.mixer.Sound("engine")

#---------------------------Start-screen---------------------------------------------

def get_current_choice(current_choice, event):
    if event == UP:
        current_choice -= 1

    if event == DOWN:
        current_choice += 1

    if current_choice > 3:
        current_choice = 0

    if current_choice < 0:
        current_choice = 3

    return current_choice


def correct_settings_range(settings, car_list, track_list):
    if settings[0] > len(car_list) - 1:
        settings[0] = 0
    if settings[0] < 0:
        settings[0] = len(car_list) - 1

    if settings[1] > len(track_list) - 1:
        settings[1] = 0
    if settings[1] < 0:
        settings[1] = len(track_list) - 1

    if settings[2] > 60:
        settings[2] = 10
    if settings[2] < 10:
        settings[2] = 60

    return settings

    
def update_current_settings(settings, current_choice, car_list, track_list, event):
    if event == RIGHT:
        if current_choice == 2:
            settings[current_choice] += 10
        else:
            settings[current_choice] += 1

    if event == LEFT:
        if current_choice == 2:
            settings[current_choice] -= 10
        else:
            settings[current_choice] -= 1

    settings = correct_settings_range(settings, car_list, track_list)
    return settings


def display_settings(settings, current_choice, car_list, track_list):
    color_list = [black for i in range(4)]
    color_list[current_choice] = (0, 200, 100)
    
    write_text("Car:", width * 0.05, height * 0.05, int(width * 0.04), color_list[0])
    write_text("Track:", width * 0.05, height * 0.1, int(width * 0.04), color_list[1])
    write_text("Zoom:", width * 0.05, height * 0.15, int(width * 0.04), color_list[2])
    write_text("Start", width * 0.05, height * 0.8, int(width * 0.04), color_list[3])
    
    write_text(car_list[settings[0]], width * 0.5, height * 0.05, int(width * 0.04), color_list[0])
    write_text(track_list[settings[1]], width * 0.5, height * 0.1, int(width * 0.04), color_list[1])
    write_text(str(settings[2]), width * 0.5, height * 0.15, int(width * 0.04), color_list[2])
    

def start_screen(event, settings):
    if event != ESC:
        return settings

    #car, track, zoom
    settings = [0 ,0 ,30, True]
    current_choice = 0
    current_track = 0
    current_car = 0
    current_zoom = 0

    while True:
        event = check_event()
        
        if current_choice == 3 and event == ENTER:
            break
        
        current_choice = get_current_choice(current_choice, event)
        settings = update_current_settings(settings, current_choice, car_list, track_list, event)

        win.fill((200, 200, 255))
        display_settings(settings, current_choice, car_list, track_list)
        p.display.update()

    return settings


def restart_game(settings):
    grid = read_grid(direct + "/tracks/" + track_list[settings[1]])
    global visible_screen_length
    global visible_screen_height
    global tile_length
    global original_p_car_surface
    global p_car_surface
    global car_size
    global mini_map_surface
    global track_index

    track_index = settings[1]

    #screen
    visible_screen_length = settings[2]
    visible_screen_height = visible_screen_length * height / float(width)
    tile_length = 5

    #minimap
    if len(grid) > len(grid[1]):
        mini_tile_length = (width / len(grid)) / 2
    else:
        mini_tile_length = (height / len(grid[1])) / 2
    
    mini_map_surface = p.Surface((mini_tile_length * len(grid[1]), mini_tile_length * len(grid)))
    mini_map_surface.fill(green)
    mini_map_surface.set_colorkey(green)
    mini_map_surface.set_alpha(255)
    
    for y in range(len(grid)):
        for x in range(len(grid[1])):
            if grid[y][x] != None:
                p.draw.rect(mini_map_surface, grid[y][x], (x * mini_tile_length, y * mini_tile_length,
                                                mini_tile_length, mini_tile_length))

    #car
    car_size = int(0.6 * (width /visible_screen_length))
    original_p_car_surface = p.image.load(direct + "/cars/" + car_list[settings[0]])
    original_p_car_surface = p.transform.scale(original_p_car_surface, (car_size, car_size))
    p_car_surface = original_p_car_surface
    p_car_pos = place_car(grid)

    #surface, position, prev_position, speed, angle, hit_box, terrain, time_list, check_point, invalid
    p_car = Car(p_car_surface, p_car_pos, p_car_pos, 0.0, 180, None , [grey], [None, 0], True, False)

    return grid, p_car

#--------------------------------------------------------------

def read_grid(path):
    grid = []
    
    with open(path, "r") as open_file:
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


def write_text(txt ,x, y, size, color):
    
    text = p.font.SysFont('timesnewroman', size)
    textsurface = text.render(txt, False, color)
    win.blit(textsurface, (x, y))


def place_car(grid):
    
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == grid_slot_color:
                car_pos = (x * tile_length, y * tile_length)

    return car_pos

#---------------------------Car-class----------------------------------------------

class Car:
    
    def __init__(self, surface, position, prev_position, speed, angle,
                 hit_box, terrain, time_list, check_point, invalid):
        
        self.surface = surface
        self.position = position
        self.prevposition = prev_position
        self.speed = speed
        self.angle = angle
        self.hit_box = hit_box
        self.terrain = terrain
        self.time_list = time_list
        self.check_point = check_point
        self.invalid = invalid


    def update_speed(self, multiplier):
        key_list = p.key.get_pressed()
        throttle = False
        brake = False
        
        if key_list[UP] == 1:
            throttle = True
            
        else:
            engine_sound.stop()

        if key_list[DOWN] == 1:
            brake = True

        self.speed = physics.update_speed(self.speed, throttle, brake, self.terrain, multiplier)


    def update_angle(self):
        key_list = p.key.get_pressed()
        
        if key_list[RIGHT] == 1:
            self.angle += physics.update_angle(self.speed, self.terrain)

        if key_list[LEFT] == 1:
            self.angle -= physics.update_angle(self.speed, self.terrain)


    def rotate_surface(self):
        self.surface = p.transform.rotate(original_p_car_surface, (- self.angle))


    def update_position(self):
        self.prev_position = self.position
        
        x_change = math.cos(math.radians(self.angle)) * self.speed
        y_change = math.sin(math.radians(self.angle)) * self.speed
        
        self.position = (self.position[0] + x_change, self.position[1] + y_change)


    def update_hit_box(self, tile_length):
        size_x = car_size * tile_length / float((width / float(visible_screen_length)))
        size_y = size_x / 2
        #print tile_length / (float(width) / visible_screen_length)

        x_change1 = (math.cos(math.radians(90 - self.angle)) * size_y) / 2
        y_change1 = -(math.sin(math.radians(90 - self.angle)) * size_y) / 2
        x_change2 = (math.cos(math.radians(self.angle)) * size_x) / 2
        y_change2 = (math.sin(math.radians(self.angle)) * size_x) / 2

        self.hit_box = [(self.position[0] + x_change2 - x_change1, self.position[1] + y_change2 - y_change1),
                        (self.position[0] + x_change2 + x_change1, self.position[1] + y_change2 + y_change1),
                        (self.position[0] - x_change2 - x_change1, self.position[1] - y_change2 - y_change1),
                        (self.position[0] - x_change2 + x_change1, self.position[1] - y_change2 + y_change1)]


    def update_terrain(self, grid):
        terrain_list = []
    
        for position in self.hit_box:
            x = (position[0] / tile_length + 1)
            y = (position[1] / tile_length + 1)
            if 0 < x < len(grid[1]) and 0 < y < len(grid):
                terrain_list.append(grid[int(y)][int(x)])

        self.terrain = terrain_list

        if black in terrain_list:
            self.position = self.prev_position
            self.speed *= 0

        if check_point_color in terrain_list:
            self.check_point = True

        if None in self.terrain:
            self.invalid = True


    def update_time(self):

        if self.check_point and finish_line_color in self.terrain:
            self.check_point = False
            
            if self.time_list[0] != None and not self.invalid:
                self.time_list.append(time.time() - self.time_list[0])
                
            self.time_list[0] = time.time()
            self.invalid = False

        self.time_list[1] = time.time()
            
#---------------------------------------------------------------------------------

def check_event():
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            #quit()

        if event.type == p.KEYDOWN:
            if event.key == p.K_q:
                p.quit()
                #quit()
                
            return event.key


def update_screen_pos(p_car):
    x = (p_car.position[0] % tile_length) * (width / visible_screen_length) / tile_length
    y = (p_car.position[1] % tile_length) * (width / visible_screen_length) / tile_length
    
    return (x, y)


def update_grid_range(p_car):
    grid_range = []
    car_square = (int(p_car.position[0] / tile_length), int(p_car.position[1] / tile_length))
    
    grid_range = [car_square[0] - visible_screen_length / 2, car_square[0] + visible_screen_length / 2 + 3,
                  car_square[1] - visible_screen_height / 2, car_square[1] + visible_screen_height / 2 + 3]
    
    return grid_range, car_square

    
def draw_grid(grid, grid_range, screen_pos, car_square):
    grid_length = len(grid[1])
    grid_height = len(grid)
    tile_length = width / visible_screen_length

    off_screen_x = 0
    off_screen_y = 0
    x_counter = 0
    
    if grid_range[0] < 0:
        off_screen_x = - grid_range[0] - 1
        x_counter = off_screen_x

    if grid_range[1] > len(grid):
        off_screen_x = - (grid_range[1] - len(grid))

    if grid_range[2] < 0:
        off_screen_y = - grid_range[2] - 1

    y_counter = off_screen_y

    #print off_screen_y, grid_range[2]
    
    for y in range(grid_height):
        for x in range(grid_length):
            
            if grid_range[0] < x < grid_range[1] and grid_range[2] < y < grid_range[3]:
                if grid[y][x] != None:
                    p.draw.rect(win, grid[y][x], (x_counter * tile_length - screen_pos[0],
                                                  y_counter * tile_length - screen_pos[1],
                                                  tile_length, tile_length))

                    if draw_square_numbers:
                        write_text(str(x) + " "+ str(y), x_counter * tile_length - screen_pos[0],
                                   y_counter * tile_length - screen_pos[1],
                                   int(tile_length * 0.2), (255,255,255))

                x_counter += 1
                if off_screen_x >= 0:
                    if x_counter == visible_screen_length + 2:
                        y_counter += 1
                        x_counter = off_screen_x

                else:
                    if x_counter == visible_screen_length + off_screen_x + 2:
                        y_counter += 1
                        x_counter = 0


def draw_car(car_surface, hit_box, tile_length):
    size = car_surface.get_size()
    win.blit(car_surface, (width / 2 - size[0] / 2, height / 2 - size[1] / 2))

    
    for position in hit_box:
        win.set_at((int(position[0] * (width / visible_screen_length) / tile_length),
                    int(position[1] * (width / visible_screen_length) / tile_length)), (255,0,0))


def draw_mini_map(grid, car_square):

    if len(grid) > len(grid[1]):
        mini_tile_length = (width / len(grid)) / 2
    else:
        mini_tile_length = (height / len(grid[1])) / 2
        
    start_x = width - (mini_tile_length * len(grid[1]))
    
    car_x = (car_square[0] + 1) * mini_tile_length
    car_y = (car_square[1] + 1) * mini_tile_length
    
    win.blit(mini_map_surface, (start_x, 0))
    p.draw.rect(win, (255, 0, 0), (start_x + car_x, car_y, mini_tile_length, mini_tile_length))
    

def display_time(time_list, invalid):
    if time_list[0] == None:
        return

    best_times = read_best_times()
    all_time_best = best_times[track_index]
    current_time = round(time_list[1] - time_list[0], 2)
    best_time = 100000

    for time in time_list[1 : len(time_list)]:
        if time < best_time and not invalid:
            best_time = round(time, 2)

    if best_time == 100000:
        best_time = None

    
    write_text("Current lap: " + str(current_time), width * 0.03, height * 0.03, int(width * 0.02), black)
    write_text("All time best: " + str(all_time_best), width * 0.03, height * 0.09, int(width * 0.02), black)

    if invalid:
        write_text("laptime invalidated", width * 0.03, height * 0.06, int(width * 0.02), black)
        
    else:
        write_text("Session best: " + str(best_time), width * 0.03, height * 0.06, int(width * 0.02), black)

    return best_time


def read_best_times():
    best_times = []
    
    with open("best times.txt", "r") as open_file:
        for time in open_file:
            if time.rstrip() == "None":
                best_times.append(None)
            else:
                best_times.append(float(time.rstrip()))

    return best_times


def save_times(best_times):
    with open("best times.txt", "w") as open_file:
        for time in best_times:
            open_file.write(str(time) + "\n")
            
    
def update_best_times(settings, best_time):
    if settings == None:
        return
    
    best_times = read_best_times()

    if best_times[settings[1]] == None:
        best_times[settings[1]] = best_time
        
    elif best_time < best_times[settings[1]] and best_time != None:
        best_times[settings[1]] = best_time

    save_times(best_times)
    
#------------------------------Main-------------------------------------------------
    
def main():

    settings = start_screen(ESC, None)
    grid, p_car = restart_game(settings)    

    while True:
        
        #settings:
        event = check_event()
        settings = start_screen(event, settings)

        #new game:
        if settings[3]:
            grid, p_car = restart_game(settings)
            settings[3] = False

        #car:
        #p_car.update_speed(150 / float(len(grid)))
        p_car.update_speed(1)
        p_car.update_angle()
        p_car.rotate_surface()
        p_car.update_position()
        p_car.update_hit_box(width / len(grid))
        p_car.update_terrain(grid)
        p_car.update_time()

        #screen:
        screen_pos = update_screen_pos(p_car)
        grid_range, car_square = update_grid_range(p_car)

        #draw:
        win.fill(green)
        draw_grid(grid, grid_range, screen_pos, car_square)
        draw_car(p_car.surface, p_car.hit_box, tile_length)
        draw_mini_map(grid, car_square)
        best_time = display_time(p_car.time_list, p_car.invalid)
        update_best_times(settings, best_time)
        p.display.update()
        
        clock.tick(30)
        
main()










