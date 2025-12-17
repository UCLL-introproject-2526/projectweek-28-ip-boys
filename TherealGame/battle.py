import pygame
import config
import random

class PokemonBattle:
    def __init__(self, screen, player_hp, player_xp):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 50)
        
        # STATS
        self.player_hp = player_hp
        self.player_max_hp = config.PLAYER_HP_MAX
        
        # Bereken attack damage op basis van XP
        self.player_attack = config.BASE_ATTACK_DAMAGE + (player_xp * config.DAMAGE_PER_XP)
        self.player_attack = int(self.player_attack)
        
        self.enemy_hp = config.BOSS_HP
        self.enemy_max_hp = config.BOSS_HP
        self.enemy_attack = 15 # Boss doet vaste schade
        
        # STATUS
        # States: INTRO, PLAYER_TURN, PLAYER_ANIM, ENEMY_TURN, ENEMY_ANIM, WIN, LOSE
        self.state = "INTRO"
        self.message = "Professor stuurt MONSTER in!"
        self.timer = 0
        
        # MENU
        self.menu_options = ["FIGHT", "HEAL", "RUN"]
        self.selected_index = 0
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if self.state == "PLAYER_TURN":
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.execute_move()
                        
        elif self.state in ["WIN", "LOSE"]:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "EXIT" # Signaal naar main om te stoppen
        
        # Zorg dat we events flushen als we niet in player turn zijn
        else:
            pygame.event.clear()
            
    def execute_move(self):
        move = self.menu_options[self.selected_index]
        
        if move == "FIGHT":
            damage = self.player_attack + random.randint(-2, 5)
            self.enemy_hp -= damage
            self.message = f"Jij doet {damage} schade!"
            self.state = "PLAYER_ANIM"
            self.timer = 60 # Wacht 1 seconde
            
        elif move == "HEAL":
            heal = 40
            self.player_hp = min(self.player_max_hp, self.player_hp + heal)
            self.message = "Je genas 40 HP!"
            self.state = "PLAYER_ANIM"
            self.timer = 60
            
        elif move == "RUN":
            self.message = "Je kunt niet vluchten voor een examen!"
            self.state = "PLAYER_ANIM"
            self.timer = 60

    def update(self):
        if self.state == "INTRO":
            self.timer += 1
            if self.timer > 120: # 2 seconden intro
                self.state = "PLAYER_TURN"
                self.message = "Wat ga je doen?"
                
        elif self.state == "PLAYER_ANIM":
            self.timer -= 1
            if self.timer <= 0:
                if self.enemy_hp <= 0:
                    self.state = "WIN"
                    self.message = "JE HEBT GEWONNEN! (Druk Enter)"
                else:
                    self.state = "ENEMY_TURN"
                    
        elif self.state == "ENEMY_TURN":
            # Simpele AI
            damage = self.enemy_attack + random.randint(-5, 5)
            self.player_hp -= damage
            self.message = f"Monster doet {damage} schade!"
            self.state = "ENEMY_ANIM"
            self.timer = 60
            
        elif self.state == "ENEMY_ANIM":
            self.timer -= 1
            if self.timer <= 0:
                if self.player_hp <= 0:
                    self.state = "LOSE"
                    self.message = "JE BENT GEZAKT... (Druk Enter)"
                else:
                    self.state = "PLAYER_TURN"
                    self.message = "Wat ga je doen?"

    def draw(self):
        # 1. ACHTERGROND
        self.screen.fill(config.BATTLE_BG)
        
        # 2. SPRITES
        # Enemy (Rechtsboven)
        if "boss" in config.ASSETS:
            enemy_img = config.ASSETS["boss"]
            self.screen.blit(enemy_img, (config.SCREEN_WIDTH - 300, 100))
        
        # Player (Linksonder - Back view)
        if "player_back" in config.ASSETS:
            player_img = config.ASSETS["player_back"]
            self.screen.blit(player_img, (100, config.SCREEN_HEIGHT - 350))
            
        # 3. HEALTH BARS
        self.draw_health_bar(100, 100, self.enemy_hp, self.enemy_max_hp, "PROF. MONSTER")
        self.draw_health_bar(config.SCREEN_WIDTH - 400, config.SCREEN_HEIGHT - 150, self.player_hp, self.player_max_hp, "STUDENT (JIJ)")
        
        # 4. TEKST BOX / MENU
        pygame.draw.rect(self.screen, config.BATTLE_BOX, (0, config.SCREEN_HEIGHT - 150, config.SCREEN_WIDTH, 150))
        pygame.draw.rect(self.screen, config.WHITE, (0, config.SCREEN_HEIGHT - 150, config.SCREEN_WIDTH, 150), 4)
        
        if self.state == "PLAYER_TURN":
            # Teken Menu
            start_x = config.SCREEN_WIDTH - 300
            start_y = config.SCREEN_HEIGHT - 120
            for i, option in enumerate(self.menu_options):
                color = config.HIGHLIGHT_COLOR if i == self.selected_index else config.BATTLE_TEXT
                text = self.font.render(f"> {option}", True, color)
                self.screen.blit(text, (start_x, start_y + i * 40))
            
            # Teken vraag
            msg = self.font.render(self.message, True, config.BATTLE_TEXT)
            self.screen.blit(msg, (50, config.SCREEN_HEIGHT - 100))
            
        else:
            # Teken alleen bericht
            msg = self.big_font.render(self.message, True, config.BATTLE_TEXT)
            msg_rect = msg.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 75))
            self.screen.blit(msg, msg_rect)

        pygame.display.flip()

    def draw_health_bar(self, x, y, current, max_hp, name):
        # Achtergrond balk
        pygame.draw.rect(self.screen, (200, 200, 200), (x, y, 300, 100), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 300, 100), 3, border_radius=10)
        
        # Naam
        name_surf = self.font.render(name, True, (0, 0, 0))
        self.screen.blit(name_surf, (x + 20, y + 10))
        
        # Balk
        bar_width = 260
        pct = max(0, current / max_hp)
        color = config.HP_BAR_GOOD
        if pct < 0.5: color = config.HP_BAR_LOW
        if pct < 0.2: color = config.HP_BAR_CRIT
        
        pygame.draw.rect(self.screen, config.HP_BAR_BG, (x + 20, y + 50, bar_width, 20))
        pygame.draw.rect(self.screen, color, (x + 20, y + 50, bar_width * pct, 20))
        
        # HP Text
        hp_txt = self.font.render(f"{int(current)}/{max_hp}", True, (0,0,0))
        self.screen.blit(hp_txt, (x + 20, y + 75))