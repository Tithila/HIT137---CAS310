import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
FPS = 60
WHITE, BLACK, RED, PINK, GOLD, DARK_YELLOW = (255, 255, 255), (0, 0, 0), (255, 0, 0), (255, 105, 180), (255, 215, 0), (255, 165, 0)
GROUND_HEIGHT = 350
GRAVITY = 1
PLAYER_SPEED, JUMP_STRENGTH = 5, -15
PROJECTILE_SPEED, MISSILE_DAMAGE = 10, 50
ENEMY_BASE_SPEED, ENEMY_BASE_HEALTH = 3, 10
PLAYER_MAX_HEALTH, PROJECTILE_DAMAGE, ENEMY_COLLISION_DAMAGE = 200, 5, 2
RELOAD_TIME, MAGAZINE_SIZE, SPECIAL_ATTACK_ENERGY = 1000, 30, 15
BOSS_HEALTH_MULTIPLIER = 5
HEALTH_ORB_RESTORE = 20
ENERGY_ORB_GAIN = 4
ENEMY_PROJECTILE_DAMAGE = 5 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side Scroller")
clock = pygame.time.Clock()

def create_img(width, height, color):
    img = pygame.Surface((width, height))
    img.fill(color)
    return img

player_img = create_img(40, 60, (0, 128, 255))
enemy_img = create_img(40, 60, RED)
boss_img = create_img(80, 120, (128, 0, 128))
projectile_img = create_img(10, 5, (0, 0, 128))
enemy_projectile_img = create_img(10, 5, RED)
missile_img = create_img(15, 10, DARK_YELLOW)
health_orb_img = create_img(15, 15, PINK)
energy_orb_img = create_img(15, 15, GOLD)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(midleft=(100, GROUND_HEIGHT - 30))
        self.health, self.ammo, self.energy = PLAYER_MAX_HEALTH, MAGAZINE_SIZE, 0
        self.speed_y, self.jumping, self.reloading, self.reload_time = 0, False, False, 0
        self.kills = 0

    def handle_movement(self, keys):
        self.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PLAYER_SPEED
        if not self.jumping and keys[pygame.K_SPACE]:
            self.speed_y, self.jumping = JUMP_STRENGTH, True
        self.speed_y += GRAVITY
        self.rect.y += self.speed_y
        if self.rect.bottom >= GROUND_HEIGHT:
            self.rect.bottom, self.speed_y, self.jumping = GROUND_HEIGHT, 0, False

    def handle_reload(self, keys):
        if keys[pygame.K_r] and not self.reloading:
            self.reloading = True
            self.reload_time = pygame.time.get_ticks()

        if self.reloading and pygame.time.get_ticks() - self.reload_time >= RELOAD_TIME:
            self.ammo, self.reloading = MAGAZINE_SIZE, False

    def shoot(self):
        if self.ammo > 0 and not self.reloading:
            projectile = Projectile(self.rect.right, self.rect.centery, 1)
            all_sprites.add(projectile)
            projectiles.add(projectile)
            self.ammo -= 1

    def special_attack(self):
        if self.energy >= SPECIAL_ATTACK_ENERGY:
            missile = Missile(self.rect.right, self.rect.centery)
            all_sprites.add(missile)
            missiles.add(missile)
            self.energy = 0

    def take_damage(self, amount):
        self.health = max(self.health - amount, 0)

    def gain_health(self, amount):
        self.health = min(self.health + amount, PLAYER_MAX_HEALTH)

    def gain_energy(self, amount=1):
        self.energy = min(self.energy + amount, SPECIAL_ATTACK_ENERGY)

    def draw_info(self, screen):
        def draw_bar(x, y, current, max_value, color):
            pygame.draw.rect(screen, BLACK, (x, y, 200, 20))
            pygame.draw.rect(screen, color, (x, y, 200 * (current / max_value), 20))

        draw_bar(10, 10, self.health, PLAYER_MAX_HEALTH, RED)
        font = pygame.font.SysFont(None, 24)
        ammo_text = font.render(f"Ammo: {self.ammo}/{MAGAZINE_SIZE}", True, RED if self.ammo == 0 else BLACK)
        energy_text = font.render(f"Energy: {self.energy}/{SPECIAL_ATTACK_ENERGY}", True, BLACK)
        kills_text = font.render(f"Kills: {total_kills}", True, BLACK)  
        screen.blit(ammo_text, (10, 40))
        screen.blit(energy_text, (10, 70))
        screen.blit(kills_text, (10, 100))  
        if self.ammo == 0:
            reload_text = font.render("(R) to Reload", True, RED)
            screen.blit(reload_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))

class Orb(pygame.sprite.Sprite):
    """Represents health and energy orbs."""
    def __init__(self, x, y, orb_type):
        super().__init__()
        self.orb_type = orb_type  
        self.image = health_orb_img if orb_type == 'health' else energy_orb_img
        self.rect = self.image.get_rect(midbottom=(x, y))

    def update(self):
        pass

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = projectile_img if direction == 1 else enemy_projectile_img
        self.rect = self.image.get_rect(midleft=(x, y))
        self.direction = direction

    def update(self):
        self.rect.x += PROJECTILE_SPEED * self.direction
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class Missile(Projectile):
    def __init__(self, x, y):
        super().__init__(x, y, 1)
        self.image = missile_img

    def update(self):
        self.rect.x += PROJECTILE_SPEED * 2
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH, GROUND_HEIGHT))
        self.health = ENEMY_BASE_HEALTH * (1.5 ** level)
        self.speed = ENEMY_BASE_SPEED * (1.1 ** level)
        self.shoot_timer = 0

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

        self.shoot_timer += 1
        if self.shoot_timer > 90:
            enemy_projectile = Projectile(self.rect.left, self.rect.centery, -1)
            all_sprites.add(enemy_projectile)
            enemy_projectiles.add(enemy_projectile)
            self.shoot_timer = 0

class Boss(Enemy):
    def __init__(self, level):
        super().__init__(level)
        self.image = boss_img
        self.health *= BOSS_HEALTH_MULTIPLIER
        self.speed = 0  
        self.rect.midright = (SCREEN_WIDTH - 50, GROUND_HEIGHT - 50)  

    def draw_health_bar(self, screen):
        bar_x, bar_y = SCREEN_WIDTH // 4, 20
        bar_width = SCREEN_WIDTH // 2  
        bar_height = 20

        max_health = ENEMY_BASE_HEALTH * BOSS_HEALTH_MULTIPLIER
        current_width = min(bar_width, int(bar_width * (self.health / max_health)))

        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height))  # Black background container
        pygame.draw.rect(screen, RED, (bar_x, bar_y, current_width, bar_height))  # Red health bar


all_sprites, projectiles, missiles, orbs = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
enemy_projectiles, enemies = pygame.sprite.Group(), pygame.sprite.Group()

def reset_game():
    global player, boss, current_level, enemies_defeated, total_kills, boss_fight
    all_sprites.empty()
    projectiles.empty()
    missiles.empty()
    orbs.empty()
    enemy_projectiles.empty()
    enemies.empty()
    
    player = Player()
    all_sprites.add(player)
    
    boss = None
    current_level, enemies_defeated, total_kills, boss_fight = 1, 0, 0, False

def run_game():
    global running, total_kills, enemies_defeated, boss_fight, current_level
    reset_game()
    
    running = True
    spawn_timer, orb_spawn_timer = 0, 0
    boss = None