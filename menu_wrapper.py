import pygame
from screen import Screen
from menu_screen import MenuScreen  # to maintain compatibility with game screen

class MenuScreenWrapper(Screen):
    def __init__(self, surface):   # uses the parent class
        super().__init__(surface)
        self.menu = MenuScreen(surface)
    
    def handle_events(self, event):
        return self.menu.handle_events(event)    #event handler
    
    def update(self, game_data=None):
        mouse = pygame.mouse.get_pos()    #gets the mouse position and passes it
        self.menu.update(mouse)
    
    def draw(self):
        self.menu.draw()   #calls the draw method