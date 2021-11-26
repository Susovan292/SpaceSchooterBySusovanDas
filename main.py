import pygame
import os


FIRST_PLAYER_NAME = str(input("Enter First Player Name : "))
SECOND_PLAYER_NAME = str(input("Enter SECOND Player Name : "))

pygame.font.init()
pygame.mixer.init()


# WIDTH, HEIGHT = 900, 500
WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter By Susovan Das")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'BulletHit1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'GunFire.mp3'))
GUNLOADED_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'GunLoaded.mp3'))
BGM = pygame.mixer.Sound(os.path.join('Assets', 'BGM.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('Comicsans', 100)
FPS = 60
VEL = 10
BULLET_VEL = 40
MAX_BULLETS = 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 55
BULLET_WIDTH, BULLET_HEIGHT = 20, 5
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), True, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), True, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a]:  # yellow left
        yellow.x -= VEL
        if yellow.x <= 0:
            yellow.x = 0

    if key_pressed[pygame.K_d]:  # yellow right
        yellow.x += VEL
        if yellow.x >= BORDER.x - SPACESHIP_WIDTH:
            yellow.x = BORDER.x - SPACESHIP_WIDTH
    if key_pressed[pygame.K_w]:  # yellow up
        yellow.y -= VEL
        if yellow.y <= 0:
            yellow.y = 0
    if key_pressed[pygame.K_s]:  # yellow down
        yellow.y += VEL
        if yellow.y >= HEIGHT - SPACESHIP_HEIGHT:
            yellow.y = HEIGHT - SPACESHIP_HEIGHT


def red_handle_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT]:  # red left
        red.x -= VEL
        if red.x <= BORDER.x+10:
            red.x = BORDER.x+10

    if key_pressed[pygame.K_RIGHT]:  # red right
        red.x += VEL
        if red.x >= WIDTH - SPACESHIP_WIDTH:
            red.x = WIDTH - SPACESHIP_WIDTH
    if key_pressed[pygame.K_UP]:  # red up
        red.y -= VEL
        if red.y <= 0:
            red.y = 0
    if key_pressed[pygame.K_DOWN]:  # red down
        red.y += VEL
        if red.y >= HEIGHT - SPACESHIP_HEIGHT:
            red.y = HEIGHT - SPACESHIP_HEIGHT


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT//2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    GUNLOADED_SOUND.play()
    pygame.time.delay(1000)
    BGM.play()
    yellow = pygame.Rect(0, HEIGHT/2+SPACESHIP_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(WIDTH-SPACESHIP_WIDTH, HEIGHT/2+SPACESHIP_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and red_health >= 0 and yellow_health >= 0:

                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    BULLET_FIRE_SOUND.play()
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2-2,
                                         BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    BULLET_FIRE_SOUND.play()
                    bullet = pygame.Rect(red.x, red.y + yellow.height // 2 - 2,
                                         BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1
                yellow_health += 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                red_health += 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = FIRST_PLAYER_NAME+" Wins!"
        if yellow_health <= 0:
            winner_text = SECOND_PLAYER_NAME+" Wins!"

        key_pressed = pygame.key.get_pressed()
        yellow_handle_movement(key_pressed, yellow)
        red_handle_movement(key_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        if winner_text != "":
            draw_winner(winner_text)
            break
    
    pygame.quit()


if __name__ == "__main__":
    main()
