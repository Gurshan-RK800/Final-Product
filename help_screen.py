import pygame
from screen import Screen

class HelpScreen(Screen): #displays how to play the game for the player
    def __init__(self, surface):
        super().__init__(surface)
        self.bg = (22, 64, 21)        #sets the fonts and colours
       
        self.title_font = pygame.font.Font("fonts/font.otf", 30)
        self.text_font = pygame.font.Font("fonts/font.otf", 24)
        

        self.title = self.title_font.render("Instructions", True, (255, 255, 255))
        self.title_rect = self.title.get_rect(center=(self.width//2, 100))   #centers the text in the middle
        
        self.help_text = [    # List of instructions for help on how to play + adding any other help
            "Use LEFT/RIGHT or A/D keys to move",
            "Press SPACE to jump",
            "Press F or LEFT CTRL to shoot",
            "Avoid hitting obstacles",
            "Move from left to right to complete the level",
            "Press ESC to return to menu"
        ]
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:   #checks for any keys entered by the user
            if event.key == pygame.K_ESCAPE:
                return "menu"
        return None
    
    def update(self, game_data=None):
        pass
                                    #for the future if a new feature is needed or any updates
    def draw(self):
        self.surface.fill(self.bg)
        
        self.surface.blit(self.title, self.title_rect)
        
        y_pos = 200
        for line in self.help_text:   #loop to space everything evenly
            text = self.text_font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.width//2, y_pos))
            self.surface.blit(text, text_rect)
            y_pos += 50