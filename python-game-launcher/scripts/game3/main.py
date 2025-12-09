import pygame
import sys
import math
from constants import *
from firefly import Firefly
from level_manager import LevelManager
from enemies import Bug, Ant, Firefly_Enemy

pygame.init()

# încarcă sunete
try:
    jump_sound = pygame.mixer.Sound('sounds/jump-sound.wav')
    death_sound = pygame.mixer.Sound('sounds/death-sound.wav')
    collect_sound = pygame.mixer.Sound('sounds/collect-sound.wav')
    win_sound = pygame.mixer.Sound('sounds/win-sound.wav')

    # volume
    jump_sound.set_volume(0.4)
    death_sound.set_volume(0.5)
    collect_sound.set_volume(0.3)
    win_sound.set_volume(0.4)
except Exception as e:
    print(f"Nu s-au încărcat sunetele: {e}")
    jump_sound = None
    death_sound = None
    collect_sound = None
    win_sound = None

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shadow Switch - Firefly's Journey")
clock = pygame.time.Clock()

# fonts
font_large = pygame.font.Font(None, 70)
font_medium = pygame.font.Font(None, 45)
font_small = pygame.font.Font(None, 32)

# level manager
level_manager = LevelManager()
current_level = level_manager.current_level

# cream playerul
firefly = Firefly(100, GROUND_LEVEL - 50)

# camera position
screen_movement = 0

# game state
game_over = False
win = False
level_complete = False
death_by_spike = False
death_by_enemy = False
show_intro = True

# nori animați
cloud_positions = [
    {'x': 300, 'y': 80, 'speed': 0.2, 'scale': 0.9, 'alpha': 200},
    {'x': 550, 'y': 120, 'speed': 0.15, 'scale': 1.1, 'alpha': 180},
    {'x': 800, 'y': 90, 'speed': 0.25, 'scale': 0.8, 'alpha': 190},
    {'x': 400, 'y': 160, 'speed': 0.18, 'scale': 0.85, 'alpha': 170},
    {'x': 700, 'y': 180, 'speed': 0.22, 'scale': 0.95, 'alpha': 185},
]

def draw_gradient_background(screen):
    """desenam background cu gradient"""
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        if ratio < 0.5:
            r = int(SKY_TOP[0] + (SKY_MIDDLE[0] - SKY_TOP[0]) * (ratio * 2))
            g = int(SKY_TOP[1] + (SKY_MIDDLE[1] - SKY_TOP[1]) * (ratio * 2))
            b = int(SKY_TOP[2] + (SKY_MIDDLE[2] - SKY_TOP[2]) * (ratio * 2))
        else:
            r = int(SKY_MIDDLE[0] + (SKY_BOTTOM[0] - SKY_MIDDLE[0]) * ((ratio - 0.5) * 2))
            g = int(SKY_MIDDLE[1] + (SKY_BOTTOM[1] - SKY_MIDDLE[1]) * ((ratio - 0.5) * 2))
            b = int(SKY_MIDDLE[2] + (SKY_BOTTOM[2] - SKY_MIDDLE[2]) * ((ratio - 0.5) * 2))

        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))


