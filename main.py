import pygame
import win32api
import win32con
import win32gui
import ctypes
import random
from pet import Pet

# Set up the game
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.NOFRAME)
clock = pygame.time.Clock()
running = True
fuchsia = (255, 0, 128)  # Transparency color
main_pet = Pet(pygame.image.load('assets/leon-0a.gif').convert())
main_pet.position = main_pet.sprite.get_rect()
FPS = 40


# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
ctypes.windll.user32.SetWindowLongW(hwnd, -20, ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x80000)

# Make the entire window transparent
transparency_color = (0, 0, 0)
color_key = (transparency_color[2] << 16) | (transparency_color[1] << 8) | transparency_color[0]
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, color_key, 0, 0x00000001)

transparent_surface = pygame.Surface(screen.get_size())
transparent_surface.fill((0, 0, 0))
screen.blit(main_pet.sprite, main_pet.position)
pygame.display.update()

# Function that picks where a pet is going to move to
def pick_target_location(moving_pet):
    # Get the possible range for where the pet can go without being cut off
    width, height = pygame.display.get_window_size()
    width -= moving_pet.sprite.get_width()
    height -= moving_pet.sprite.get_height()

    return random.randint(0,width), random.randint(0,height)

# Move the pet smoothly the amount specified
def move(moving_pet, x, y):
    if x >= 0 and y >= 0:
        while x > 0 or y > 0:
            screen.blit(transparent_surface,moving_pet.position,moving_pet.position)  # erase pet
            if (x > 0): # move x if still needed
                moving_pet.position = moving_pet.position.move(1,0)
                x -= 1
            if (y > 0): # move y if still needed
                moving_pet.position = moving_pet.position.move(0,1)
                y -= 1
            screen.blit(moving_pet.sprite, moving_pet.position)
            pygame.display.update()  
            clock.tick(FPS)
    elif x <= 0 and y >= 0:
        while x < 0 or y > 0:
            screen.blit(transparent_surface,moving_pet.position,moving_pet.position) # erase pet
            if (x < 0): # move x if still needed
                moving_pet.position = moving_pet.position.move(1,0)
                x += 1
            if (y > 0): # move y if still needed
                moving_pet.position = moving_pet.position.move(0,1)
                y -= 1
            screen.blit(moving_pet.sprite, moving_pet.position)
            pygame.display.update()  
            clock.tick(FPS)
    elif x >= 0 and y <= 0:
        while x > 0 or y < 0:
            screen.blit(transparent_surface,moving_pet.position,moving_pet.position)  # erase pet
            if (x > 0): # move x if still needed
                moving_pet.position = moving_pet.position.move(1,0)
                x -= 1
            if (y < 0): # move y if still needed
                moving_pet.position = moving_pet.position.move(0,1)
                y += 1
            screen.blit(moving_pet.sprite, moving_pet.position)
            pygame.display.update()  
            clock.tick(FPS)
    elif x < 0 and y < 0:
        while x < 0 or y < 0:
            screen.blit(transparent_surface,moving_pet.position,moving_pet.position)  # erase pet
            if (x < 0): # move x if still needed
                moving_pet.position = moving_pet.position.move(1,0)
                x += 1
            if (y < 0): # move y if still needed
                moving_pet.position = moving_pet.position.move(0,1)
                y += 1
            screen.blit(moving_pet.sprite, moving_pet.position)
            pygame.display.update()  
            clock.tick(FPS) 

main_pet.update_next_time(pygame.time.get_ticks())            
while running: # Begin the program loop
    clock.tick(FPS)

    #Keep the pet on the top
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE)

    # TODO: Implement a quit game feature which updates running to false 
    
    # Check for when the pet is ready to change state
    if pygame.time.get_ticks() >= main_pet.next_time:
        if main_pet.state == "ASLEEP":
            # TODO: Play the waking up animation
            pass

        # Choose a new action 
        main_pet.update_state()
        match main_pet.state:
            case 'ASLEEP':
                # TODO: Play the falling asleep animation
                main_pet.update_next_time(pygame.time.get_ticks())
            case 'IDLE':
                main_pet.update_next_time(pygame.time.get_ticks())
            case 'MOVING':
                # Get a location target
                x, y = pick_target_location(main_pet)

                # Calculate the movement needed to get to target
                x -= main_pet.position.x 
                y -= main_pet.position.y

                # move the pet smoothly to the target
                move(main_pet, x, y)
                main_pet.update_state()

pygame.quit()

