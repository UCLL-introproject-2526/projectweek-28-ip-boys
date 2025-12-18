import pygame
from data import config

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 60)

    def draw_hud(self, player):
        # Health bar
        bar_width = 200
        hp_percent = player.hp / config.PLAYER_HP_MAX
        pygame.draw.rect(self.screen, (50, 50, 50), (20, 20, bar_width, 25))
        
        hp_color = (0, 255, 0)
        if hp_percent < 0.5: hp_color = (255, 165, 0)
        if hp_percent < 0.2: hp_color = (255, 0, 0)
        
        pygame.draw.rect(self.screen, hp_color, (20, 20, bar_width * hp_percent, 25))
        pygame.draw.rect(self.screen, (255, 255, 255), (20, 20, bar_width, 25), 3)

        # Wapen Info
        curr_wep = player.weapons_owned[player.current_weapon_index]
        curr_ammo = player.ammo[curr_wep]
        
        wep_text = self.font.render(f"WEAPON: {config.WEAPONS[curr_wep]['name']} (G)", True, (255, 255, 255))
        self.screen.blit(wep_text, (20, 60))
        
        ammo_color = (255, 255, 255)
        if curr_ammo == 0: ammo_color = (255, 0, 0)
        ammo_text = self.font.render(f"AMMO: {curr_ammo}", True, ammo_color)
        self.screen.blit(ammo_text, (20, 90))
        
        # XP Info
        xp_text = self.font.render(f"XP: {player.xp}", True, (50, 150, 255))
        self.screen.blit(xp_text, (config.SCREEN_WIDTH - 150, 20))

        # Sleutel
        if player.has_key:
            pygame.draw.rect(self.screen, (255, 215, 0), (20, 130, 40, 40)) 
            key_text = self.font.render("SLEUTEL", True, (255, 215, 0))
            self.screen.blit(key_text, (70, 138))

    def draw_popup_message(self, message):
        msg_surf = self.font.render(message, True, (255, 255, 255))
        msg_rect = msg_surf.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT - 100))
        bg_rect = msg_rect.inflate(20, 10)
        
        pygame.draw.rect(self.screen, (0,0,0), bg_rect)
        pygame.draw.rect(self.screen, (255,255,255), bg_rect, 2)
        self.screen.blit(msg_surf, msg_rect)

    def draw_cutscene_overlay(self, map_name):
        pygame.draw.rect(self.screen, (0, 0, 0), (50, config.SCREEN_HEIGHT - 160, config.SCREEN_WIDTH - 100, 150))
        pygame.draw.rect(self.screen, (255, 255, 255), (50, config.SCREEN_HEIGHT - 160, config.SCREEN_WIDTH - 100, 150), 3)
        
        lines = ["TEACHER: 'TRY ME, STUDENT!'", "(CLICK ON ENTER FOR A FIGHT!)"]
        if map_name == "PRINCIPAL_ROOM":
            lines = ["PRINCIPAL: 'LET'S SEE IF U CAN SUCCEED...'", "(CLICK ON ENTER FOR A FIGHT!)"]
            
        font = pygame.font.Font(None, 32)
        for i, line in enumerate(lines):
            text = font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (70, config.SCREEN_HEIGHT - 130 + i*30))

    def draw_full_screen_popup(self, title_text, options, bg_color):
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

        title_surf = self.title_font.render(title_text, True, (255, 215, 0)) 
        title_rect = title_surf.get_rect(center=(config.SCREEN_WIDTH // 2, box_y + 50))
        self.screen.blit(title_surf, title_rect)

        for i, opt in enumerate(options):
            opt_surf = self.font.render(opt, True, (255, 255, 255))
            opt_rect = opt_surf.get_rect(center=(config.SCREEN_WIDTH // 2, box_y + 120 + (i * 50)))
            self.screen.blit(opt_surf, opt_rect)