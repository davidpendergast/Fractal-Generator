from __future__ import division
import pygame

# Customizable variables
screen_size = (800,450)
default_view = [-4, 4, -screen_size[1]/screen_size[0]*4, screen_size[1]/screen_size[0]*4]
custom_view = None
#custom_view = None
iter_limit = 50

# Global vars
view = None
screen = None

def mandlebrot_function(x, y):
    i = 0
    val = 0
    
    c = x + y*1j
    while i < iter_limit:
        if abs(val) > 2:
            return i
        val = val*val + c
        i += 1
        
    return -1
    
def draw_frac(screen,screen_size):
    global view
    x_low = view[0]
    x_high = view[1]
    y_low = view[2]
    y_high = view[3]

    rect = pygame.Rect(0,0,screen_size[0],3)

    for y_idx in range(0, screen_size[1]):
        if handle_events():
            return False
        for x_idx in range(0, screen_size[0]):
            x = (x_idx / screen_size[0])*(x_high - x_low) + x_low
            y = (y_idx / screen_size[1])*(y_high - y_low) + y_low

            val = mandlebrot_function(x, y)
            if  val == -1:
                screen.set_at((x_idx,y_idx), (0, 0, 0))
            else:
                screen.set_at((x_idx, y_idx), (100+ ((val*20) % 156), 100+((val*20) % 156), 255))
            screen.set_at((x_idx,y_idx+1), (255,0,0))
            screen.set_at((x_idx,y_idx+2), (255,0,0))
        pygame.display.update(rect)
        rect.move_ip(0,1)
        
    return True

def handle_events():
    needs_redraw = False
    global iter_limit, view
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_idx = event.pos[0]
            x = (x_idx / screen_size[0])*(view[1] - view[0]) + view[0]
            y_idx = event.pos[1]
            y = (y_idx / screen_size[1])*(view[3] - view[2]) + view[2]
            
            new_width = (view[1]-view[0])/2
            new_height = (view[3]-view[2])/2
            x_low = x - new_width/2
            x_high = x + new_width/2
            y_low = y - new_height/2
            y_high = y + new_height/2
            view = [x_low, x_high, y_low, y_high]
            print "zooming to ("+str(x_low)+", "+str(x_high)+", "+str(y_low)+", "+str(y_high)+")"
            needs_redraw = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: 
                pygame.image.save(screen, "fractal.png")
            if event.key == pygame.K_UP:
                iter_limit = iter_limit * 10
                print "iterations = "+str(iter_limit)
            if event.key == pygame.K_DOWN:
                if iter_limit > 10:
                    iter_limit = iter_limit / 10
                    print "iterations = "+str(iter_limit)
            if event.key == pygame.K_RETURN:
                needs_redraw = True
    return needs_redraw

def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode(screen_size)

    global view
    if custom_view != None:
        view = custom_view
    else:
        view = default_view

    bool = True
    while True:
        if bool:
            while draw_frac(screen,screen_size) == False:
                pass
        bool = handle_events()
            
               
                

    pygame.quit()

main()


    
