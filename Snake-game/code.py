import pygame
import time
import random

# Initialize pygame
pygame.init()

# Screen size
width = 600
height = 400

# Colors
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
white = (255, 255, 255)

# Snake block size & speed
block_size = 20
speed = 5

# Create screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Clock and font
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Score function
def your_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    screen.blit(value, [0, 0])

# Draw the snake
def draw_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], block, block])

# Game loop
def game_loop():
    game_over = False
    game_close = False

    x = width // 2
    y = height // 2

    x_change = 0
    y_change = 0

    snake = []
    length = 1

    food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0
    food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0

    while not game_over:

        while game_close:
            screen.fill(black)
            msg = font_style.render("You Lost! Press Q to Quit or C to Play Again", True, red)
            screen.blit(msg, [width / 6, height / 3])
            your_score(length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = block_size
                    x_change = 0

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += x_change
        y += y_change
        screen.fill(blue)
        pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])

        snake_head = [x, y]
        snake.append(snake_head)

        if len(snake) > length:
            del snake[0]

        for block in snake[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(block_size, snake)
        your_score(length - 1)

        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0
            length += 1

        clock.tick(speed)

    pygame.quit()
    quit()

game_loop()
