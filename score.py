import pygame

class Score:
    def __init__(self):
        self.value = 0
        self.lives = 3  
        self.coin_value = 10  
        
        
        self.font = pygame.font.Font("fonts/font.otf", 24)
        self.color = (255, 255, 0)  
        self.lives_color = (255, 0, 0)  
        self.position = (20, 20)  
        self.lives_position = (20, 50)  
    
    def updatingcoins(self, coin_x=None, coin_y=None):
       
        self.value += self.coin_value
    
    def score_lifedrawn(self, surface):
       
       
        score_text = f"SCORE: {self.value}"
        score_surface = self.font.render(score_text, True, self.color)
        surface.blit(score_surface, self.position)
        
        
        lives_text = f"LIVES: {self.lives}"
        lives_surface = self.font.render(lives_text, True, self.lives_color)
        surface.blit(lives_surface, self.lives_position)
    
    def lifelost(self):
       
        self.lives -= 1
        return self.lives > 0
    
    def resetinglives(self):
        
        self.value = 0
        self.lives = 3  