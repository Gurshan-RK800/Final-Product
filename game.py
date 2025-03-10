import pygame
import sys
from menu_wrapper import MenuScreenWrapper
from playing_screen import PlayingScreen
from help_screen import HelpScreen

class Game:
    def __init__(self, title="Dusk Dashers", width=800, height=600, bg_color=(0, 0, 0)):
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.background = bg_color
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.MENU = "menu"
        self.GAME = "playing" 
        self.HELP = "help"
        
        self.current = self.MENU
        
        self.game_screens = {
            self.MENU: MenuScreenWrapper(self.window),
            self.GAME: PlayingScreen(self.window),
            self.HELP: HelpScreen(self.window)
        }
        
    def handle_input(self):
      
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.running = False
                return
            
           
            next_screen = self.game_screens[self.current].handle_events(event)
            
           
            if next_screen:
                if next_screen in self.game_screens:
                   
                    self.current = next_screen
                elif next_screen == "exit":
                    print("Thanks for playing!")
                    self.running = False
            
    def update(self):
        self.game_screens[self.current].update()
    
    def gamedrawing(self):
        self.game_screens[self.current].draw()
        pygame.display.flip()
        
    def run_game(self):
        while self.running:
            self.handle_input()
            self.update()
            self.gamedrawing()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    my_game = Game(title="Dusk Dashers", bg_color=(30, 40, 80))
    print("Game starting - press ESC to return to menu!")
    my_game.run_game()