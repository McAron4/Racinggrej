green = (0,250,0)
grey = (100,100,100)
yellow = (255,250,0)
black = (0,0,0)
grid_slot_color = (170,170,170)
finish_line_color = (255,255,255)
check_point_color = (110,110,110)

acceleration = 0.07
max_speed = 5

#-----------------------Speed-----------------------------------
def green_yellow_speed(speed, throttle, brake, multiplier):
    if throttle:
        speed += 0.05 * multiplier
    else:
        speed *= 0.9
        
    if brake:
        speed *= 0.9 

    if speed < 0.05 * multiplier:
        speed = 0 

    if speed > 0.6 * multiplier:
        speed *= 0.2 * multiplier
    
    return speed


def grey_speed(speed, throttle, brake, multiplier):
    if throttle:
        speed += acceleration * multiplier
    else:
        speed *= 0.97

    if brake:
        speed *= 0.9

    if speed < acceleration * multiplier:
        speed = 0

    if speed > max_speed * multiplier:
        speed = max_speed * multiplier
    
    return speed 


def update_speed(speed, throttle, brake, terrain_list, multiplier):
    if None in terrain_list or yellow in terrain_list:
        speed = green_yellow_speed(speed, throttle, brake, multiplier)

    else:
        speed = grey_speed(speed, throttle, brake, multiplier)
        
    return speed
    
#---------------------------------Angle-------------------------------

def update_angle(speed, terrain_list):
    angle = 7 / (speed * 0.1 + 1)
    #print angle
    return angle

    


































    
    
    
