import pygame
import random
import json
import os
import config
import UCLL_maps as maps
from enemy import Enemy
from projectile import Projectile
from npc import Teacher
from item import Item
from particle import Particle

class Game:
    def __init__(self, screen, load_saved=False, difficulty="NORMAL"):
        self.screen = screen
        self.tile_size = config.TILE_SIZE
        
        # HITBOX IS KLEIN (60px) ZODAT JE DOOR DEUREN PAST
        self.player_rect = pygame.Rect(0, 0, config.PLAYER_SIZE, config.PLAYER_SIZE)
        self.player_hp = config.PLAYER_HP_MAX
        self.player_invulnerable_timer = 0 
        
        self.player_direction = "down"
        
        # XP SYSTEM (Nog steeds handig voor score of damage scaling als je dat wilt)
        self.player_xp = 0
        
        # DIFFICULTY
        self.difficulty = difficulty
        settings = config.DIFFICULTY_SETTINGS.get(difficulty, config.DIFFICULTY_SETTINGS["NORMAL"])
        self.zombie_spawn_rate = settings["spawn_rate"] 
        self.darkness_enabled = settings["darkness"]    
        
        # ANIMATIE
        self.is_moving = False
        self.animation_timer = 0
        self.animation_speed = 10 
        self.animation_frame = 0 
        
        # SCREEN SHAKE
        self.screen_shake = 0 
        
        # INVENTORY
        self.weapons_owned = ["pistol"] 
        self.current_weapon_index = 0
        self.ammo = {
            "pistol": config.WEAPONS["pistol"]["start_ammo"],
            "shotgun": config.WEAPONS["shotgun"]["start_ammo"]
        }
        self.has_key = False 

        self.shoot_cooldown = 0
        self.switch_cooldown = 0
        
        self.projectiles = []
        self.enemies = []
        self.teachers = []
        self.items = [] 
        self.particles = [] 
        
        self.zombie_spawn_timer = self.zombie_spawn_rate

        self.cleared_rooms = [] 
        self.current_room_id = None 
        self.saved_position = None  
        self.saved_map_name = "ground"

        self.state = "PLAYING" 
        self.cutscene_timer = 0
        self.active_teacher = None
        self.popup_message = None 
        self.popup_timer = 0

        # LIGHTING
        self.night_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.ambient_light = (10, 10, 20) 
        self.flashlight_radius = 250      

        # SAVE/LOAD
        if load_saved and os.path.exists(config.SAVE_FILE):
            self.load_game()
        else:
            self.load_map("ground") 
            self.player_rect.x = 4 * self.tile_size
            self.player_rect.y = 25 * self.tile_size

    def add_screen_shake(self, amount):
        self.screen_shake = max(self.screen_shake, amount)

    def save_game(self):
        data = {
            "difficulty": self.difficulty,
            "player_hp": self.player_hp,
            "player_xp": self.player_xp,
            "player_x": self.player_rect.x,
            "player_y": self.player_rect.y,
            "current_map_name": self.current_map_name,
            "weapons_owned": self.weapons_owned,
            "current_weapon_index": self.current_weapon_index,
            "ammo": self.ammo,
            "has_key": self.has_key,
            "cleared_rooms": self.cleared_rooms,
            "saved_position": self.saved_position,
            "saved_map_name": self.saved_map_name,
            "current_room_id": self.current_room_id
        }
        try:
            with open(config.SAVE_FILE, 'w') as f:
                json.dump(data, f)
            print("[INFO] Spel automatisch opgeslagen.")
        except Exception as e:
            print(f"[FOUT] Kon spel niet opslaan: {e}")

    def load_game(self):
        try:
            with open(config.SAVE_FILE, 'r') as f:
                data = json.load(f)
            
            self.difficulty = data.get("difficulty", self.difficulty)
            settings = config.DIFFICULTY_SETTINGS.get(self.difficulty, config.DIFFICULTY_SETTINGS["NORMAL"])
            self.zombie_spawn_rate = settings["spawn_rate"]
            self.darkness_enabled = settings["darkness"]

            self.player_hp = data.get("player_hp", 100)
            self.player_xp = data.get("player_xp", 0)
            
            self.current_map_name = data.get("current_map_name", "ground")
            self.weapons_owned = data.get("weapons_owned", ["pistol"])
            self.current_weapon_index = data.get("current_weapon_index", 0)
            self.ammo = data.get("ammo", {"pistol": 20, "shotgun": 0})
            self.has_key = data.get("has_key", False)
            self.cleared_rooms = data.get("cleared_rooms", [])
            self.saved_position = data.get("saved_position", None)
            self.saved_map_name = data.get("saved_map_name", "ground")
            self.current_room_id = data.get("current_room_id", None)
            
            self.load_map(self.current_map_name)
            self.player_rect.x = data.get("player_x", 4 * config.TILE_SIZE)
            self.player_rect.y = data.get("player_y", 25 * config.TILE_SIZE)
            
            print("[INFO] Spel geladen!")
        except Exception as e:
            print(f"[FOUT] Kon savefile niet laden: {e}")
            self.load_map("ground") 

    def load_map(self, map_name):
        self.current_map_name = map_name
        self.map_data_original = maps.ALL_MAPS[map_name]
        
        self.map_data = []
        self.enemies = []
        self.teachers = []
        self.items = []
        self.particles = []
        
        max_width = 0
        for row_idx, row_string in enumerate(self.map_data_original):
            if len(row_string) > max_width: max_width = len(row_string)
            
            new_row = ""
            for col_idx, char in enumerate(row_string):
                if char == 'Z':
                    self.enemies.append(Enemy(col_idx * self.tile_size, row_idx * self.tile_size, self.map_data_original))
                    new_row += "."
                elif char == 'T':
                    if self.current_room_id in self.cleared_rooms: pass 
                    else: self.teachers.append(Teacher(col_idx * self.tile_size, row_idx * self.tile_size))
                    new_row += "." 
                elif char == 'b':
                    new_row += "b"
                elif char == 'B':
                    new_row += "B"
                elif char == 'H':
                    self.items.append(Item(col_idx * self.tile_size, row_idx * self.tile_size, "health"))
                    new_row += "."
                elif char == 'A':
                    self.items.append(Item(col_idx * self.tile_size, row_idx * self.tile_size, "ammo"))
                    new_row += "."
                elif char == 'S':
                    self.items.append(Item(col_idx * self.tile_size, row_idx * self.tile_size, "shotgun"))
                    new_row += "."
                elif char == 'K': 
                    if not self.has_key:
                        self.items.append(Item(col_idx * self.tile_size, row_idx * self.tile_size, "key"))
                    new_row += "."
                else:
                    new_row += char
            self.map_data.append(new_row)

        self.map_pixel_width = max_width * self.tile_size
        self.map_pixel_height = len(self.map_data) * self.tile_size

    def find_spawn_point(self, target_char):
        for row_idx, row in enumerate(self.map_data):
            for col_idx, char in enumerate(row):
                if char == target_char:
                    return (col_idx - 1) * self.tile_size, row_idx * self.tile_size
        return 2 * self.tile_size, 2 * self.tile_size

    def reset_game(self):
        self.player_hp = config.PLAYER_HP_MAX
        self.player_xp = 0 
        self.cleared_rooms = []
        self.current_room_id = None
        self.has_key = False 
        
        self.weapons_owned = ["pistol"]
        self.current_weapon_index = 0
        self.ammo["pistol"] = config.WEAPONS["pistol"]["start_ammo"]
        self.ammo["shotgun"] = config.WEAPONS["shotgun"]["start_ammo"]
        
        self.load_map("ground")
        self.player_rect.x = 4 * self.tile_size
        self.player_rect.y = 25 * self.tile_size
        self.state = "PLAYING"
        self.save_game()

    def spawn_random_zombie(self):
        if self.current_map_name not in ["ground", "first"]:
            return

        attempts = 0
        while attempts < 10:
            r_row = random.randint(0, len(self.map_data) - 1)
            r_col = random.randint(0, len(self.map_data[0]) - 1)
            
            if self.map_data[r_row][r_col] == '.':
                spawn_x = r_col * self.tile_size
                spawn_y = r_row * self.tile_size
                dist = ((spawn_x - self.player_rect.x)**2 + (spawn_y - self.player_rect.y)**2)**0.5
                
                if dist > 400: 
                    self.enemies.append(Enemy(spawn_x, spawn_y, self.map_data_original))
                    break
            attempts += 1

    def handle_input(self):
        keys = pygame.key.get_pressed()
        mouse_clicked = pygame.mouse.get_pressed()[0] 

        if keys[pygame.K_ESCAPE]:
            self.state = "PAUSED"
            return
        if self.state == "PAUSED":
            if keys[pygame.K_r]: self.state = "PLAYING" 
            if keys[pygame.K_q]: 
                self.save_game()
                pygame.quit(); exit()
            return
        if self.state == "GAMEOVER":
            if keys[pygame.K_r]: self.reset_game()
            if keys[pygame.K_q]: self.state = "MENU"; pygame.quit(); exit() 
            return
        
        if self.state == "CUTSCENE": 
            if self.cutscene_timer > 30:
                if keys[pygame.K_SPACE] or mouse_clicked:
                    self.end_cutscene_start_boss()
            return

        dx = 0
        dy = 0
        self.is_moving = False 

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -config.PLAYER_SPEED
            self.player_direction = "left"
            self.is_moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = config.PLAYER_SPEED
            self.player_direction = "right"
            self.is_moving = True
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -config.PLAYER_SPEED
            self.player_direction = "up"
            self.is_moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = config.PLAYER_SPEED
            self.player_direction = "down"
            self.is_moving = True

        if self.is_moving:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = 1 if self.animation_frame == 0 else 0
        else:
            self.animation_frame = 0 

        self.player_rect.x += dx
        if self.check_wall_collision(): self.player_rect.x -= dx
        self.player_rect.y += dy
        if self.check_wall_collision(): self.player_rect.y -= dy
            
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
                    self.add_screen_shake(10)
                else:
                    self.add_screen_shake(2)
                
                offset_y = (config.PLAYER_VISUAL_SIZE - config.PLAYER_SIZE) // 2
                bullet_y = self.player_rect.centery - offset_y 
                bullet = Projectile(self.player_rect.centerx, bullet_y, self.player_direction, current_weapon)
                self.projectiles.append(bullet)
                self.shoot_cooldown = weapon_stats["cooldown"]

        # ---- INTERACTIE MET TEACHER (E) ----
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            for teacher in self.teachers:
                if not teacher.defeated and teacher.is_player_near(self.player_rect):
                    self.start_cutscene(teacher)
                    break 

        for item in self.items[:]:
            if self.player_rect.colliderect(item.rect):
                if item.item_type == "health":
                    self.player_hp = min(config.PLAYER_HP_MAX, self.player_hp + config.HEALTH_REGEN)
                    self.items.remove(item)
                elif item.item_type == "ammo":
                    self.ammo["pistol"] += config.AMMO_PACK_AMOUNT
                    if "shotgun" in self.weapons_owned:
                         self.ammo["shotgun"] += 2
                    self.items.remove(item)
                elif item.item_type == "shotgun":
                    if "shotgun" not in self.weapons_owned:
                        self.weapons_owned.append("shotgun")
                    self.ammo["shotgun"] += config.SHOTGUN_AMMO_AMOUNT
                    self.items.remove(item)
                elif item.item_type == "key": 
                    self.has_key = True
                    self.show_popup_message("SLEUTEL GEVONDEN!")
                    self.save_game()
                    self.items.remove(item)

        self.check_events()
        
        self.zombie_spawn_timer -= 1
        if self.zombie_spawn_timer <= 0:
            self.spawn_random_zombie()
            self.zombie_spawn_timer = self.zombie_spawn_rate

        if self.player_invulnerable_timer > 0:
            self.player_invulnerable_timer -= 1
            
        if self.popup_timer > 0:
            self.popup_timer -= 1

        for e in self.enemies: e.update(self.player_rect)
        for p in self.projectiles: p.update()
        
        for p in self.particles[:]:
            p.update()
            if p.lifetime <= 0:
                self.particles.remove(p)

        self.handle_combat()

    def show_popup_message(self, msg):
        self.popup_message = msg
        self.popup_timer = 120 

    def check_teacher_click(self):
        mx, my = pygame.mouse.get_pos()
        camera_x = max(0, min(self.player_rect.centerx - (config.SCREEN_WIDTH // 2), self.map_pixel_width - config.SCREEN_WIDTH))
        camera_y = max(0, min(self.player_rect.centery - (config.SCREEN_HEIGHT // 2), self.map_pixel_height - config.SCREEN_HEIGHT))
        world_mx = mx + camera_x
        world_my = my + camera_y
        
        for teacher in self.teachers:
            if not teacher.defeated and teacher.rect.collidepoint(world_mx, world_my):
                self.start_cutscene(teacher)

    def start_cutscene(self, teacher):
        self.state = "CUTSCENE"
        self.active_teacher = teacher
        self.cutscene_timer = 0

    def end_cutscene_start_boss(self):
        if self.active_teacher:
            # Verwijder de teacher (NPC)
            if self.active_teacher in self.teachers:
                self.teachers.remove(self.active_teacher)
                
                # Bepaal positie
                boss_x = self.active_teacher.rect.x
                boss_y = self.active_teacher.rect.y
                
                # Spawn de Boss Enemy
                boss = Enemy(boss_x, boss_y, self.map_data_original, is_boss=True)
                
                # Check of het de Final Boss is
                if self.current_map_name == "director_room":
                    boss.hp = 500 # FINAL BOSS HP
                    print("[INFO] Final Boss (Shooter Mode) Spawned!")
                else:
                    boss.hp = 200 # MINI BOSS HP
                    print("[INFO] Mini Boss Spawned!")
                
                self.enemies.append(boss)
                
            self.active_teacher = None
            self.state = "PLAYING" # Gewoon doorspelen!

    def handle_combat(self):
        projectiles_to_keep = []
        for p in self.projectiles:
            if not p.active: continue

            col = int(p.rect.centerx // self.tile_size)
            row = int(p.rect.centery // self.tile_size)
            hit_wall = False
            if 0 <= row < len(self.map_data) and 0 <= col < len(self.map_data[row]):
                tile = self.map_data[row][col]
                if tile == 'W' or tile == 'b' or tile == 'L' or tile == 'B': 
                    hit_wall = True
            if hit_wall: continue 

            hit_enemy = False
            for e in self.enemies:
                if not e.is_cured and p.rect.colliderect(e.rect):
                    e.take_damage(p.damage)
                    hit_enemy = True
                    
                    for _ in range(12): 
                        self.particles.append(Particle(e.rect.centerx, e.rect.centery, (200, 0, 0)))

                    if e.is_cured:
                        self.player_xp += config.XP_PER_ZOMBIE
                        if e.is_boss:
                            self.cleared_rooms.append(self.current_room_id)
                            self.save_game()
                    break 
            if not hit_enemy:
                projectiles_to_keep.append(p)
        self.projectiles = projectiles_to_keep

        for e in self.enemies:
            if not e.is_cured and e.rect.colliderect(self.player_rect):
                if self.player_invulnerable_timer == 0:
                    self.player_hp -= 10 
                    self.player_invulnerable_timer = 60 
                    self.add_screen_shake(15) 
                    
                    if self.player_hp <= 0:
                        self.state = "GAMEOVER"

    def check_wall_collision(self):
        points = [self.player_rect.topleft, self.player_rect.topright,
                  self.player_rect.bottomleft, self.player_rect.bottomright]
        for point in points:
            col = int(point[0] // self.tile_size)
            row = int(point[1] // self.tile_size)
            if row < 0 or col < 0 or row >= len(self.map_data) or col >= len(self.map_data[0]):
                return True
            if 0 <= row < len(self.map_data):
                if 0 <= col < len(self.map_data[row]):
                    tile = self.map_data[row][col]
                    if tile == 'W' or tile == 'b': return True
                    if tile == 'B': return True 
                    if tile == 'L': return True
        for t in self.teachers:
            if self.player_rect.colliderect(t.rect.inflate(-10, -10)):
                return True
        return False

    def check_events(self):
        center_x = self.player_rect.centerx
        center_y = self.player_rect.centery
        col = int(center_x // self.tile_size)
        row = int(center_y // self.tile_size)
        
        neighbors = [(row, col+1), (row, col-1), (row+1, col), (row-1, col)]
        for nr, nc in neighbors:
            if 0 <= nr < len(self.map_data) and 0 <= nc < len(self.map_data[nr]):
                if self.map_data[nr][nc] == 'L':
                    door_rect = pygame.Rect(nc*self.tile_size, nr*self.tile_size, self.tile_size, self.tile_size)
                    if self.player_rect.colliderect(door_rect.inflate(10, 10)):
                        if self.has_key:
                            self.saved_map_name = self.current_map_name
                            self.saved_position = (self.player_rect.x, self.player_rect.y) 
                            self.current_room_id = "director_room"
                            self.load_map("director_room")
                            self.player_rect.x = 9 * self.tile_size 
                            self.player_rect.y = 8 * self.tile_size 
                            self.has_key = False 
                            self.show_popup_message("DEUR GEOPEND!")
                            self.save_game()
                        else:
                            if self.popup_timer == 0:
                                self.show_popup_message("GESLOTEN! ZOEK SLEUTEL")

        if 0 <= row < len(self.map_data) and 0 <= col < len(self.map_data[row]):
            tile_char = self.map_data[row][col]
            
            if tile_char in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                room_id = tile_char
                if room_id not in self.cleared_rooms:
                    self.saved_map_name = self.current_map_name
                    self.saved_position = (self.player_rect.x, self.player_rect.y - 64) 
                    self.current_room_id = room_id
                    self.load_map("classroom")
                    self.player_rect.x = 9 * self.tile_size 
                    self.player_rect.y = 12 * self.tile_size 
                    self.save_game()
            
            elif tile_char == 'E':
                if self.saved_map_name and self.saved_position is not None:
                    self.load_map(self.saved_map_name)
                    self.player_rect.x, self.player_rect.y = self.saved_position
                    self.saved_position = None
                    self.current_room_id = None
                    self.save_game()
                else:
                    self.load_map("ground")
                    self.player_rect.x = 4 * self.tile_size
                    self.player_rect.y = 25 * self.tile_size
            
            elif tile_char == '>': 
                if len(self.cleared_rooms) >= 1: 
                    self.load_map("first")
                    self.player_rect.topleft = self.find_spawn_point('<')
                    self.save_game() 
                else:
                     self.player_rect.x -= 10 

            elif tile_char == '<':
                self.load_map("ground")
                self.player_rect.topleft = self.find_spawn_point('>')
                self.save_game() 

    def draw(self):
        self.screen.fill(config.BLACK)

        shake_x = 0
        shake_y = 0
        if self.screen_shake > 0:
            shake_x = random.randint(-self.screen_shake, self.screen_shake)
            shake_y = random.randint(-self.screen_shake, self.screen_shake)
            self.screen_shake -= 1

        camera_x = max(0, min(self.player_rect.centerx - (config.SCREEN_WIDTH // 2), self.map_pixel_width - config.SCREEN_WIDTH))
        camera_y = max(0, min(self.player_rect.centery - (config.SCREEN_HEIGHT // 2), self.map_pixel_height - config.SCREEN_HEIGHT))
        
        camera_x += shake_x
        camera_y += shake_y

        start_col = int(camera_x // self.tile_size)
        end_col = start_col + (config.SCREEN_WIDTH // self.tile_size) + 2
        start_row = int(camera_y // self.tile_size)
        end_row = start_row + (config.SCREEN_HEIGHT // self.tile_size) + 2

        # 1. VLOER
        for row in range(start_row, min(end_row, len(self.map_data))):
            current_row_len = len(self.map_data[row])
            for col in range(start_col, min(end_col, current_row_len)):
                x = (col * self.tile_size) - camera_x
                y = (row * self.tile_size) - camera_y
                if "floor" in config.ASSETS: self.screen.blit(config.ASSETS["floor"], (x, y))
                else: pygame.draw.rect(self.screen, (100,100,100), (x, y, self.tile_size, self.tile_size))

        # 2. ENTITEITEN & MUREN
        entities_by_row = {}
        
        p_row = int(self.player_rect.centery // self.tile_size)
        if p_row not in entities_by_row: entities_by_row[p_row] = []
        entities_by_row[p_row].append("player")
        
        for e in self.enemies:
            e_row = int(e.rect.centery // self.tile_size)
            if e_row not in entities_by_row: entities_by_row[e_row] = []
            entities_by_row[e_row].append(e)
            
        for t in self.teachers:
            t_row = int(t.rect.centery // self.tile_size)
            if t_row not in entities_by_row: entities_by_row[t_row] = []
            entities_by_row[t_row].append(t)
            
        for i in self.items:
            i_row = int(i.rect.centery // self.tile_size)
            if i_row not in entities_by_row: entities_by_row[i_row] = []
            entities_by_row[i_row].append(i)

        for row in range(start_row, min(end_row, len(self.map_data))):
            current_row_len = len(self.map_data[row])
            
            # A. Muren & Deuren
            for col in range(start_col, min(end_col, current_row_len)):
                char = self.map_data[row][col]
                x = (col * self.tile_size) - camera_x
                y = (row * self.tile_size) - camera_y

                if char == 'W':
                    img = config.ASSETS.get("wall")
                    if img: self.screen.blit(img, (x, y - (img.get_height() - self.tile_size)))
                    else: pygame.draw.rect(self.screen, (50,50,50), (x, y, self.tile_size, self.tile_size))
                elif char in ['1','2','3','4','5','6','7','8','9','0','E']: 
                    img = config.ASSETS.get("door")
                    if img: self.screen.blit(img, (x, y))
                    else: pygame.draw.rect(self.screen, (0,0,255), (x, y, self.tile_size, self.tile_size))
                    if char != 'E':
                         font = pygame.font.Font(None, 36)
                         text = font.render(char, True, (255,255,255))
                         self.screen.blit(text, (x+20, y+20))
                
                # LOCKED DOOR
                elif char == 'L':
                    img = config.ASSETS.get("locked_door")
                    if img: self.screen.blit(img, (x, y))
                    else: pygame.draw.rect(self.screen, (255,0,0), (x, y, self.tile_size, self.tile_size))
                
                elif char == 'b':
                     pygame.draw.rect(self.screen, (139, 69, 19), (x + 5, y + 20, 54, 40)) 
                elif char == 'B':
                     img = config.ASSETS.get("student_bench")
                     if img: self.screen.blit(img, (x, y))
                elif (char == '>' or char == '<'): 
                    img = config.ASSETS.get("stairs")
                    if img: self.screen.blit(img, (x, y))
            
            # B. Entiteiten
            if row in entities_by_row:
                for entity in entities_by_row[row]:
                    if entity == "player":
                        if self.player_invulnerable_timer % 10 < 5: 
                            player_draw_x = self.player_rect.x - camera_x
                            player_draw_y = self.player_rect.y - camera_y
                            if "player_sprites" in config.ASSETS and config.ASSETS["player_sprites"]:
                                
                                sprite_key = self.player_direction 
                                if self.is_moving:
                                    if self.player_direction in ["up", "down"]:
                                        foot = "_l" if self.animation_frame == 0 else "_r"
                                        sprite_key = "walk_" + self.player_direction + foot
                                        
                                    elif self.animation_frame == 1:
                                        sprite_key = "walk_" + self.player_direction
                                
                                sprite = config.ASSETS["player_sprites"].get(sprite_key, config.ASSETS["player_sprites"]["down"])
                                offset_x = (config.PLAYER_VISUAL_SIZE - config.PLAYER_SIZE) // 2
                                offset_y = config.PLAYER_VISUAL_SIZE - config.PLAYER_SIZE
                                self.screen.blit(sprite, (player_draw_x - offset_x, player_draw_y - offset_y))
                            else:
                                pygame.draw.rect(self.screen, config.PLAYER_COLOR, (player_draw_x, player_draw_y, config.PLAYER_SIZE, config.PLAYER_SIZE))
                    else:
                        if isinstance(entity, Teacher):
                            entity.draw(self.screen, camera_x, camera_y, self.player_rect)
                        else:
                            entity.draw(self.screen, camera_x, camera_y)


        # 3. PROJECTIELEN & PARTICLES
        for p in self.projectiles: p.draw(self.screen, camera_x, camera_y)
        for p in self.particles: p.draw(self.screen, camera_x, camera_y)

        # 4. LIGHTING SYSTEM
        if self.darkness_enabled:
            self.night_surface.fill(self.ambient_light)
            
            player_screen_x = self.player_rect.centerx - camera_x
            player_screen_y = self.player_rect.centery - camera_y
            
            pygame.draw.circle(self.night_surface, (255, 255, 255), 
                               (player_screen_x, player_screen_y), 
                               self.flashlight_radius)
            
            self.screen.blit(self.night_surface, (0, 0), special_flags=pygame.BLEND_MULT)

        # 5. HUD
        bar_width = 200
        hp_percent = self.player_hp / config.PLAYER_HP_MAX
        pygame.draw.rect(self.screen, (50, 50, 50), (20, 20, bar_width, 25))
        hp_color = (0, 255, 0)
        if hp_percent < 0.5: hp_color = (255, 165, 0)
        if hp_percent < 0.2: hp_color = (255, 0, 0)
        pygame.draw.rect(self.screen, hp_color, (20, 20, bar_width * hp_percent, 25))
        pygame.draw.rect(self.screen, (255, 255, 255), (20, 20, bar_width, 25), 3)

        curr_wep = self.weapons_owned[self.current_weapon_index]
        curr_ammo = self.ammo[curr_wep]
        font = pygame.font.Font(None, 36)
        
        wep_text = font.render(f"Wapen: {config.WEAPONS[curr_wep]['name']} (G)", True, (255, 255, 255))
        self.screen.blit(wep_text, (20, 60))
        
        ammo_color = (255, 255, 255)
        if curr_ammo == 0: ammo_color = (255, 0, 0)
        ammo_text = font.render(f"Ammo: {curr_ammo}", True, ammo_color)
        self.screen.blit(ammo_text, (20, 90))
        
        xp_text = font.render(f"XP: {self.player_xp}", True, (50, 150, 255))
        self.screen.blit(xp_text, (config.SCREEN_WIDTH - 150, 20))

        if self.has_key:
            pygame.draw.rect(self.screen, (255, 215, 0), (20, 130, 40, 40)) 
            key_text = font.render("SLEUTEL", True, (255, 215, 0))
            self.screen.blit(key_text, (70, 138))

        if self.popup_timer > 0:
            msg_surf = font.render(self.popup_message, True, (255, 255, 255))
            msg_rect = msg_surf.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT - 100))
            bg_rect = msg_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, (0,0,0), bg_rect)
            pygame.draw.rect(self.screen, (255,255,255), bg_rect, 2)
            self.screen.blit(msg_surf, msg_rect)

        if self.state == "CUTSCENE":
            self.draw_overlay_rect()
            font = pygame.font.Font(None, 32)
            
            # AANGEPASTE TEKST
            lines = ["LERAAR: 'Kom maar op student!'", "(Klik of druk SPATIE voor gevecht!)"]
            if self.current_map_name == "director_room":
                lines = ["DIRECTEUR: 'Eens zien of je slaagt...'", "(Klik of druk SPATIE voor examen!)"]
                
            for i, line in enumerate(lines):
                text = font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (70, config.SCREEN_HEIGHT - 130 + i*30))
            self.cutscene_timer += 1

        elif self.state == "PAUSED":
            self.draw_popup("PAUZE", ["R - Verder spelen", "Q - Stoppen"], (40, 40, 60))

        elif self.state == "GAMEOVER":
            self.draw_popup("GAME OVER", ["R - Opnieuw proberen", "Q - Afsluiten"], (60, 20, 20))

        pygame.display.flip()

    def draw_overlay_rect(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (50, config.SCREEN_HEIGHT - 160, config.SCREEN_WIDTH - 100, 150))
        pygame.draw.rect(self.screen, (255, 255, 255), (50, config.SCREEN_HEIGHT - 160, config.SCREEN_WIDTH - 100, 150), 3)

    def draw_centered_text(self, text, y_offset, color=(255, 255, 255), size=48):
        font = pygame.font.Font(None, size)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + y_offset))
        self.screen.blit(surf, rect)

    def draw_popup(self, title_text, options, bg_color):
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        box_w, box_h = 400, 300
        box_x = (config.SCREEN_WIDTH - box_w) // 2
        box_y = (config.SCREEN_HEIGHT - box_h) // 2

        pygame.draw.rect(self.screen, (20, 20, 20), (box_x + 8, box_y + 8, box_w, box_h)) 
        pygame.draw.rect(self.screen, bg_color, (box_x, box_y, box_w, box_h)) 
        pygame.draw.rect(self.screen, (200, 200, 200), (box_x, box_y, box_w, box_h), 4) 

        font_title = pygame.font.Font(None, 60)
        title_surf = font_title.render(title_text, True, (255, 215, 0)) 
        title_rect = title_surf.get_rect(center=(config.SCREEN_WIDTH // 2, box_y + 50))
        self.screen.blit(title_surf, title_rect)

        font_opt = pygame.font.Font(None, 36)
        for i, opt in enumerate(options):
            opt_surf = font_opt.render(opt, True, (255, 255, 255))
            opt_rect = opt_surf.get_rect(center=(config.SCREEN_WIDTH // 2, box_y + 120 + (i * 50)))
            self.screen.blit(opt_surf, opt_rect)