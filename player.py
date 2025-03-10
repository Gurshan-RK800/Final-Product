import pygame
import os
from bullet import Bullet

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.xspeed = 0
        self.yspeed = 0
        self.speed = 5
        self.direction = "right"
        
        self.gravity = 0.5
        self.jmpHight = -12
        self.isground = False
        self.mapX = x
        self.hasJumped = False
        self.jmpBuff = 0
        self.jmpMax = 10
        
        self.totalJmp = 2
        self.currentJmps = 0
        
        self.shoot_cooldown = 0
        self.shoot_cooldown_time = 20
        self.bullets = []
        
        self.t_anim = 0
        self.anim_Speed = 10
        self.activePNG = 0
        
        self.init_sounds()
        
        self.Lframes = []
        self.Rframes = []
        
        self.scale_factor = 1.5
        
        for i in range(1, 5):
            img = pygame.image.load(os.path.join("player", f"left{i}.png"))
            img = pygame.transform.scale(img, 
                                        (int(img.get_width() * self.scale_factor), 
                                         int(img.get_height() * self.scale_factor)))
            self.Lframes.append(img)
            
        for i in range(1, 5):
            img = pygame.image.load(os.path.join("player", f"right{i}.png"))
            img = pygame.transform.scale(img, 
                                        (int(img.get_width() * self.scale_factor), 
                                         int(img.get_height() * self.scale_factor)))
            self.Rframes.append(img)
            
        if self.Rframes:
            self.width = self.Rframes[0].get_width()
            self.height = self.Rframes[0].get_height()
        
        self.is_hit = False
    
    def init_sounds(self):
        try:
            self.fire_sound = pygame.mixer.Sound("sounds/fire.wav")
            self.jump_sound = pygame.mixer.Sound("sounds/jump.wav")
        except:
            print("Warning: Player sound files not found.")
            self.fire_sound = None
            self.jump_sound = None
    
    def playermov(self, keys_pressed, tilemap):
        self.xspeed = 0
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.xspeed = -self.speed
            self.direction = "left"
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.xspeed = self.speed
            self.direction = "right"
        
        if keys_pressed[pygame.K_SPACE]:
            if not self.hasJumped:
                self.jmpBuff = self.jmpMax
            self.hasJumped = True
        else:
            self.hasJumped = False
        
        if self.jmpBuff > 0:
            self.jmpBuff -= 1
            if self.currentJmps < self.totalJmp:
                self.yspeed = self.jmpHight
                self.currentJmps += 1
                self.jmpBuff = 0
                if self.jump_sound:
                    pygame.mixer.Sound.play(self.jump_sound)
        
        self.yspeed += self.gravity
        
        next_x = self.mapX + self.xspeed
        player_rect = pygame.Rect(next_x, self.y, self.width, self.height)
        collision, tile_rect = tilemap.check_collision(player_rect)
        
        if collision:
            if self.xspeed > 0:
                self.mapX = tile_rect.left - self.width
            elif self.xspeed < 0:
                self.mapX = tile_rect.right
            self.xspeed = 0
        else:
            self.mapX = next_x
        
        old_on_ground = self.isground
        self.isground = False
        
        next_y = self.y + self.yspeed
        player_rect = pygame.Rect(self.mapX, next_y, self.width, self.height)
        collision, tile_rect = tilemap.check_collision(player_rect)
        
        if collision:
            if self.yspeed > 0:
                self.y = tile_rect.top - self.height
                self.isground = True
                self.currentJmps = 0
            elif self.yspeed < 0:
                self.y = tile_rect.bottom
            self.yspeed = 0
        else:
            self.y = next_y
        
        self.x = self.mapX - tilemap.get_scroll_x()
    
    def playerJump(self):
        if self.currentJmps < self.totalJmp:
            self.jmpBuff = self.jmpMax
    
    def shoot(self):
        if self.shoot_cooldown == 0:
            bullet_x = self.x + (self.width - 10 if self.direction == "right" else 0)
            bullet_y = self.y + self.height // 2 - 5
            bullet_world_x = self.mapX + (self.width - 10 if self.direction == "right" else 0)
            
            self.bullets.append(Bullet(bullet_x, bullet_y, self.direction, bullet_world_x))
            
            if self.fire_sound:
                pygame.mixer.Sound.play(self.fire_sound)
            
            self.shoot_cooldown = self.shoot_cooldown_time
    
    def updateblt(self, tilemap):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        for bullet in self.bullets[:]:
            bullet.update(tilemap)
            if not bullet.active:
                self.bullets.remove(bullet)
    
    def update_ani(self):
        if self.xspeed != 0:
            self.t_anim += 1
            if self.t_anim >= self.anim_Speed:
                self.t_anim = 0
                self.activePNG = (self.activePNG + 1) % 4
    
    def hashit(self):
        self.is_hit = True
    
    def draw(self, surface):
        frames = self.Lframes if self.direction == "left" else self.Rframes
        
        if frames:
            surface.blit(frames[self.activePNG], (self.x, self.y))
        
        for bullet in self.bullets:
            bullet.draw(surface)
    
    def playerRect(self):
        return pygame.Rect(self.mapX, self.y, self.width, self.height)
    
    def resetPlayer(self, x, y):
        self.mapX = x
        self.y = y
        self.xspeed = 0
        self.yspeed = 0
        self.currentJmps = 0