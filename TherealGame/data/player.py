import pygame
from data import config
from data.projectile import Projectile

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, config.PLAYER_SIZE, config.PLAYER_SIZE)
        self.hp = config.PLAYER_HP_MAX
        self.xp = 0
        self.invulnerable_timer = 0 
        
        self.direction = "down"
        self.is_moving = False
        
        # Animatie
        self.animation_timer = 0
        self.animation_speed = 10 
        self.animation_frame = 0 

        # Inventory
        self.weapons_owned = ["pistol"] 
        self.current_weapon_index = 0
        self.ammo = {
            "pistol": config.WEAPONS["pistol"]["start_ammo"],
            "shotgun": config.WEAPONS["shotgun"]["start_ammo"]
        }
        self.has_key = False 

        # Cooldowns
        self.shoot_cooldown = 0
        self.switch_cooldown = 0

    def handle_input(self, map_data, projectiles_list, game_instance):
        keys = pygame.key.get_pressed()
        
        dx = 0
        dy = 0
        self.is_moving = False 

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -config.PLAYER_SPEED
            self.direction = "left"
            self.is_moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = config.PLAYER_SPEED
            self.direction = "right"
            self.is_moving = True
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -config.PLAYER_SPEED
            self.direction = "up"
            self.is_moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = config.PLAYER_SPEED
            self.direction = "down"
            self.is_moving = True

        if self.is_moving:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = 1 if self.animation_frame == 0 else 0
        else:
            self.animation_frame = 0 

        self.rect.x += dx
        if self.check_wall_collision(map_data, game_instance.teachers): self.rect.x -= dx
        self.rect.y += dy
        if self.check_wall_collision(map_data, game_instance.teachers): self.rect.y -= dy
            
        if self.switch_cooldown > 0: self.switch_cooldown -= 1
        if keys[pygame.K_g] and self.switch_cooldown == 0:
            self.current_weapon_index += 1
            if self.current_weapon_index >= len(self.weapons_owned):
                self.current_weapon_index = 0
            self.switch_cooldown = 20 

        current_weapon = self.weapons_owned[self.current_weapon_index]
        weapon_stats = config.WEAPONS[current_weapon]
        
        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1
        
        if keys[pygame.K_SPACE] and self.shoot_cooldown == 0:
            if self.ammo[current_weapon] > 0:
                self.ammo[current_weapon] -= 1
                
                if current_weapon == "shotgun":
                    game_instance.add_screen_shake(10)
                else:
                    game_instance.add_screen_shake(2)
                
                offset_y = (config.PLAYER_VISUAL_SIZE - config.PLAYER_SIZE) // 2
                bullet_y = self.rect.centery - offset_y 
                bullet = Projectile(self.rect.centerx, bullet_y, self.direction, current_weapon)
                projectiles_list.append(bullet)
                self.shoot_cooldown = weapon_stats["cooldown"]

    def check_wall_collision(self, map_data, teachers):
        points = [self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright]
        for point in points:
            col = int(point[0] // config.TILE_SIZE)
            row = int(point[1] // config.TILE_SIZE)
            
            if row < 0 or col < 0 or row >= len(map_data) or col >= len(map_data[0]):
                return True
            
            if 0 <= row < len(map_data):
                if 0 <= col < len(map_data[row]):
                    tile = map_data[row][col]
                    if tile in ['W', 'b', 'B', 'L']: return True
        
        for t in teachers:
            if self.rect.colliderect(t.rect.inflate(-10, -10)):
                return True
        return False

    def update(self):
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

    def draw(self, screen, camera_x, camera_y):
        if self.invulnerable_timer > 0 and self.invulnerable_timer % 10 < 5: 
            return # Knipper effect

        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y - camera_y
        
        sprite_key = self.direction 
        if self.is_moving:
            if self.direction in ["up", "down"]:
                foot = "_l" if self.animation_frame == 0 else "_r"
                sprite_key = "walk_" + self.direction + foot
            elif self.animation_frame == 1:
                sprite_key = "walk_" + self.direction
        
        sprite = config.ASSETS["player_sprites"].get(sprite_key, config.ASSETS["player_sprites"]["down"])
        
        offset_x = (config.PLAYER_VISUAL_SIZE - config.PLAYER_SIZE) // 2
        offset_y = config.PLAYER_VISUAL_SIZE - config.PLAYER_SIZE
        screen.blit(sprite, (draw_x - offset_x, draw_y - offset_y))