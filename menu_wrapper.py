import pygame
from screen import Screen
from menu_screen import MenuScreen

class MenuScreenWrapper(Screen):
    def __init__(self, surface):
        super().__init__(surface)
        self.menu = MenuScreen(surface)
    
    def handle_events(self, event):
        return self.menu.handle_events(event)
    
    def update(self, game_data=None):
        mouse = pygame.mouse.get_pos()
        self.menu.update(mouse)
    
    def draw(self):
        self.menu.draw()