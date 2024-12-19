import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 700, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pygame Wing")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PAD_WIDTH, PAD_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont('comicsans', 40)
WINNING_SCORE = 10

class Paddle:
    COLOR = WHITE
    VEL = 4
    
    def __init__(self, x, y, width, height):
        self.x = self.ORIGINAL_x = x
        self.y = self.ORIGINAL_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
    
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.ORIGINAL_x
        self.y = self.ORIGINAL_y        

class Ball:
    MAX_VEL = 5
    COLOR = WHITE
    
    def __init__(self, x, y, radius):
        self.x = self.ORIGINAL_x = x
        self.y = self.ORIGINAL_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
        
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
    def reset(self):
        self.x = self.ORIGINAL_x
        self.y = self.ORIGINAL_y
        self.y_vel = 0
        self.x_vel *= -1

def draw(win, paddle1, paddle2, ball, score1, score2):
    win.fill(BLACK)
    paddle1.draw(win)
    paddle2.draw(win)
    ball.draw(win)
    
    score1_text = SCORE_FONT.render(str(score1), 1, WHITE)
    score2_text = SCORE_FONT.render(str(score2), 1, WHITE)
    
    win.blit(score1_text, (WIDTH//2 - 50, 50))
    win.blit(score2_text, (WIDTH//2 + 25, 50))
    
    for paddle in [paddle1, paddle2]:
        paddle.draw(win)
        
    for i in range(10, HEIGHT, 20):
        if i % 2 == 0:
            continue
        
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 2, i, 4, 10))
        
    ball.draw(win)
    
    pygame.display.update()
    
def handle(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    if ball.x - ball.radius <= 0: 
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                medell_y = (left_paddle.y + left_paddle.height) // 2
                difference_in_y = medell_y - ball.y
                reduction_factor = difference_in_y / (left_paddle.height // 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    elif ball.x + ball.radius >= WIDTH:  
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                medell_y = (right_paddle.y + right_paddle.height) // 2
                difference_in_y = medell_y - ball.y
                reduction_factor = difference_in_y / (right_paddle.height // 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height + left_paddle.VEL <= HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height + right_paddle.VEL <= HEIGHT:
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()
    
    left_paddle = Paddle(10, HEIGHT//2 - PAD_HEIGHT//2, PAD_WIDTH, PAD_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PAD_WIDTH, HEIGHT//2 - PAD_HEIGHT//2, PAD_WIDTH, PAD_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    
    score1 = 0
    score2 = 0
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        
        ball.move()
        handle(ball, left_paddle, right_paddle)
        
        if ball.x < 0:
            score2 += 1
            ball.reset()
        elif ball.x > WIDTH:
            score1 += 1
            ball.reset()
        
        draw(WIN, left_paddle, right_paddle, ball, score1, score2)
        
        if score1 >= WINNING_SCORE or score2 >= WINNING_SCORE:
            win_text = "Left Player Wins!" if score1 >= WINNING_SCORE else "Right Player Wins!"
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            score1 = 0
            score2 = 0
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()