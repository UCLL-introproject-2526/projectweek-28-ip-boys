import pygame
import random
import json
import os

from data import config
from data import UCLL_maps as maps
from data.enemy import Enemy
from data.npc import Teacher
from data.item import Item
from data.particle import Particle, CuredStudent
from data.player import Player
from data.ui import UI

class Game:
    def __init__(self, screen, load_saved=False, difficulty="NORMAL"):
        self.screen = screen
        self.tile_size = config.TILE_SIZE
        
        self.ui = UI(screen)
        self.player = Player(0, 0)
        
        # Difficulty
        self.difficulty = difficulty
        settings = config.DIFFICULTY_SETTINGS.get(difficulty, config.DIFFICULTY_SETTINGS["NORMAL"])
        self.zombie_spawn_rate = settings["spawn_rate"] 
        self.darkness_enabled = settings["darkness"]    
        
        # Lijsten
        self.projectiles = []
        self.enemies = []
        self.teachers = []
        self.items = [] 
        self.particles = [] 
        
        self.screen_shake = 0 
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

        # Lighting
        self.night_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.ambient_light = (10, 10, 20) 
        self.flashlight_radius = 250      

        if load_saved and os.path.exists(config.SAVE_FILE):
            self.load_game()
        else:
            self.load_map("ground") 
            self.player.rect.x = 4 * self.tile_size
            self.player.rect.y = 25 * self.tile_size

    def add_screen_shake(self, amount):
        self.screen_shake = max(self.screen_shake, amount)

    def save_game(self):
        data = {
            "difficulty": self.difficulty,
            "player_hp": self.player.hp,
            "player_xp": self.player.xp,
            "player_x": self.player.rect.x,
            "player_y": self.player.rect.y,
            "current_map_name": self.current_map_name,
            "weapons_owned": self.player.weapons_owned,
            "current_weapon_index": self.player.current_weapon_index,
            "ammo": self.player.ammo,
            "has_key": self.player.has_key,
            "cleared_rooms": self.cleared_rooms,
            "saved_position": self.saved_position,
            "saved_map_name": self.saved_map_name,
            "current_room_id": self.current_room_id
        }
        try:
            with open(config.SAVE_FILE, 'w') as f:
                json.dump(data, f)
            print("Spel opgeslagen.")
        except Exception as e:
            print(f"Fout opslaan: {e}")

    def load_game(self):
        try:
            with open(config.SAVE_FILE, 'r') as f:
                data = json.load(f)
            
            self.difficulty = data.get("difficulty", self.difficulty)
            settings = config.DIFFICULTY_SETTINGS.get(self.difficulty, config.DIFFICULTY_SETTINGS["NORMAL"])
            self.zombie_spawn_rate = settings["spawn_rate"]
            self.darkness_enabled = settings["darkness"]

            self.player.hp = data.get("player_hp", 100)
            self.player.xp = data.get("player_xp", 0)
            self.player.weapons_owned = data.get("weapons_owned", ["pistol"])
            self.player.current_weapon_index = data.get("current_weapon_index", 0)
            self.player.ammo = data.get("ammo", {"pistol": 20, "shotgun": 0})
            self.player.has_key = data.get("has_key", False)
            
            self.current_map_name = data.get("current_map_name", "ground")
            self.cleared_rooms = data.get("cleared_rooms", [])
            self.saved_position = data.get("saved_position", None)
            self.saved_map_name = data.get("saved_map_name", "ground")
            self.current_room_id = data.get("current_room_id", None)
            
            self.load_map(self.current_map_name)
            self.player.rect.x = data.get("player_x", 4 * config.TILE_SIZE)
            self.player.rect.y = data.get("player_y", 25 * config.TILE_SIZE)
            
        except Exception as e:
            print(f"Fout laden: {e}")
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
                    else:
                        # --- HIER BEPALEN WE HET TYPE LERAAR ---
                        # Als we in de director_room zijn, gebruiken we de 'director' sprite
                        if self.current_map_name == "director_room":
                            self.teachers.append(Teacher(col_idx * self.tile_size, row_idx * self.tile_size, sprite_type="director"))
                        else:
                            # Anders gewoon de normale teacher
                            self.teachers.append(Teacher(col_idx * self.tile_size, row_idx * self.tile_size, sprite_type="teacher"))
                    new_row += "." 
                elif char == 'b': new_row += "b"
                elif char == 'B': new_row += "B"
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
                    if not self.player.has_key:
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
        self.player.hp = config.PLAYER_HP_MAX
        self.player.xp = 0 
        self.player.has_key = False
        self.player.weapons_owned = ["pistol"]
        self.player.current_weapon_index = 0
        self.player.ammo["pistol"] = config.WEAPONS["pistol"]["start_ammo"]
        self.player.ammo["shotgun"] = config.WEAPONS["shotgun"]["start_ammo"]

        self.cleared_rooms = []
        self.current_room_id = None
        
        self.load_map("ground")
        self.player.rect.x = 4 * self.tile_size
        self.player.rect.y = 25 * self.tile_size
        self.state = "PLAYING"
        self.save_game()

    def spawn_random_zombie(self):
        if self.current_map_name not in ["ground", "first"]: return
        attempts = 0
        while attempts < 10:
            r_row = random.randint(0, len(self.map_data) - 1)
            r_col = random.randint(0, len(self.map_data[0]) - 1)
            if self.map_data[r_row][r_col] == '.':
                spawn_x = r_col * self.tile_size
                spawn_y = r_row * self.tile_size
                dist = ((spawn_x - self.player.rect.x)**2 + (spawn_y - self.player.rect.y)**2)**0.5
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
        
        if self.state == "WIN":
            if keys[pygame.K_r]: self.reset_game()
            if keys[pygame.K_q]: pygame.quit(); exit()
            return

        if self.state == "GAMEOVER":
            if keys[pygame.K_r]: self.reset_game()
            if keys[pygame.K_q]: self.state = "MENU"; pygame.quit(); exit() 
            return
        
        if self.state == "CUTSCENE": 
            if self.cutscene_timer > 30:
                if keys[pygame.K_RETURN] or mouse_clicked:
                    self.end_cutscene_start_boss()
            return

        # Speler Input
        self.player.handle_input(self.map_data, self.projectiles, self)

        # Interactie Teacher
        if keys[pygame.K_e]:
            for teacher in self.teachers:
                if not teacher.defeated and teacher.is_player_near(self.player.rect):
                    self.start_cutscene(teacher)
                    break 

        # Items
        for item in self.items[:]:
            if self.player.rect.colliderect(item.rect):
                if item.item_type == "health":
                    self.player.hp = min(config.PLAYER_HP_MAX, self.player.hp + config.HEALTH_REGEN)
                    self.items.remove(item)
                elif item.item_type == "ammo":
                    self.player.ammo["pistol"] += config.AMMO_PACK_AMOUNT
                    if "shotgun" in self.player.weapons_owned:
                         self.player.ammo["shotgun"] += 2
                    self.items.remove(item)
                elif item.item_type == "shotgun":
                    if "shotgun" not in self.player.weapons_owned:
                        self.player.weapons_owned.append("shotgun")
                    self.player.ammo["shotgun"] += config.SHOTGUN_AMMO_AMOUNT
                    self.items.remove(item)
                elif item.item_type == "key": 
                    self.player.has_key = True
                    self.show_popup_message("SLEUTEL GEVONDEN!")
                    self.save_game()
                    self.items.remove(item)

        self.check_events()
        self.zombie_spawn_timer -= 1
        if self.zombie_spawn_timer <= 0:
            self.spawn_random_zombie()
            self.zombie_spawn_timer = self.zombie_spawn_rate

        self.player.update()
        if self.popup_timer > 0: self.popup_timer -= 1

        for e in self.enemies: e.update(self.player.rect)
        for p in self.projectiles: p.update()
        for p in self.particles[:]:
            p.update()
            if p.lifetime <= 0: self.particles.remove(p)

        self.handle_combat()

    def show_popup_message(self, msg):
        self.popup_message = msg
        self.popup_timer = 120 

    def start_cutscene(self, teacher):
        self.state = "CUTSCENE"
        self.active_teacher = teacher
        self.cutscene_timer = 0

    def end_cutscene_start_boss(self):
        if self.active_teacher:
            if self.active_teacher in self.teachers:
                self.teachers.remove(self.active_teacher)
                boss_x, boss_y = self.active_teacher.rect.x, self.active_teacher.rect.y
                boss = Enemy(boss_x, boss_y, self.map_data_original, is_boss=True)
                
                if self.current_map_name == "director_room":
                    boss.hp = 500
                    boss.max_hp = 500
                else:
                    boss.hp = 200
                    boss.max_hp = 200
                self.enemies.append(boss)
            self.active_teacher = None
            self.state = "PLAYING"

    def handle_combat(self):
        projectiles_to_keep = []
        for p in self.projectiles:
            if not p.active: continue
            col = int(p.rect.centerx // self.tile_size)
            row = int(p.rect.centery // self.tile_size)
            
            # Wall Collision
            hit_wall = False
            if 0 <= row < len(self.map_data) and 0 <= col < len(self.map_data[row]):
                tile = self.map_data[row][col]
                if tile in ['W', 'b', 'L', 'B']: hit_wall = True
            if hit_wall: continue 

            # Enemy Collision
            hit_enemy = False
            for e in self.enemies:
                if not e.is_cured and p.rect.colliderect(e.rect):
                    e.take_damage(p.damage)
                    hit_enemy = True
                    
                    # Klein hit effectje (wit/blauw)
                    for _ in range(3): 
                         self.particles.append(Particle(e.rect.centerx, e.rect.centery, (200, 200, 255)))

                    if e.is_cured:
                        # --- HIER IS DE MAGIE: SPLAT & BUBBEL ---
                        
                        # 1. SPLAT! (Veel particles, paars/groen slijm effect)
                        for _ in range(25):
                            splat_color = random.choice([(100, 200, 100), (50, 150, 50), (200, 0, 200)])
                            self.particles.append(Particle(e.rect.centerx, e.rect.centery, splat_color, speed_range=6, size_range=8))
                        
                        # 2. SPAWN DE GEREDDE STUDENT (bubbel die omhoog vliegt)
                        self.particles.append(CuredStudent(e.rect.centerx, e.rect.centery))

                        self.player.xp += config.XP_PER_ZOMBIE
                        if e.is_boss:
                            if self.current_map_name == "director_room":
                                self.state = "WIN"
                                self.save_game()
                                return
                            else:
                                self.cleared_rooms.append(self.current_room_id)
                                self.save_game()
                                break 
            if not hit_enemy:
                projectiles_to_keep.append(p)
        self.projectiles = projectiles_to_keep
        
        # Verwijder genezen vijanden uit de lijst
        # (Omdat we nu een CuredStudent in de particles lijst stoppen, 
        # hoeven we de Enemy niet meer te bewaren voor de tekening)
        self.enemies = [e for e in self.enemies if not e.is_cured]

        # Player Hit
        for e in self.enemies:
            if not e.is_cured and e.rect.colliderect(self.player.rect):
                if self.player.invulnerable_timer == 0:
                    self.player.hp -= 10 
                    self.player.invulnerable_timer = 60 
                    self.add_screen_shake(15) 
                    if self.player.hp <= 0:
                        self.state = "GAMEOVER"

    def check_events(self):
        center_x, center_y = self.player.rect.centerx, self.player.rect.centery
        col = int(center_x // self.tile_size)
        row = int(center_y // self.tile_size)
        
        # Deuren
        neighbors = [(row, col+1), (row, col-1), (row+1, col), (row-1, col)]
        for nr, nc in neighbors:
            if 0 <= nr < len(self.map_data) and 0 <= nc < len(self.map_data[nr]):
                if self.map_data[nr][nc] == 'L':
                    door_rect = pygame.Rect(nc*self.tile_size, nr*self.tile_size, self.tile_size, self.tile_size)
                    if self.player.rect.colliderect(door_rect.inflate(10, 10)):
                        if self.player.has_key:
                            self.saved_map_name = self.current_map_name
                            self.saved_position = (self.player.rect.x, self.player.rect.y) 
                            self.current_room_id = "director_room"
                            self.load_map("director_room")
                            self.player.rect.x = 9 * self.tile_size 
                            self.player.rect.y = 8 * self.tile_size 
                            self.player.has_key = False 
                            self.show_popup_message("DOOR OPENED!")
                            self.save_game()
                        else:
                            if self.popup_timer == 0:
                                self.show_popup_message("CLOSED! SEARCH FOR A KEY")

        if 0 <= row < len(self.map_data) and 0 <= col < len(self.map_data[row]):
            tile_char = self.map_data[row][col]
            
            if tile_char in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                room_id = tile_char
                if room_id not in self.cleared_rooms:
                    self.saved_map_name = self.current_map_name
                    self.saved_position = (self.player.rect.x, self.player.rect.y - 64) 
                    self.current_room_id = room_id
                    self.load_map("classroom")
                    self.player.rect.x = 9 * self.tile_size 
                    self.player.rect.y = 12 * self.tile_size 
                    self.save_game()
            
            elif tile_char == 'E':
                active_enemies = [e for e in self.enemies if not e.is_cured]
                if len(active_enemies) > 0:
                    if self.popup_timer == 0: self.show_popup_message("BEAT THE BOSS FIRST!")
                else:
                    if self.saved_map_name and self.saved_position is not None:
                        self.load_map(self.saved_map_name)
                        self.player.rect.x, self.player.rect.y = self.saved_position
                        self.saved_position = None
                        self.current_room_id = None
                        self.save_game()
                    else:
                        self.load_map("ground")
                        self.player.rect.x = 4 * self.tile_size
                        self.player.rect.y = 25 * self.tile_size
            
            # ===============================
            # TRAPPEN (UP & DOWN) – NEIGHBOR BASED
            # ===============================

            # --- TRAP NAAR VOLGENDE VERDIEPING (>) ---
            for nr, nc in neighbors:
                if 0 <= nr < len(self.map_data) and 0 <= nc < len(self.map_data[nr]):
                    if self.map_data[nr][nc] == '>':
                        stair_rect = pygame.Rect(
                            nc * self.tile_size,
                            nr * self.tile_size,
                            self.tile_size,
                            self.tile_size
                        )

                        if self.player.rect.colliderect(stair_rect.inflate(10, 10)):
                            if len(self.cleared_rooms) < 6:
                                if self.popup_timer == 0:
                                    self.show_popup_message("First defeat all bosses!")
                                    return
                            else:
                                self.load_map("first")
                                self.player.rect.topleft = self.find_spawn_point('<')
                                self.save_game()
                                return


                # --- TRAP TERUG NAAR BENEDEN (<) ---
                for nr, nc in neighbors:
                    if 0 <= nr < len(self.map_data) and 0 <= nc < len(self.map_data[nr]):
                        if self.map_data[nr][nc] == '<':
                            stair_rect = pygame.Rect(
                                nc * self.tile_size,
                                nr * self.tile_size,
                                self.tile_size,
                                self.tile_size
                            )

                            if self.player.rect.colliderect(stair_rect.inflate(10, 10)):
                                self.load_map("ground")
                                self.player.rect.topleft = self.find_spawn_point('>')
                                self.save_game()
                                return


    def draw(self):
        self.screen.fill(config.BLACK)

        shake_x = 0
        shake_y = 0
        if self.screen_shake > 0:
            shake_x = random.randint(-self.screen_shake, self.screen_shake)
            shake_y = random.randint(-self.screen_shake, self.screen_shake)
            self.screen_shake -= 1

        camera_x = max(0, min(self.player.rect.centerx - (config.SCREEN_WIDTH // 2), self.map_pixel_width - config.SCREEN_WIDTH))
        camera_y = max(0, min(self.player.rect.centery - (config.SCREEN_HEIGHT // 2), self.map_pixel_height - config.SCREEN_HEIGHT))
        camera_x += shake_x
        camera_y += shake_y

        start_col = int(camera_x // self.tile_size)
        end_col = start_col + (config.SCREEN_WIDTH // self.tile_size) + 2
        start_row = int(camera_y // self.tile_size)
        end_row = start_row + (config.SCREEN_HEIGHT // self.tile_size) + 2

        # Draw Map
        for row in range(start_row, min(end_row, len(self.map_data))):
            current_row_len = len(self.map_data[row])
            for col in range(start_col, min(end_col, current_row_len)):
                x = (col * self.tile_size) - camera_x
                y = (row * self.tile_size) - camera_y
                if "floor" in config.ASSETS: self.screen.blit(config.ASSETS["floor"], (x, y))
                else: pygame.draw.rect(self.screen, (100,100,100), (x, y, self.tile_size, self.tile_size))

        # Entities
        entities_by_row = {}
        p_row = int(self.player.rect.centery // self.tile_size)
        if p_row not in entities_by_row: entities_by_row[p_row] = []
        entities_by_row[p_row].append(self.player)
        
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
                elif char == 'L':
                    img = config.ASSETS.get("locked_door")
                    if img: self.screen.blit(img, (x, y))
                elif char == 'b':
                     pygame.draw.rect(self.screen, (139, 69, 19), (x + 5, y + 20, 54, 40)) 
                elif char == 'B':
                     img = config.ASSETS.get("student_bench")
                     if img: self.screen.blit(img, (x, y))
                elif (char == '>' or char == '<'): 
                    img = config.ASSETS.get("stairs")
                    if img: self.screen.blit(img, (x, y))
            
            if row in entities_by_row:
                for entity in entities_by_row[row]:
                    if isinstance(entity, Teacher):
                        entity.draw(self.screen, camera_x, camera_y, self.player.rect)
                    else:
                        entity.draw(self.screen, camera_x, camera_y)

        for p in self.projectiles: p.draw(self.screen, camera_x, camera_y)
        for p in self.particles: p.draw(self.screen, camera_x, camera_y)

        # Lighting
        if self.darkness_enabled:
            self.night_surface.fill(self.ambient_light)
            player_screen_x = self.player.rect.centerx - camera_x
            player_screen_y = self.player.rect.centery - camera_y
            pygame.draw.circle(self.night_surface, (255, 255, 255), (player_screen_x, player_screen_y), self.flashlight_radius)
            self.screen.blit(self.night_surface, (0, 0), special_flags=pygame.BLEND_MULT)

        # UI
        self.ui.draw_hud(self.player)

        if self.popup_timer > 0: self.ui.draw_popup_message(self.popup_message)

        if self.state == "CUTSCENE":
            self.ui.draw_cutscene_overlay(self.current_map_name)
            self.cutscene_timer += 1
        elif self.state == "PAUSED":
            self.ui.draw_full_screen_popup("PAUSE", ["R - Continue", "Q - Quit"], (40, 40, 60))
        elif self.state == "GAMEOVER":
            self.ui.draw_full_screen_popup("GAME OVER", ["R - Try again", "Q - Quit"], (60, 20, 20))
        elif self.state == "WIN":
            self.ui.draw_full_screen_popup("YOU GRADUATED 🎓",["R - Continue", "Q - Quit"],(20, 100, 20))

        pygame.display.flip()