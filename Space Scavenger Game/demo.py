import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Scavenger")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60

BACKGROUND_IMAGE = pygame.image.load("assets/background.jpg")
SPACESHIP_IMAGE = pygame.image.load("assets/spaceship.png")
ASTEROID_IMAGE = pygame.image.load("assets/asteroid.png")
CRYSTAL_IMAGE = pygame.image.load("assets/energy_crystal.png")

CRASH_SOUND = pygame.mixer.Sound("assets/clash_sound.wav")
pygame.mixer.music.load("assets/background_music.wav")

SPACESHIP = pygame.transform.scale(SPACESHIP_IMAGE, (80, 80))
ASTEROID = pygame.transform.scale(ASTEROID_IMAGE, (100, 100))
FLIPPED_ASTEROID = pygame.transform.flip(ASTEROID, True, False)
CRYSTAL = pygame.transform.scale(CRYSTAL_IMAGE, (60, 60))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

spaceship_rect = SPACESHIP.get_rect(center=(WIDTH // 2, HEIGHT - 100))

asteroids = []
crystals = []

spaceship_speed = 5
asteroid_speed = 2
crystal_speed = 2

asteroid_scale_factor = 1

score = 0
lives = 3


def create_asteroid():
    global asteroid_scale_factor

    from_left = random.choice([True, False])
    if from_left:
        x = random.randint(0, WIDTH // 2)
        horizontal_speed = random.uniform(2, 4)
    else:
        x = random.randint(WIDTH // 2, WIDTH - 60)
        horizontal_speed = -random.uniform(2, 4)

    y = random.randint(-100, -40)
    rect = ASTEROID.get_rect(topleft=(x, y))
    vertical_speed = random.uniform(2, 4)

    scaled_asteroid = pygame.transform.scale(ASTEROID,
    (int(100 * asteroid_scale_factor), int(100 * asteroid_scale_factor)))

    asteroids.append({
        "rect": rect,
        "horizontal_speed": horizontal_speed,
        "vertical_speed": vertical_speed,
        "from_left": from_left,
        "image": scaled_asteroid
    })

def create_crystal():
    x = random.randint(0, WIDTH - 30)
    y = random.randint(-100, -40)
    rect = CRYSTAL.get_rect(topleft=(x, y))
    crystals.append(rect)


def draw_objects():
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(SPACESHIP, spaceship_rect.topleft)

    # pygame.draw.rect(screen, (255, 0, 0), spaceship_rect, 2)

    for asteroid in asteroids:
        if asteroid["from_left"]:
            screen.blit(pygame.transform.flip(asteroid["image"], True, False), asteroid["rect"].topleft)
        else:
            screen.blit(asteroid["image"], asteroid["rect"].topleft)

        # pygame.draw.rect(screen, (0, 0, 255), asteroid["rect"], 2)

    for crystal in crystals:
        screen.blit(CRYSTAL, crystal.topleft)
    draw_score()
    draw_lives()

def draw_score():
    font = pygame.font.Font(None, 40)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_lives():
    font = pygame.font.Font(None, 40)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH - 120, 10))

def respawn_spaceship():
    global lives, spaceship_speed, asteroid_scale_factor
    if lives > 0:
        lives -= 1
        spaceship_rect.center = (WIDTH // 2, HEIGHT - 100)
        pygame.time.wait(1000)
        spaceship_speed += 0.05
        asteroid_scale_factor += 0.005
    else:
        game_over()

def main():
    global score, spaceship_speed, asteroid_speed, crystal_speed, asteroid_scale_factor, lives

    pygame.mixer.music.play(-1)
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship_rect.left > 0:
            spaceship_rect.x -= spaceship_speed
        if keys[pygame.K_RIGHT] and spaceship_rect.right < WIDTH:
            spaceship_rect.x += spaceship_speed
        if keys[pygame.K_UP] and spaceship_rect.top > 0:
            spaceship_rect.y -= spaceship_speed
        if keys[pygame.K_DOWN] and spaceship_rect.bottom < HEIGHT:
            spaceship_rect.y += spaceship_speed

        for asteroid in asteroids[:]:
            asteroid["rect"].x += asteroid["horizontal_speed"]
            asteroid["rect"].y += asteroid["vertical_speed"]

            if asteroid["rect"].top > HEIGHT or asteroid["rect"].right < 0 or asteroid["rect"].left > WIDTH:
                asteroids.remove(asteroid)

            if spaceship_rect.colliderect(asteroid["rect"]):
                CRASH_SOUND.play()
                asteroids.clear()
                respawn_spaceship()

        for crystal in crystals[:]:
            crystal.y += crystal_speed
            if crystal.top > HEIGHT:
                crystals.remove(crystal)
            if spaceship_rect.colliderect(crystal):
                crystals.remove(crystal)
                score += 10

        if score % 100 == 0 and score != 0:
            asteroid_speed += 0.1
            spaceship_speed += 0.005
            asteroid_scale_factor += 0.002

        if random.randint(1, 20) == 1:
            create_asteroid()
        if random.randint(1, 40) == 1:
            create_crystal()

        if score >= 1000:
            success_screen()
            return

        draw_objects()
        pygame.display.flip()
        clock.tick(FPS)


def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    score_font = pygame.font.Font(None, 40)
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text,
                (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


def success_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("SUCCESS!", True, WHITE)
    score_text = pygame.font.Font(None, 40).render(f"Score: {score}", True, WHITE)

    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()