def draw_background_with_decorations(screen):
    """background cu gradient + nori animați + soare"""

    # 1. Gradient (același)
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        if ratio < 0.5:
            r = int(SKY_TOP[0] + (SKY_MIDDLE[0] - SKY_TOP[0]) * (ratio * 2))
            g = int(SKY_TOP[1] + (SKY_MIDDLE[1] - SKY_TOP[1]) * (ratio * 2))
            b = int(SKY_TOP[2] + (SKY_MIDDLE[2] - SKY_TOP[2]) * (ratio * 2))
        else:
            r = int(SKY_MIDDLE[0] + (SKY_BOTTOM[0] - SKY_MIDDLE[0]) * ((ratio - 0.5) * 2))
            g = int(SKY_MIDDLE[1] + (SKY_BOTTOM[1] - SKY_MIDDLE[1]) * ((ratio - 0.5) * 2))
            b = int(SKY_MIDDLE[2] + (SKY_BOTTOM[2] - SKY_MIDDLE[2]) * ((ratio - 0.5) * 2))
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # 2. Soare (același cu raze animate)
    sun_x, sun_y = 150, 120
    sun_radius = 50

    import math
    time_offset = pygame.time.get_ticks() / 1000

    # raze animate
    for i in range(12):
        angle = (i * 30 + time_offset * 20) % 360
        rad = math.radians(angle)
        ray_length = 80 + math.sin(time_offset * 2 + i) * 10
        end_x = sun_x + math.cos(rad) * ray_length
        end_y = sun_y + math.sin(rad) * ray_length
        pygame.draw.line(screen, (255, 240, 150),
                         (sun_x, sun_y),
                         (int(end_x), int(end_y)), 3)

    # glow
    for i in range(5, 0, -1):
        alpha = 40 * i
        glow_surf = pygame.Surface((sun_radius * 2 + i * 20, sun_radius * 2 + i * 20), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 220, 100, alpha),
                           (sun_radius + i * 10, sun_radius + i * 10),
                           sun_radius + i * 10)
        screen.blit(glow_surf, (sun_x - sun_radius - i * 10, sun_y - sun_radius - i * 10))

    pygame.draw.circle(screen, (255, 230, 120), (sun_x, sun_y), sun_radius)
    pygame.draw.circle(screen, (255, 245, 180), (sun_x, sun_y), sun_radius - 15)

    # 3. Funcție nori
    def draw_cloud(x, y, scale=1.0, alpha=180):
        cloud_surf = pygame.Surface((int(140 * scale), int(70 * scale)), pygame.SRCALPHA)
        cloud_color = (255, 255, 255, alpha)

        pygame.draw.circle(cloud_surf, cloud_color,
                           (int(25 * scale), int(45 * scale)), int(20 * scale))
        pygame.draw.circle(cloud_surf, cloud_color,
                           (int(45 * scale), int(35 * scale)), int(25 * scale))
        pygame.draw.circle(cloud_surf, cloud_color,
                           (int(70 * scale), int(30 * scale)), int(30 * scale))
        pygame.draw.circle(cloud_surf, cloud_color,
                           (int(95 * scale), int(35 * scale)), int(25 * scale))
        pygame.draw.circle(cloud_surf, cloud_color,
                           (int(115 * scale), int(45 * scale)), int(20 * scale))

        screen.blit(cloud_surf, (int(x), int(y)))

    # 4. Update și desenare nori animați
    for cloud in cloud_positions:
        # mișcare
        cloud['x'] += cloud['speed']

        # wrap around (când iese din ecran, reapare în stânga)
        if cloud['x'] > SCREEN_WIDTH + 150:
            cloud['x'] = -150

        # desenare
        draw_cloud(cloud['x'], cloud['y'], cloud['scale'], cloud['alpha'])

def draw_spotlight_darkness(screen, firefly, screen_movement):
    """intuneric cu spotlight doar in jurul firefly-ului - PROGRESIV"""

    # darkness incepe doar cand lumina scade sub 80%
    if firefly.light_level >= 80:
        return  # nu desenam nimic, totul vizibil!

    # calculam cat de intunecat trebuie sa fie
    # la 80% light = 0% darkness
    # la 0% light = 100% darkness
    darkness_intensity = (80 - firefly.light_level) / 80  # 0.0 la 1.0

    # creăm suprafață neagră
    darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    max_darkness_alpha = int(220 * darkness_intensity)  # maxim 220 alpha
    darkness.fill((0, 0, 0, max_darkness_alpha))

    # calculăm poziția firefly pe ecran
    firefly_screen_x = firefly.x - screen_movement + firefly.width // 2
    firefly_screen_y = firefly.y + firefly.height // 2

    # calculăm raza spotlight-ului
    max_radius = SPOTLIGHT_RADIUS
    min_radius = 100
    light_ratio = firefly.light_level / MAX_LIGHT
    current_radius = int(min_radius + (max_radius - min_radius) * light_ratio)

    # creăm gradient circular pentru spotlight (zona vizibilă)
    spotlight_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    for radius in range(current_radius, 0, -10):
        # alpha scade de la centru spre margine
        alpha = int(max_darkness_alpha * (1 - (radius / current_radius) ** 2))
        pygame.draw.circle(spotlight_surface, (0, 0, 0, alpha),
                           (int(firefly_screen_x), int(firefly_screen_y)),
                           radius)

    # aplicam darkness cu spotlight "cut out"
    screen.blit(darkness, (0, 0))
    screen.blit(spotlight_surface, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)


