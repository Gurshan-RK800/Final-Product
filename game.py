import pygame
import sys
from menu_wrapper import MenuScreenWrapper
from playing_screen import PlayingScreen     # Imports from other files to be used
from help_screen import HelpScreen

class Game:     # handles the main game window + the state
    def __init__(self, title="Dusk Dashers", width=800, height=600, bg_color=(0, 0, 0)):
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.background = bg_color
        self.clock = pygame.time.Clock()     # control the frame frate
        self.running = True         # keeps track if the game is running
        
        self.MENU = "menu"
        self.GAME = "playing"        # defines the game states here
        self.HELP = "help"

        self.current = self.MENU
        
        self.game_screens = {
            self.MENU: MenuScreenWrapper(self.window),      # game player screen
            self.GAME: PlayingScreen(self.window),       # main meny screen
            self.HELP: HelpScreen(self.window)       #instructions here
        }
        
    def handle_input(self):
         #essentiallt the basic game loop
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:  #Pressing 'x' would close the game
                self.running = False
                return
            
           
            next_screen = self.game_screens[self.current].handle_events(event)

           # Ensures the game only transitions to actually valid screens.
           
            if next_screen:
                if next_screen in self.game_screens:
                   
                    self.current = next_screen
                elif next_screen == "exit":
                    print("Thanks for playing!")  # if returned screen is 'exit' adds a message
                    self.running = False
            
    def update(self):
        self.game_screens[self.current].update()   # only current game state is updated
    
    def gamedrawing(self):
        self.game_screens[self.current].draw()
        pygame.display.flip()      #draw method to the ONLY active screen
        
    def run_game(self):  # essentially just runs the gmae loop
        while self.running:
            self.handle_input()
            self.update()
            self.gamedrawing()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":   # basically just makes sure only code in this file is being executed
    my_game = Game(title="Dusk Dashers", bg_color=(30, 40, 80))
    print("Game starting - press ESC to return to menu!")
    my_game.run_game()