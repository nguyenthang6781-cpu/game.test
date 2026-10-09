import pygame
import random

# ===============================
# 1) SETTINGS / CẤU HÌNH
# ===============================
WIDTH = 480
HEIGHT = 640
FPS = 60
GRAVITY = 0.42
FLAP_FORCE = -7.5
PIPE_WIDTH = 70
PIPE_GAP = 170
PIPE_SPEED = 2.4
PIPE_INTERVAL = 90
GROUND_HEIGHT = 90
BIRD_X = 100
BIRD_RADIUS = 18

BACKGROUND_COLOR = (135, 206, 235)
GROUND_COLOR = (100, 180, 60)
PIPE_COLOR = (30, 140, 60)
BIRD_COLOR = (255, 210, 0)
TEXT_COLOR = (255, 255, 255)

# ===============================
# 2) GAME OBJECTS / ĐỐI TƯỢNG GAME
# ===============================
class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = HEIGHT // 2
        self.velocity = 0.0
        self.radius = BIRD_RADIUS

    def flap(self):
        self.velocity = FLAP_FORCE

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, screen):
        pygame.draw.circle(screen, BIRD_COLOR, (int(self.x), int(self.y)), self.radius)


class Pipe:
    def __init__(self):
        self.width = PIPE_WIDTH
        self.x = WIDTH + 50
        self.space_top = random.randint(80, HEIGHT - GROUND_HEIGHT - PIPE_GAP - 80)
        self.gap_y = self.space_top + PIPE_GAP
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, 0, self.width, self.space_top))
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, self.gap_y, self.width, HEIGHT - GROUND_HEIGHT - self.gap_y))


# ===============================
# 3) GAME LOGIC / LOGIC GAME
# ===============================
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird - One File")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 36)

        self.running = True
        self.game_over = False
        self.score = 0
        self.bird = Bird()
        self.pipes = []
        self.pipe_timer = 0

    def reset(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird()
        self.pipes = []
        self.pipe_timer = 0

    def spawn_pipe(self):
        self.pipes.append(Pipe())

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset()
                    self.bird.flap()

    def update(self):
        if self.game_over:
            return

        self.bird.update()

        self.pipe_timer += 1
        if self.pipe_timer >= PIPE_INTERVAL:
            self.spawn_pipe()
            self.pipe_timer = 0

        for pipe in self.pipes:
            pipe.update()
            if not pipe.passed and pipe.x + PIPE_WIDTH < BIRD_X:
                pipe.passed = True
                self.score += 1

        self.pipes = [pipe for pipe in self.pipes if pipe.x + PIPE_WIDTH > -10]

        if self.bird.y <= 0:
            self.game_over = True
        if self.bird.y + self.bird.radius >= HEIGHT - GROUND_HEIGHT:
            self.game_over = True

        for pipe in self.pipes:
            if (
                self.bird.x + self.bird.radius > pipe.x
                and self.bird.x - self.bird.radius < pipe.x + pipe.width
                and (
                    self.bird.y - self.bird.radius < pipe.space_top
                    or self.bird.y + self.bird.radius > pipe.gap_y
                )
            ):
                self.game_over = True

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        for pipe in self.pipes:
            pipe.draw(self.screen)

        self.bird.draw(self.screen)

        pygame.draw.rect(self.screen, GROUND_COLOR, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        label = self.font.render(str(self.score), True, TEXT_COLOR)
        self.screen.blit(label, (WIDTH // 2 - 10, 20))

        if self.game_over:
            game_over_text = self.font.render("Game Over", True, TEXT_COLOR)
            self.screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 40))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_input()
            self.update()
            self.draw()

        pygame.quit()


# ===============================
# 4) ENTRY POINT / ĐIỂM VÀO CHƯƠNG TRÌNH
# ===============================
if __name__ == "__main__":
    game = Game()
    game.run()
