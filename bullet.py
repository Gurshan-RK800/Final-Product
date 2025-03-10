import pygame


class Bullet:    #the characteristics of the bullet, speed, direction and the x,y variables
    def __init__(self, x, y, direction, world_x):
        self.world_x = world_x
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 10
        self.active = True

        self.image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(self.image, (10, 5))
        self.width = self.image.get_width()
        self.height = self.image.get_height() + 2

        if direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, tilemap):
        #updates the bullet position in accordance to the map


        if self.direction == "right":
            self.world_x += self.speed
        else:
            self.world_x -= self.speed

        self.x = self.world_x - tilemap.get_scroll_x()             #how it goes accordance to the scrolling

        bullet_rect = pygame.Rect(self.world_x, self.y, self.width, self.height)
        collision, _ = tilemap.check_collision(bullet_rect)

        if collision:
            self.active = False           #collision detection

        if self.x < -self.width or self.x > 800 + self.width:
            self.active = False

    def draw(self, surface):
        #shows the bullet onto the screen for the player to see
        surface.blit(self.image, (self.x, self.y))
