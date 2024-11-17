import pygame
import random

# initialize pygame
pygame.init()

# Set up display
width, height = 500, 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Define colors
white = (255, 255, 255)
pink = (255, 182, 193)
palevioletred = (219, 112, 147)

# Define constants
FPS = 30
gravity = 1
jump = 15
pipe_width = 70
pipe_gap = 150

# Load bird image
bird_img = pygame.Surface((30, 30))
bird_img.fill((199, 21, 133))

class Bird:
    def __init__(self):
        self.x = 100
        self.y = height // 2
        self.vel = 0
        self.rect = pygame.Rect(self.x, self.y, 30, 30)

    def update(self):
        self.vel += gravity
        self.y += self.vel
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        self.vel = -jump

    def draw(self, win):
        win.blit(bird_img, (self.x, self.y))

class Pipe:
    def __init__(self):
        self.x = width
        self.height = random.randint(50, height - pipe_gap - 50)
        self.top = pygame.Rect(self.x, 0, pipe_width, self.height)
        self.bottom = pygame.Rect(self.x, self.height + pipe_gap, pipe_width, height - self.height - pipe_gap)

    def update(self):
        self.x -= 5
        self.top.topleft = (self.x, 0)
        self.bottom.topleft = (self.x, self.height + pipe_gap)

    def draw(self, win):
        pygame.draw.rect(win, pink, self.top)
        pygame.draw.rect(win, pink, self.bottom)

def game_over(win, score):
    font_big = pygame.font.SysFont("arial", 72)
    font_small = pygame.font.SysFont("arial", 36)

    game_over_text = font_big.render("Game Over", True, palevioletred)
    score_text = font_big.render(f"Score: {score}", True, palevioletred)
    restart_text = font_small.render("Press any key to exit", True, palevioletred)

    win.fill(white)
    win.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 3))
    win.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))
    win.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 100))
    pygame.display.update()
    wait_for_exit()

def wait_for_exit():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def main():
    pygame.init()
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    font = pygame.font.SysFont("arial", 36)

    run = True
    while run:
        clock.tick(FPS)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        # Update bird
        bird.update()

        # Update pipes
        if pipes[-1].x < width // 2:
            pipes.append(Pipe())

        for pipe in pipes[:]:
            pipe.update()
            if pipe.x + pipe_width < 0:
                pipes.remove(pipe)
                score += 1

        # Check collisions
        for pipe in pipes:
            if bird.rect.colliderect(pipe.top) or bird.rect.colliderect(pipe.bottom):
                game_over(win, score)
                run = False

        if bird.y > height or bird.y < 0:
            game_over(win, score)
            run = False

        # Draw everything
        win.fill(white)
        bird.draw(win)
        for pipe in pipes:
            pipe.draw(win)
        score_text = font.render(f"Score: {score}", True, palevioletred)
        win.blit(score_text, (10, 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