def draw_ui(screen, firefly, level_id):
    """desenam UI (health bar pentru lumina) - vizibilitate îmbunătățită"""
    # light bar background
    bar_x, bar_y = 20, 20
    bar_width, bar_height = 250, 35

    # shadow pentru bar (adâncime)
    pygame.draw.rect(screen, (0, 0, 0, 100),
                     (bar_x + 2, bar_y + 2, bar_width + 4, bar_height + 4),
                     border_radius=5)

    pygame.draw.rect(screen, (50, 50, 50),
                     (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4),
                     border_radius=5)
    pygame.draw.rect(screen, (30, 30, 30),
                     (bar_x, bar_y, bar_width, bar_height),
                     border_radius=5)

    # light bar fill
    fill_width = int((firefly.light_level / MAX_LIGHT) * bar_width)

    # culoare in functie de cat de mult e
    if firefly.light_level > 60:
        bar_color = YELLOW
    elif firefly.light_level > 30:
        bar_color = ORANGE
    else:
        bar_color = (255, 100, 100)

    if fill_width > 0:
        pygame.draw.rect(screen, bar_color,
                         (bar_x, bar_y, fill_width, bar_height),
                         border_radius=5)

    # text cu contrast maxim - shadow + culoare adaptivă
    # shadow negru
    light_shadow = font_small.render(f"Light: {int(firefly.light_level)}", True, BLACK)
    screen.blit(light_shadow, (bar_x + 11, bar_y + 5))

    # text principal - negru când bara e plină, alb când e goală
    if firefly.light_level > 50:
        text_color = BLACK
    else:
        text_color = WHITE

    light_text = font_small.render(f"Light: {int(firefly.light_level)}", True, text_color)
    screen.blit(light_text, (bar_x + 10, bar_y + 4))

    # form indicator - mai contrastant
    form_x = SCREEN_WIDTH - 200
    form_y = 20

    form_bg_color = YELLOW if firefly.form == "light" else SHADOW_PURPLE

    # shadow pentru form indicator
    pygame.draw.rect(screen, (0, 0, 0, 100),
                     (form_x + 2, form_y + 2, 180, 43),
                     border_radius=8)

    pygame.draw.rect(screen, (50, 50, 50),
                     (form_x - 3, form_y - 3, 180, 43),
                     border_radius=8)
    pygame.draw.rect(screen, form_bg_color,
                     (form_x, form_y, 174, 37),
                     border_radius=8)

    form_text_str = "* LIGHT" if firefly.form == "light" else "~ SHADOW"
    form_text_color = BLACK if firefly.form == "light" else WHITE

    # shadow pentru text
    form_shadow = font_small.render(form_text_str, True, BLACK if firefly.form == "shadow" else (200, 200, 200))
    screen.blit(form_shadow, (form_x + 16, form_y + 5))

    form_text = font_small.render(form_text_str, True, form_text_color)
    screen.blit(form_text, (form_x + 15, form_y + 4))

    # level indicator - cu shadow
    level_shadow = font_small.render(f"Level {level_id}/4", True, BLACK)
    screen.blit(level_shadow, (SCREEN_WIDTH // 2 - 49, 26))

    level_text = font_small.render(f"Level {level_id}/4", True, WHITE)
    screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 25))

    # instructiuni - cu shadow pentru vizibilitate
    inst_color = WHITE
    inst_text_str = "← → Move | SPACE Jump | S Switch Form"

    inst_shadow = font_small.render(inst_text_str, True, BLACK)
    screen.blit(inst_shadow, (21, SCREEN_HEIGHT - 39))

    inst_text = font_small.render(inst_text_str, True, inst_color)
    screen.blit(inst_text, (20, SCREEN_HEIGHT - 40))

    # warning daca lumina e scazuta
    if firefly.light_level < 40 and firefly.light_level > 0:
        warning_alpha = int(150 + 105 * math.sin(pygame.time.get_ticks() / 200))
        warning_color = (255, 100, 100)

        warning_surface = pygame.Surface((SCREEN_WIDTH, 80), pygame.SRCALPHA)
        warning_surface.fill((0, 0, 0, 150))
        screen.blit(warning_surface, (0, SCREEN_HEIGHT // 2 - 40))

        # shadow pentru warning
        warning_shadow = font_medium.render("!!! LOW LIGHT! FIND ORBS !!!", True, BLACK)
        screen.blit(warning_shadow, (SCREEN_WIDTH // 2 - 219, SCREEN_HEIGHT // 2 - 19))

def update_camera(firefly, screen_movement, level_width):
    """update camera position pentru scrolling"""
    # camera urmareste playerul
    target_screen_movement = firefly.x - CAMERA_OFFSET_X

    # limitam camera
    if target_screen_movement < 0:
        target_screen_movement = 0
    if target_screen_movement > level_width - SCREEN_WIDTH:
        target_screen_movement = level_width - SCREEN_WIDTH

    # smooth camera (lerp)
    screen_movement += (target_screen_movement - screen_movement) * 0.1

    return screen_movement


# particule pentru intro
intro_particles = []
for _ in range(50):
    import random
    intro_particles.append({
        'x': random.randint(0, SCREEN_WIDTH),
        'y': random.randint(0, SCREEN_HEIGHT),
        'speed': random.uniform(0.3, 1.0),
        'size': random.randint(2, 5),
        'brightness': random.randint(100, 200)
    })

def update_intro_particles():
    """update particule pentru intro"""
    for particle in intro_particles:
        particle['y'] -= particle['speed']
        if particle['y'] < 0:
            particle['y'] = SCREEN_HEIGHT
            particle['x'] = __import__('random').randint(0, SCREEN_WIDTH)

def draw_intro_screen(screen):
    """ecran de intro/start - mai frumos!"""
    # background gradient
    draw_gradient_background(screen)

    # particule plutitoare
    update_intro_particles()
    for particle in intro_particles:
        color = (particle['brightness'], particle['brightness'], particle['brightness'])
        pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), particle['size'])

    # overlay semi-transparent
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0, 0))

    # animatie de pulsare
    time_ms = pygame.time.get_ticks()
    pulse = abs(math.sin(time_ms / 400)) * 0.2 + 0.8
    glow_pulse = abs(math.sin(time_ms / 300)) * 15 + 35

    # titlu principal - CENTRAT
    title_text = font_large.render("SHADOW SWITCH", True, YELLOW)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 180))

    # glow pentru titlu
    glow_surface = pygame.Surface((title_rect.width + 40, title_rect.height + 40), pygame.SRCALPHA)
    for i in range(20, 0, -4):
        alpha = int(80 * (i / 20) * pulse)
        glow_color = (*YELLOW[:3], alpha)
        glow_rect = pygame.Rect(20 - i, 20 - i, title_rect.width + i * 2, title_rect.height + i * 2)
        pygame.draw.rect(glow_surface, glow_color, glow_rect, border_radius=10)
    screen.blit(glow_surface, (title_rect.x - 20, title_rect.y - 20))
    screen.blit(title_text, title_rect)

    # subtitlu - CENTRAT
    subtitle_text = font_medium.render("Firefly's Journey", True, (200, 200, 255))
    subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 260))
    screen.blit(subtitle_text, subtitle_rect)

    # separator line
    pygame.draw.line(screen, (100, 150, 200),
                     (SCREEN_WIDTH // 2 - 200, 300),
                     (SCREEN_WIDTH // 2 + 200, 300), 3)

    # licurici animat in centru - mai mare si mai frumos
    firefly_y = 370

    # glow mare
    for radius in range(int(glow_pulse + 40), int(glow_pulse), -8):
        alpha = int(100 * ((radius - glow_pulse) / 40))
        glow_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*YELLOW[:3], alpha), (radius, radius), radius)
        screen.blit(glow_surf, (SCREEN_WIDTH // 2 - radius, firefly_y - radius))

    # corp licurici
    firefly_radius = 25
    pygame.draw.circle(screen, YELLOW, (SCREEN_WIDTH // 2, firefly_y), firefly_radius)

    # ochi
    eye_y = firefly_y - 5
    pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH // 2 - 10, eye_y), 5)
    pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH // 2 + 10, eye_y), 5)
    pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2 - 9, eye_y - 1), 2)
    pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2 + 11, eye_y - 1), 2)

    # instructiuni - CENTRATE si mai spatiate
    inst_y_start = 470
    inst_spacing = 50

    inst1 = font_small.render("Collect light orbs to survive", True, (220, 220, 220))
    inst1_rect = inst1.get_rect(center=(SCREEN_WIDTH // 2, inst_y_start))
    screen.blit(inst1, inst1_rect)

    inst2 = font_small.render("Switch forms to pass barriers", True, (220, 220, 220))
    inst2_rect = inst2.get_rect(center=(SCREEN_WIDTH // 2, inst_y_start + inst_spacing))
    screen.blit(inst2, inst2_rect)

    inst3 = font_small.render("Reach the finish portal!", True, (220, 220, 220))
    inst3_rect = inst3.get_rect(center=(SCREEN_WIDTH // 2, inst_y_start + inst_spacing * 2))
    screen.blit(inst3, inst3_rect)

    # buton start - CENTRAT cu animatie pulsanta
    start_pulse = abs(math.sin(time_ms / 350))
    start_scale = 1.0 + start_pulse * 0.1

    # background pentru buton
    button_width = 450
    button_height = 70
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2,
                              SCREEN_HEIGHT - 120,
                              button_width, button_height)

    # glow pentru buton
    glow_color = (*GREEN[:3], int(100 + 100 * start_pulse))
    for i in range(10, 0, -2):
        glow_rect = button_rect.inflate(i * 4, i * 4)
        pygame.draw.rect(screen, (*GREEN[:3], int(30 * (i / 10))), glow_rect, border_radius=15)

    # buton fundal
    pygame.draw.rect(screen, (50, 150, 100), button_rect, border_radius=12)
    pygame.draw.rect(screen, GREEN, button_rect, 4, border_radius=12)

    # text start - CENTRAT
    start_text = font_medium.render("PRESS SPACE TO START", True, WHITE)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 85))
    screen.blit(start_text, start_rect)


# GAME LOOP
running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # INTRO SCREEN
        if show_intro:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_intro = False  # incepe jocul!

        # GAMEPLAY
        elif not game_over and not win and not level_complete:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    firefly.jump()
                    if jump_sound:
                        jump_sound.play()
                if event.key == pygame.K_s:
                    firefly.switch_form()

        # RESTART / NEXT LEVEL
        elif game_over or level_complete:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # restart level
                    current_level = level_manager.load_level(level_manager.current_level_id)
                    firefly = Firefly(100, GROUND_LEVEL - 50)
                    screen_movement = 0
                    game_over = False
                    level_complete = False
                    death_by_spike = False
                    death_by_enemy = False

                if event.key == pygame.K_n and level_complete:
                    # next level
                    next_level = level_manager.next_level()
                    if next_level:
                        current_level = next_level
                        firefly = Firefly(100, GROUND_LEVEL - 50)
                        screen_movement = 0
                        level_complete = False
                    else:
                        win = True

        # WIN SCREEN
        elif win:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # restart from level 1
                    level_manager = LevelManager()
                    current_level = level_manager.current_level
                    firefly = Firefly(100, GROUND_LEVEL - 50)
                    screen_movement = 0
                    game_over = False
                    win = False
                    level_complete = False
                    death_by_spike = False
                    death_by_enemy = False
                    show_intro = True  # arata intro din nou

    if not game_over and not win and not level_complete:
        keys = pygame.key.get_pressed()
        firefly.move(keys, current_level.width)
        firefly.apply_gravity(GROUND_LEVEL)
        # UPDATE MOVING PLATFORMS - ADAUGĂ ASTA!
        for platform in current_level.moving_platforms:
            platform.update()
        # UPDATE ENEMIES
        for enemy in current_level.enemies:
            enemy.update()

        # verificam coliziuni cu platforme (normale + mobile)
        all_platforms = current_level.platforms + current_level.moving_platforms
        firefly.check_platform_collision(all_platforms)

        # verificam daca e in shadow zone - forteaza shadow form
        in_shadow_zone = False
        for zone in current_level.shadow_zones:
            if zone.contains_player(firefly):
                firefly.force_shadow_form()
                in_shadow_zone = True
                break

        firefly.update_light(dt * FPS)

        # colecteaza orbs
        for orb in current_level.light_orbs:
            orb.update()
            if orb.check_collision(firefly):
                firefly.collect_light(LIGHT_ORB_VALUE)
                if collect_sound:
                    collect_sound.play()

        # verificam coliziune cu form barriers
        firefly_rect = firefly.get_rect()
        for barrier in current_level.form_barriers:
            if firefly_rect.colliderect(barrier.get_rect()):
                if not barrier.can_pass(firefly.form):
                    # blocam playerul
                    if firefly.x < barrier.x:
                        firefly.x = barrier.x - firefly.width
                    else:
                        firefly.x = barrier.x + barrier.width

        # verificam coliziune cu hazards
        death_by_spike = False
        for hazard in current_level.hazards:
            if firefly_rect.colliderect(hazard.get_rect()):
                game_over = True
                death_by_spike = True  # marcam ca a murit de spike
                if death_sound:
                    death_sound.play()
                break

        # verificam coliziune cu inamici
        for enemy in current_level.enemies:
            if firefly_rect.colliderect(enemy.get_rect()):
                game_over = True
                death_by_enemy = True
                death_by_spike = False  # moarte de inamic
                if death_sound:
                    death_sound.play()
                break

        # game over daca nu mai are lumina
        if firefly.light_level <= 0:
            game_over = True
            if death_sound:
                death_sound.play()

        # verificam daca a ajuns la finish
            # verificam daca a ajuns la finish
        if firefly_rect.colliderect(current_level.get_finish_rect()):
            # daca e ultimul nivel, direct WIN
            if level_manager.current_level_id == 4:
                win = True
                if win_sound:
                    win_sound.play()
            else:
                level_complete = True
                if win_sound:
                    win_sound.play()

        # update camera
        screen_movement = update_camera(firefly, screen_movement, current_level.width)

        # update portal
        current_level.portal.update()

    # DESENAM TOTUL
    draw_background_with_decorations(screen)

    # ground line
    pygame.draw.line(screen, (80, 80, 80),
                     (0, GROUND_LEVEL),
                     (SCREEN_WIDTH, GROUND_LEVEL), 3)

    # desenam shadow zones
    for zone in current_level.shadow_zones:
        zone.draw(screen, screen_movement)

    # desenam platforme
    for platform in current_level.platforms:
        platform.draw(screen, screen_movement)

    # desenam moving platforms
    for platform in current_level.moving_platforms:
        platform.draw(screen, screen_movement)

    # desenam form barriers
    for barrier in current_level.form_barriers:
        barrier.draw(screen, screen_movement)

    # desenam hazards
    for hazard in current_level.hazards:
        hazard.draw(screen, screen_movement)

    # desenam inamici
    for enemy in current_level.enemies:
        enemy.draw(screen, screen_movement)

    # desenam orbs
    for orb in current_level.light_orbs:
        orb.draw(screen, screen_movement)

    # desenam portal (finish)
    current_level.portal.draw(screen, screen_movement)

    # desenam firefly
    firefly.draw(screen, screen_movement)

    # SPOTLIGHT DARKNESS - doar daca nu e game over/win
    if not game_over and not win and not level_complete:
        draw_spotlight_darkness(screen, firefly, screen_movement)

    # UI
    draw_ui(screen, firefly, level_manager.current_level_id)

    # SCREENS

    if game_over:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        # mesaj diferit in functie de cum ai murit
        if death_by_spike:
            death_text = font_large.render("OUCH! SPIKE TRAP!", True, (255, 100, 100))
        elif death_by_enemy:
            death_text = font_large.render("CAUGHT BY ENEMY!", True, (255, 100, 100))
        else:
            death_text = font_large.render("DARKNESS CONSUMED YOU", True, (255, 100, 100))

        restart_text = font_medium.render("Press R to Restart", True, WHITE)

        # centrare cu get_rect
        death_rect = death_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))

        screen.blit(death_text, death_rect)
        screen.blit(restart_text, restart_rect)

    if level_complete and not win:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 200, 180))
        screen.blit(overlay, (0, 0))

        complete_text = font_large.render(f"LEVEL {level_manager.current_level_id} COMPLETE!", True, GREEN)
        next_text = font_medium.render("Press N for Next Level", True, BLACK)
        restart_text = font_small.render("Press R to Restart", True, BLACK)
        # centrare
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))

        screen.blit(complete_text, complete_rect)
        screen.blit(next_text, next_rect)
        screen.blit(restart_text, restart_rect)

    if win:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 100, 200))
        screen.blit(overlay, (0, 0))

        # animatie de pulsare pentru text
        pulse = abs(math.sin(pygame.time.get_ticks() / 500)) * 0.3 + 0.7

        win_text = font_large.render("*** CONGRATULATIONS! ***", True, YELLOW)
        complete_text = font_medium.render("You've completed Shadow Switch!", True, BLACK)
        achievement_text = font_small.render("All 4 levels conquered", True, BLACK)
        restart_text = font_small.render("Press R to Play Again", True, BLACK)

        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        achievement_rect = achievement_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))

        screen.blit(win_text, win_rect)
        screen.blit(complete_text, complete_rect)
        screen.blit(achievement_text, achievement_rect)
        screen.blit(restart_text, restart_rect)

     # INTRO SCREEN - desenam peste tot
    if show_intro:
        draw_intro_screen(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()