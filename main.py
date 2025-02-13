import pygame
from pet import pet
import win32api
import win32con
import win32gui

#set up the game
pygame.init()
DISPLAY = pygame.display.set_mode((0,0), pygame.NOFRAME)
clock = pygame.time.Clock()
running = True

