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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z or event.key == pygame.K_e:
                    player.shoot()
                if event.key == pygame.K_q:
                    player.special_attack()

        keys = pygame.key.get_pressed()
        player.handle_movement(keys)
        player.handle_reload(keys)

        # Enemy spawning logic (only when no boss fight)
        if not boss_fight:
            spawn_timer += 1
            if spawn_timer > 120:  # Spawn an enemy every 2 seconds (60 FPS)
                enemy = Enemy(current_level)
                all_sprites.add(enemy)
                enemies.add(enemy)
                spawn_timer = 0

        # Level and boss check
        if not boss_fight and enemies_defeated >= 20:
            if current_level < 3:
                current_level += 1
                enemies_defeated = 0
            else:
                boss_fight = True
                boss = Boss(current_level)
                all_sprites.add(boss)
                enemies.add(boss)

        # Randomly spawn orbs
        orb_spawn_timer += 1
        if orb_spawn_timer > 300:  # Spawn orb every 5 seconds (at 60 FPS)
            orb_type = random.choice(['health', 'energy'])
            x_pos = random.randint(200, SCREEN_WIDTH - 50)
            orb = Orb(x_pos, GROUND_HEIGHT - 10, orb_type)
            all_sprites.add(orb)
            orbs.add(orb)
            orb_spawn_timer = 0

        # Check for orb collisions
        orb_hits = pygame.sprite.spritecollide(player, orbs, True)
        for orb in orb_hits:
            if orb.orb_type == 'health':
                player.gain_health(HEALTH_ORB_RESTORE)
            elif orb.orb_type == 'energy':
                player.gain_energy(ENERGY_ORB_GAIN)

        # Update all sprites
        all_sprites.update()

        # Handle collisions
        # Player collides with enemies
        if pygame.sprite.spritecollide(player, enemies, False):
            player.take_damage(ENEMY_COLLISION_DAMAGE)

        # Player collides with enemy projectiles
        enemy_projectile_hits = pygame.sprite.spritecollide(player, enemy_projectiles, True)
        for projectile in enemy_projectile_hits:
            player.take_damage(ENEMY_PROJECTILE_DAMAGE)  # Apply damage from enemy projectile

        # Projectile hits an enemy
        hits = pygame.sprite.groupcollide(enemies, projectiles, False, True)
        for enemy, bullet_list in hits.items():
            for bullet in bullet_list:
                enemy.health -= PROJECTILE_DAMAGE
                if enemy.health <= 0:
                    enemy.kill()
                    enemies_defeated += 1
                    player.gain_energy()  # Grant energy on enemy kill
                    total_kills += 1  # Increment total kills when an enemy is killed
                    if isinstance(enemy, Boss):
                        show_end_screen("You Win!")
                        return

        # Missile hits an enemy
        missile_hits = pygame.sprite.groupcollide(enemies, missiles, False, True)
        for enemy, missile_list in missile_hits.items():
            for missile in missile_list:
                enemy.health -= MISSILE_DAMAGE
                if enemy.health <= 0:
                    enemy.kill()
                    enemies_defeated += 1
                    player.gain_energy()  # Grant energy on enemy kill
                    total_kills += 1  # Increment total kills when an enemy is killed
                    if isinstance(enemy, Boss):
                        show_end_screen("You Win!")
                        return

        # Check if the player dies
        if player.health <= 0:
            show_end_screen("You Lose!")
            return

        # Drawing code
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        all_sprites.draw(screen)
        player.draw_info(screen)
        font = pygame.font.SysFont(None, 36)
        level_text = font.render(f"Level: {current_level}", True, BLACK)
        screen.blit(level_text, (SCREEN_WIDTH - 150, 10))

        # Draw boss health bar if boss is active
        if boss_fight and boss:
            boss.draw_health_bar(screen)

        pygame.display.flip()
        clock.tick(FPS)

def show_end_screen(message):
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 72)
    message_text = font.render(message, True, BLACK)
    kills_text = font.render(f"Total Kills: {total_kills}", True, BLACK)
    restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
    screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(kills_text, (SCREEN_WIDTH // 2 - kills_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run_game()  # Restart the game loop
                    waiting = False  # Exit the waiting loop after restart
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Start the game
run_game()
pygame.quit()
