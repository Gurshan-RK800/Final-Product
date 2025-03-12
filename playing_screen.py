import pygame
from screen import Screen
from player import Player
from enemy import Enemy
from tilemap import TileMap, COIN, EMPTY 
from score import Score  
from sound_manager import SoundManager  

class PlayingScreen(Screen):  # tile map, player, enemies, score and sounds
    def __init__(self, surface):
        super().__init__(surface)
        self.tilemap = TileMap(tile_size=32)
        self.current_level = 1
        self.max_level = 2
        
        self.player_start_x = 100
        self.player_start_y = 300
        self.player = Player(self.player_start_x, self.player_start_y)
        self.player.mapX = self.player_start_x
        
        self.score = Score()
        
        self.sound_manager = SoundManager()
        
        self.enemies = []
        self.settingEnemies()
        
        self.background_image = pygame.image.load("background.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        
        self.sound_manager.bgmusic()
        
        try:
            self.hit_sound = pygame.mixer.Sound("sounds/hit.mp3")
        except:
            print("Warning: hit.mp3 sound file not found")
            self.hit_sound = None
    
    def settingEnemies(self):    #setting up the enemies
        self.enemies = []
        self.enemies.append(Enemy(300, 350, 300, 500))
        self.enemies.append(Enemy(600, 350, 550, 750))
        self.enemies.append(Enemy(900, 350, 850, 1050))
        self.enemies.append(Enemy(1200, 350, 1150, 1350))
        self.enemies.append(Enemy(1600, 350, 1550, 1750))
        self.enemies.append(Enemy(2000, 350, 1950, 2150))
        
    def nextlevel(self):
        #move to the next level if available
        if self.current_level < self.max_level:
            self.current_level += 1
            if self.current_level == 2:
                self.tilemap.create_level2()
            # reseting the players position
            self.player.resetPlayer(self.player_start_x, self.player_start_y)
            # Reset enemies for the new level
            self.settingEnemies()
            return True
        return False
    def islevelcompleted(self):
        #chekcs if the player has reached the end of the level
        # For example, if player reaches far right of map
        if self.player.mapX > (self.tilemap.width * self.tilemap.tile_size) - 100:
            return self.nextlevel()
        return False
    
    def gamerestart(self):   #resetting to the first level
       
        self.current_level = 1
        
        self.tilemap.create_level()
        
        self.player = Player(self.player_start_x, self.player_start_y)
        self.player.mapX = self.player_start_x
        
        self.settingEnemies()
        
        self.score.resetinglives()
    
    def handle_events(self, event):   #player inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                
                return "menu"
            elif event.key == pygame.K_SPACE:
                self.player.playerJump()
            elif event.key == pygame.K_f or event.key == pygame.K_LCTRL:  
                self.player.shoot()
                self.sound_manager.soundplaying("fire")
            elif event.key == pygame.K_r:
                self.gamerestart()
                self.sound_manager.bgmusic()
        elif event.type == pygame.QUIT:
            return "exit"
        
        return None
    
    def coinCollect(self):  #player position if near any coins
        player_rect = self.player.playerRect()
        
        tile_x1 = max(0, int(player_rect.left / self.tilemap.tile_size))
        tile_x2 = min(self.tilemap.width - 1, int(player_rect.right / self.tilemap.tile_size))
        tile_y1 = max(0, int(player_rect.top / self.tilemap.tile_size))
        tile_y2 = min(self.tilemap.height - 1, int(player_rect.bottom / self.tilemap.tile_size))
        
        for y in range(tile_y1, tile_y2 + 1):
            for x in range(tile_x1, tile_x2 + 1):
                if self.tilemap.tiles[y][x] == COIN:
                    coin_world_x = x * self.tilemap.tile_size
                    coin_screen_x = coin_world_x - self.tilemap.get_scroll_x()
                    coin_screen_y = y * self.tilemap.tile_size
                    
                    self.score.updatingcoins(coin_screen_x, coin_screen_y)
                    
                    self.sound_manager.soundplaying("coin")
                    
                    self.tilemap.clear_tile(x, y)
    
    def bulletcollision(self): # bullet hitting enemy or tile
        for enemy in self.enemies[:]:
            enemy_rect = enemy.get_rect()
            for bullet in self.player.bullets[:]:
                bullet_rect = pygame.Rect(bullet.world_x, bullet.y, bullet.width, bullet.height)
                if bullet_rect.colliderect(enemy_rect):
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    break
        
        player_rect = self.player.playerRect()
        for enemy in self.enemies:
            for bullet in enemy.bullets[:]:
                bullet_rect = pygame.Rect(bullet.world_x, bullet.y, bullet.width, bullet.height)
                if bullet_rect.colliderect(player_rect):
                    bullet.active = False
                    self.P_handle()
    
    def enemyCollision(self):  #player running into an enemy
        player_rect = self.player.playerRect()
        for enemy in self.enemies:
            if player_rect.colliderect(enemy.get_rect()):
                self.P_handle()
                break
    
    def P_handle(self): # player lives
        if not self.score.lifelost():
            self.GameOver()
        else:
            self.resetplayer()
    
    def resetplayer(self):
        self.player.resetPlayer(self.player_start_x, self.player_start_y)
    
    def GameOver(self):  #plays the game over sound + restarting if no lives
        self.sound_manager.soundplaying("game_over")
        self.gamerestart()
        self.sound_manager.bgmusic()
    
    def update(self, game_data=None):  #movement actions, animations + level completion
        keys_pressed = pygame.key.get_pressed()
        
        self.player.playermov(keys_pressed, self.tilemap)
        self.player.update_ani()
        
        self.player.updateblt(self.tilemap)
        self.islevelcompleted()
        
        self.coinCollect()
        
        for enemy in self.enemies:
            enemy.update(self.tilemap, self.player)
        
        self.enemyCollision()
        self.bulletcollision()
        
        if self.player.y > self.height:
            self.P_handle()
    
    def draw(self): # draws background, tiles, enemies, player onto screen
        self.surface.blit(self.background_image, (0, 0))
        
        self.tilemap.draw(self.surface, self.player.mapX, self.width)
        
        for enemy in self.enemies:
            enemy.draw(self.surface)
        
        self.player.draw(self.surface)
        
        self.score.score_lifedrawn(self.surface)