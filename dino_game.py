import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
GROUND_HEIGHT = 50
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

class Dino:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - 40
        self.width = 40
        self.height = 40
        self.jumping = False
        self.jump_velocity = 0
        self.gravity = 0.8
        self.jump_strength = -15
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def jump(self):
        if not self.jumping:
            self.jump_velocity = self.jump_strength
            self.jumping = True

    def update(self):
        if self.jumping:
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity

            if self.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.height:
                self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
                self.jumping = False
                self.jump_velocity = 0

        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

class Cactus:
    def __init__(self):
        self.width = 20
        self.height = 40
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chrome Dino Game")
        self.clock = pygame.time.Clock()
        self.dino = Dino()
        self.cacti = []
        self.score = 0
        self.game_speed = 5
        self.spawn_timer = 0
        self.font = pygame.font.Font(None, 36)

    def spawn_cactus(self):
        if len(self.cacti) == 0 or self.cacti[-1].x < SCREEN_WIDTH - 300:
            self.cacti.append(Cactus())

    def update(self):
        self.dino.update()
        
        # Spawn cacti
        self.spawn_timer += 1
        if self.spawn_timer >= 60:
            self.spawn_cactus()
            self.spawn_timer = 0

        # Update cacti
        for cactus in self.cacti[:]:
            cactus.update()
            if cactus.x < -cactus.width:
                self.cacti.remove(cactus)
                self.score += 1

        # Check collisions
        for cactus in self.cacti:
            if self.dino.rect.colliderect(cactus.rect):
                return False

        return True

    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw ground
        pygame.draw.line(self.screen, BLACK, (0, SCREEN_HEIGHT - GROUND_HEIGHT),
                        (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT), 2)
        
        # Draw game objects
        self.dino.draw(self.screen)
        for cactus in self.cacti:
            cactus.draw(self.screen)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.dino.jump()

            if not self.update():
                running = False

            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run() 