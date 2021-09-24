import pygame, sys, random

# Set up-------------------------------------------------------------------------------------------------------
pygame.mixer.pre_init(44100, -16, 2, 512)
screen_size = (800, 600)
pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Ping Pong - Made by LEANH")
fpsClock = pygame.time.Clock()

# Game rect-------------------------------------------------------------------------------------------------------
player = pygame.Rect(screen_size[0] - 15, screen_size[1] / 2 - 70, 10, 115)
ball = pygame.Rect(screen_size[0] / 2 - 15, screen_size[1] / 2 - 15, 25, 25)
opponent = pygame.Rect(5, screen_size[1] / 2 - 70, 10, 115)

# Game variable---------------------------------------------------------------------------------------------------------------------------
GREY = (200, 200, 200)

ball_speed_x = 6 * random.choice((1, -1))
ball_speed_y = 6 * random.choice((1, -1))
player_speed = 0
opponent_speed  = 6

# Text-----------------------------------------------------------------------------------------------------------------------------
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("04B_19.TTF", 30)

# Score timer-------------------------------------------------------------------------------------------------------------------------------
score_time = True 

# Sound---------------------------------------------------------------------------------------------------------------------------
pong_sound = pygame.mixer.Sound("sound/pong.ogg")
score_sound = pygame.mixer.Sound("sound/score.ogg")


def ball_animation(): 
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_size[1]:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1
    
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()
    
    if ball.right >= screen_size[0]:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()
    
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_size[1]:
        player.bottom = screen_size[1]

def opponent_bot():
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_size[1]:
        opponent.bottom = screen_size[1]
    
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

def reset():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()

    ball.center = (screen_size[0] / 2, screen_size[1] / 2)   

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_x = 6 * random.choice((1, -1))
        ball_speed_y = 6 * random.choice((1, -1))
        score_time = None

    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))
    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 6
            if event.key == pygame.K_DOWN:
                player_speed += 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 6
            if event.key == pygame.K_DOWN:
                player_speed -= 6

    # Logic---------------------------------------------------------------------------------------------------------------------------
    ball_animation()
    player_animation()
    opponent_bot()
    
    # Draw--------------------------------------------------------------------------------------------------------------------------------
    screen.fill(pygame.Color('#2F373F'))
    pygame.draw.rect(screen, GREY, player)
    pygame.draw.rect(screen, GREY, opponent)
    pygame.draw.ellipse(screen, GREY, ball)
    pygame.draw.aaline(screen, GREY, (screen_size[0] / 2, 0), (screen_size[0] / 2, screen_size[1]))

    if score_time:
        reset()

    player_text  = game_font.render(f"{player_score}", False, GREY)
    screen.blit(player_text, (420, 280))
    
    opponent_text  = game_font.render(f"{opponent_score}", False, GREY)
    screen.blit(opponent_text, (365, 280))

    # Updating the window------------------------------------------------------------------------------------------------------
    pygame.display.update()
    fpsClock.tick(60)
