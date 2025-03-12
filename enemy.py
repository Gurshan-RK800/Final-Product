import pygame
import os
from bullet import Bullet   # for consistency
import random

class Enemy:
    def __init__(self, x, y, patrol_start_x, patrol_end_x, tilemap=None):
        self.x = x
        self.y = y
        self.world_x = x
        self.width = 64
        self.height = 64
        self.velocity_x = 2
        self.direction = "right"
        self.tilemap = tilemap
        self.patrol_start_x = patrol_start_x
        self.patrol_end_x = patrol_end_x
        self.animation_count = 0
        self.animation_speed = 8
        self.current_frame = 0

        self.left_frames = []
        self.right_frames = []

        for i in range(1, 9):
            img = pygame.image.load(f"enemy/left ({i}).png")
            img_width = int(img.get_width() * 0.1)
            img_height = int(img.get_height() * 0.1)
            img = pygame.transform.scale(img, (img_width, img_height))
            self.left_frames.append(img)

            img = pygame.image.load(f"enemy/right ({i}).png")
            img_width = int(img.get_width() * 0.1)
            img_height = int(img.get_height() * 0.1)
            img = pygame.transform.scale(img, (img_width, img_height))
            self.right_frames.append(img)


            self.width = self.right_frames[0].get_width()
            self.height = self.right_frames[0].get_height()

        self.shoot_cooldown = 30
        self.shoot_cooldown_time = 60
        self.bullets = []
        self.shoot_range = 1000

    def update(self, tilemap, player=None):

        self.tilemap = tilemap


        next_x = self.world_x
        if self.direction == "right":
            next_x += self.velocity_x
            if next_x >= self.patrol_end_x:
                self.direction = "left"
                next_x = self.patrol_end_x
        else:
            next_x -= self.velocity_x
            if next_x <= self.patrol_start_x:
                self.direction = "right"
                next_x = self.patrol_start_x


        if self.tilemap:

            feet_x = next_x + self.width // 2  # Center of enemy at next position
            ground_y = (self.tilemap.height - 1) * self.tilemap.tile_size


            tile_x = int(feet_x / self.tilemap.tile_size)
            tile_y = int(ground_y / self.tilemap.tile_size)


            valid_move = True
            if tile_y < self.tilemap.height and tile_x < self.tilemap.width and tile_x >= 0:

                if self.tilemap.tiles[tile_y][tile_x] == 0:
                    valid_move = False

                    if self.direction == "right":
                        self.direction = "left"
                    else:
                        self.direction = "right"


            if valid_move:
                self.world_x = next_x

        else:

            self.world_x = next_x

        self.animation_count += 1
        if self.animation_count >= self.animation_speed:
            self.animation_count = 0
            self.current_frame = (self.current_frame + 1) % 8

        self.x = self.world_x - tilemap.get_scroll_x()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.shoot_cooldown == 0:
            self.enemyshooting()
            self.shoot_cooldown = self.shoot_cooldown_time

        for bullet in self.bullets[:]:
            bullet.update(tilemap)
            if not bullet.active:
                self.bullets.remove(bullet)

    def enemyshooting(self):
        if self.tilemap:
            ground_y = (self.tilemap.height - 1) * self.tilemap.tile_size
            bullet_y = ground_y - self.height // 2 - 5
        else:
            bullet_y = self.y + self.height // 2 - 5

        bullet_x_offset = self.width if self.direction == "right" else 0
        new_bullet = Bullet(self.x + bullet_x_offset, bullet_y, self.direction, self.world_x + bullet_x_offset)
        self.bullets.append(new_bullet)

    def draw(self, surface):
        if self.x + self.width >= 0 and self.x <= 800:
            frames = self.left_frames if self.direction == "left" else self.right_frames

            if frames:
                if self.tilemap:
                    ground_y = (self.tilemap.height - 1) * self.tilemap.tile_size
                    draw_y = ground_y - self.height
                else:
                    draw_y = self.y
                surface.blit(frames[self.current_frame], (self.x, draw_y))

        for bullet in self.bullets:
            bullet.draw(surface)

    def get_rect(self):
        if self.tilemap:
            ground_y = (self.tilemap.height - 1) * self.tilemap.tile_size
            collision_y = ground_y - self.height
            return pygame.Rect(self.world_x, collision_y, self.width, self.height)
        return pygame.Rect(self.world_x, self.y, self.width, self.height)

    def get_bullets(self):
        return self.bullets