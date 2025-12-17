import pygame
import config
import random

class PokemonBattle:
    def __init__(self, screen, player_hp, player_xp):
        self.screen = screen
        
        # Fonts
        self.font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 30)
        
        # STATS
        self.player_hp = player_hp
        self.player_max_hp = config.PLAYER_HP_MAX
        
        # Attack damage met XP bonus
        base_dmg = config.BASE_ATTACK_DAMAGE
        bonus = int(player_xp * config.DAMAGE_PER_XP)
        self.player_attack = base_dmg + bonus
        
        self.enemy_hp = config.BOSS_HP
        self.enemy_max_hp = config.BOSS_HP
        self.enemy_attack = 15 
        
        # STATUS & ANIMATIE
        self.state = "INTRO"
        self.message = "DIRECTEUR daagt je uit!"
        self.timer = 0
        self.blink_timer = 0
        
        # MENU NAVIGATIE
        # 0: FIGHT, 1: HEAL
        # 2: ---  , 3: RUN
        self.menu_index = 0 
        self.show_fight_menu = False # Als we op FIGHT klikken
        
    def handle_input(self, event):
        """Verwerkt input die vanuit TheMain wordt doorgegeven."""
        
        if self.state == "PLAYER_TURN":
            if event.type == pygame.KEYDOWN:
                
                # NAVIGATIE (2x2 Grid)
                if event.key == pygame.K_LEFT:
                    self.menu_index = 0 if self.menu_index == 1 else 2
                elif event.key == pygame.K_RIGHT:
                    self.menu_index = 1 if self.menu_index == 0 else 3
                elif event.key == pygame.K_UP:
                    self.menu_index = 0 if self.menu_index == 2 else 1
                elif event.key == pygame.K_DOWN:
                    self.menu_index = 2 if self.menu_index == 0 else 3
                
                # ACTIE KIEZEN
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.execute_move()

        elif self.state in ["WIN", "LOSE"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = "EXIT" 

    def execute_move(self):
        # 0 = FIGHT
        if self.menu_index == 0:
            crit = random.random() < 0.1 # 10% critical hit kans
            dmg = self.player_attack + random.randint(-3, 5)
            if crit: 
                dmg = int(dmg * 1.5)
                self.message = f"CRITICAL HIT! {dmg} schade!"
            else:
                self.message = f"Je raakt de Boss! {dmg} schade!"
            
            self.enemy_hp -= dmg
            self.state = "PLAYER_ANIM"
            self.timer = 60 # Wacht 1 seconde
            
        # 1 = HEAL
        elif self.menu_index == 1:
            heal = 50
            self.player_hp = min(self.player_max_hp, self.player_hp + heal)
            self.message = "Je eet een broodje... +50 HP!"
            self.state = "PLAYER_ANIM"
            self.timer = 60
            
        # 3 = RUN
        elif self.menu_index == 3:
            self.message = "Je kunt niet spijbelen voor dit examen!"
            self.state = "PLAYER_ANIM" # Beurt gaat gewoon voorbij
            self.timer = 60
            
        # 2 = Leeg (of Magic/Items later)
        else:
            pass

    def update(self):
        self.blink_timer += 1
        
        if self.state == "INTRO":
            self.timer += 1
            if self.timer > 120:
                self.state = "PLAYER_TURN"
                self.message = "Wat ga je doen?"
                
        elif self.state == "PLAYER_ANIM":
            self.timer -= 1
            if self.timer <= 0:
                if self.enemy_hp <= 0:
                    self.state = "WIN"
                    self.message = "DIRECTEUR VERSLAGEN! (Druk Enter)"
                else:
                    self.state = "ENEMY_TURN"
                    
        elif self.state == "ENEMY_TURN":
            # Boss valt aan
            dmg = self.enemy_attack + random.randint(-5, 10)
            self.player_hp -= dmg
            self.message = f"Boss gebruikt 'Slecht Cijfer'! -{dmg} HP"
            self.state = "ENEMY_ANIM"
            self.timer = 80
            
        elif self.state == "ENEMY_ANIM":
            self.timer -= 1
            if self.timer <= 0:
                if self.player_hp <= 0:
                    self.state = "LOSE"
                    self.message = "HEREXAMEN... (Druk Enter)"
                else:
                    self.state = "PLAYER_TURN"
                    self.message = "Wat ga je doen?"

    def draw(self):
        # 1. ACHTERGROND (Gesplitst voor diepte)
        self.screen.fill((240, 240, 240)) # Lichte lucht
        # Groene cirkel onder enemy
        pygame.draw.ellipse(self.screen, (180, 220, 180), (config.SCREEN_WIDTH - 350, 180, 300, 100))
        # Groene cirkel onder player
        pygame.draw.ellipse(self.screen, (180, 220, 180), (50, config.SCREEN_HEIGHT - 300, 300, 100))

        # 2. SPRITES
        # Enemy (Rechtsboven)
        if "boss" in config.ASSETS:
            img = config.ASSETS["boss"]
            # Beetje laten zweven
            y_offset = 5 * (self.blink_timer // 10 % 2) 
            self.screen.blit(img, (config.SCREEN_WIDTH - 320, 80 + y_offset))
        
        # Player (Linksonder - Back)
        if "player_back" in config.ASSETS:
            img = config.ASSETS["player_back"]
            self.screen.blit(img, (100, config.SCREEN_HEIGHT - 350))

        # 3. GUI PANELEN (De zwarte balk onderaan)
        panel_rect = pygame.Rect(0, config.SCREEN_HEIGHT - 160, config.SCREEN_WIDTH, 160)
        pygame.draw.rect(self.screen, (40, 50, 60), panel_rect) # Donkergrijs
        pygame.draw.rect(self.screen, (200, 160, 60), panel_rect, 6) # Gouden rand

        # 4. TEKST OF MENU
        if self.state == "PLAYER_TURN":
            # RECHTS: ACTIE MENU (Wit vak)
            menu_rect = pygame.Rect(config.SCREEN_WIDTH - 400, config.SCREEN_HEIGHT - 150, 380, 140)
            pygame.draw.rect(self.screen, (255, 255, 255), menu_rect, border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0), menu_rect, 4, border_radius=10)
            
            options = ["FIGHT", "HEAL", "-", "RUN"]
            coords = [(50, 40), (220, 40), (50, 90), (220, 90)]
            
            for i, opt in enumerate(options):
                cx, cy = coords[i]
                # Kleur geselecteerde optie
                color = (200, 0, 0) if i == self.menu_index else (50, 50, 50)
                prefix = "> " if i == self.menu_index else ""
                
                txt_surf = self.font.render(prefix + opt, True, color)
                self.screen.blit(txt_surf, (menu_rect.x + cx, menu_rect.y + cy - 15))
            
            # LINKS: BERICHT "Wat ga je doen?"
            msg_surf = self.font.render(self.message, True, (255, 255, 255))
            self.screen.blit(msg_surf, (40, config.SCREEN_HEIGHT - 100))
            
        else:
            # ALLEEN TEKST (Gecentreerd of links)
            msg_surf = self.font.render(self.message, True, (255, 255, 255))
            self.screen.blit(msg_surf, (50, config.SCREEN_HEIGHT - 100))

        # 5. HEALTH BARS (Pokémon Stijl)
        self.draw_hp_box(50, 50, self.enemy_hp, self.enemy_max_hp, "PROF. MONSTER", 50)
        self.draw_hp_box(config.SCREEN_WIDTH - 400, config.SCREEN_HEIGHT - 420, self.player_hp, self.player_max_hp, "JENTE", 15)

    def draw_hp_box(self, x, y, curr, max_hp, name, level):
        # Wit vlak met zwarte rand
        pygame.draw.rect(self.screen, (250, 250, 240), (x, y, 320, 90), border_radius=5)
        pygame.draw.rect(self.screen, (0,0,0), (x, y, 320, 90), 3, border_radius=5)
        
        # Naam en Level
        name_surf = self.small_font.render(name, True, (0,0,0))
        lvl_surf = self.small_font.render(f"Lv{level}", True, (0,0,0))
        self.screen.blit(name_surf, (x+15, y+10))
        self.screen.blit(lvl_surf, (x+250, y+10))
        
        # HP Balk Achtergrond
        pygame.draw.rect(self.screen, (80, 80, 80), (x+50, y+45, 200, 15))
        
        # HP Balk Voorgrond (Kleur veranderd bij low HP)
        pct = max(0, curr / max_hp)
        col = (50, 200, 50) # Groen
        if pct < 0.5: col = (220, 180, 20) # Geel
        if pct < 0.2: col = (220, 50, 50) # Rood
        
        pygame.draw.rect(self.screen, col, (x+50, y+45, 200 * pct, 15))
        
        # HP Text (Alleen bij speler vaak, maar hier bij beiden voor duidelijkheid)
        hp_txt = self.small_font.render(f"{int(curr)} / {max_hp}", True, (50, 50, 50))
        self.screen.blit(hp_txt, (x+50, y+65))