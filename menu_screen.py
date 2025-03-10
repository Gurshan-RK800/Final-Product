import pygame


class Button:  #clickable buttons in the Dusk Dasher UI
    def __init__(self, x, y, width, height, text, action, color=(88, 101, 242), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action  
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font("fonts/font.otf", 24)
        self.font.get_italic()
        self.shadow_offset = 3
        self.border_radius = 12


    def draw(self, surface):
       #draws the buttons onto a given surface
        pygame.draw.rect(surface, self.color, self.rect, border_radius=self.border_radius)
        

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center) #makes a rectangle that holds the text
        surface.blit(text_surf, text_rect)  # draws the text onto the surface and centres it in the button
    

    def handle_event(self, event): #handles user inputs like clicking
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
            print(f"Button clicked: {self.text}")
            return self.action
        return None


class MenuScreen:   #represents menu screen, backgrounds, buttons and text
    def __init__(self, surface):
        self.surface = surface
        self.width, self.height = surface.get_size()  # gets dimensions
        self.buttons = []
        
        
        self.background = pygame.image.load("background.png").convert()  #loads background iamge
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        
        #buttons + dimensions + spacing
        btn_w = 220
        btn_h = 60
        spacing = 25
        start_y = (self.height - (3 * btn_h + 2 * spacing)) // 2
        center_x = (self.width - btn_w) // 2
        
        #each button with their text, action and color
        button_info = [
            ("Play", "playing", (76, 175, 80)),
            ("Help", "help", (33, 150, 243)),
            ("Exit", "exit", (239, 83, 80))
        ]
        #loops through button info list
        for i, (text, action, color) in enumerate(button_info):
            btn_y = start_y + i * (btn_h + spacing)
            button = Button(center_x, btn_y, btn_w, btn_h, text, action, color)
            self.buttons.append(button)
        
       
        
       #using italic fonts to make the text look appealing
        self.title_font = pygame.font.Font("fonts/font.otf", 50)
        self.title_font.get_italic()
        self.title = self.title_font.render("Dusk Dashers", True, (255, 255, 255))
        self.title_rect = self.title.get_rect(center=(self.width // 2, start_y - 100))
        
       
        self.subtitle_font = pygame.font.SysFont("Segoe UI Light", 24)
        self.subtitle = self.subtitle_font.render("An Amazing Adventure", True, (200, 200, 200))
        self.subtitle_rect = self.subtitle.get_rect(center=(self.width // 2, start_y - 50))

   # buttons event handler
    def handle_events(self, event):
        for btn in self.buttons:    #loops through the buttons
            action = btn.handle_event(event)
            if action:
                return action
        return None
    
    def update(self, mouse_pos):  # For future updates integrate them here
       
        pass
       #draw to render the menu screen
    def draw(self):
        self.surface.blit(self.background, (0, 0))  #blits background onto top left.
        
       # creates a rectangle for the shadow text, positions it slightly offset for a shadow effect.
        shadow_surf = self.title_font.render("Dusk Dashers", True, (20, 20, 40))
        shadow_rect = shadow_surf.get_rect(center=(self.title_rect.center[0] + 3, self.title_rect.center[1] + 3))
        self.surface.blit(shadow_surf, shadow_rect)
        
       
        self.surface.blit(self.title, self.title_rect)
        self.surface.blit(self.subtitle, self.subtitle_rect)
        
        
        for btn in self.buttons:
            btn.draw(self.surface)