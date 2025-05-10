import pygame
import random
import os

# init
pygame.init()

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
GROUND_HEIGHT = 50
FPS = 60
FRAME_W, FRAME_H = 40, 40

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rectangle with spikes is lava")

# create animation frames
frames = []
for i in range(4):
    frame = pygame.Surface((FRAME_W, FRAME_H), pygame.SRCALPHA)
    pygame.draw.rect(frame, BLACK, (0, 0, FRAME_W, FRAME_H))
    if i % 2 == 0:
        pygame.draw.line(frame, WHITE, (10, 10), (30, 10), 2)  # eye
        pygame.draw.line(frame, WHITE, (5, 20), (35, 20), 2)   # mouth
    else:
        pygame.draw.line(frame, WHITE, (10, 15), (30, 15), 2)  # eye
        pygame.draw.line(frame, WHITE, (5, 25), (35, 25), 2)   # mouth
    frames.append(frame)

class Dino:
    def __init__(self):
        # position and size
        self.x = 50
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - FRAME_H
        self.width = FRAME_W
        self.height = FRAME_H
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # jump physics
        self.jumping = False
        self.jump_velocity = 0
        self.gravity = 0.8
        self.jump_strength = -15
        
        # animation
        self.current_frame = 0
        self.animation_delay = 80
        self.last_update = pygame.time.get_ticks()

    def jump(self):
        if not self.jumping:
            self.jump_velocity = self.jump_strength
            self.jumping = True

    def update(self):
        # handle jumping
        if self.jumping:
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity
            if self.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.height:
                self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
                self.jumping = False
                self.jump_velocity = 0
        self.rect.y = self.y

        # update animation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.last_update = current_time

    def draw(self, screen):
        screen.blit(frames[self.current_frame], (self.x, self.y))

class Cactus:
    def __init__(self):
        # position and size
        self.width = 20
        self.height = random.randint(30, 50)  # random height between 30 and 50
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # movement
        self.speed = 5

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self, screen):
        # draw main body
        pygame.draw.rect(screen, BLACK, self.rect)
        
        # draw spikes
        spike_height = 5
        # left side spikes
        for i in range(3):
            spike_y = self.y + (i * (self.height // 3))
            pygame.draw.polygon(screen, BLACK, [
                (self.x, spike_y),
                (self.x - 5, spike_y + spike_height),
                (self.x, spike_y + spike_height * 2)
            ])
        
        # right side spikes
        for i in range(3):
            spike_y = self.y + (i * (self.height // 3))
            pygame.draw.polygon(screen, BLACK, [
                (self.x + self.width, spike_y),
                (self.x + self.width + 5, spike_y + spike_height),
                (self.x + self.width, spike_y + spike_height * 2)
            ])
        
        # top spikes
        for i in range(2):
            spike_x = self.x + (i * (self.width // 2))
            pygame.draw.polygon(screen, BLACK, [
                (spike_x, self.y),
                (spike_x + spike_height, self.y - 5),
                (spike_x + spike_height * 2, self.y)
            ])
        
        # bottom spikes
        for i in range(2):
            spike_x = self.x + (i * (self.width // 2))
            pygame.draw.polygon(screen, BLACK, [
                (spike_x, self.y + self.height),
                (spike_x + spike_height, self.y + self.height + 5),
                (spike_x + spike_height * 2, self.y + self.height)
            ])

class Game:
    def __init__(self):
        # setup
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
        
    def reset_game(self):
        # game objects
        self.dino = Dino()
        self.cacti = []
        
        # game state
        self.score = 0
        self.game_speed = 5
        self.spawn_timer = 0
        self.min_spawn_distance = 300
        self.max_spawn_distance = 600
        self.difficulty_timer = 0
        self.game_over = False

    def spawn_cactus(self):
        # calculate spawn distance based on score
        if self.score > 10:
            self.min_spawn_distance = max(200, 300 - (self.score * 5))
            self.max_spawn_distance = max(400, 600 - (self.score * 5))
        
        # random spawn distance
        spawn_distance = random.randint(self.min_spawn_distance, self.max_spawn_distance)
        
        # check if enough space for new cactus
        if len(self.cacti) == 0 or self.cacti[-1].x < SCREEN_WIDTH - spawn_distance:
            self.cacti.append(Cactus())

    def update(self):
        if self.game_over:
            return True

        # update dino
        self.dino.update()
        
        # spawn and update cacti
        self.spawn_timer += 1
        if self.spawn_timer >= 60:  # try to spawn every second
            self.spawn_cactus()
            self.spawn_timer = 0

        # update cacti and increase speed
        for cactus in self.cacti[:]:
            cactus.speed = self.game_speed + (self.score //5)  # increase speed every 5 points
            cactus.update()
            if cactus.x < -cactus.width:
                self.cacti.remove(cactus)
                self.score += 1

        # check collisions
        for cactus in self.cacti:
            if self.dino.rect.colliderect(cactus.rect):
                self.game_over = True
                return True
        return True

    def draw(self):
        # clear screen
        self.screen.fill(WHITE)
        
        # draw ground
        pygame.draw.line(self.screen, BLACK, (0, SCREEN_HEIGHT - GROUND_HEIGHT),
                        (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT), 2)
        
        # draw game objects
        self.dino.draw(self.screen)
        for cactus in self.cacti:
            cactus.draw(self.screen)

        # draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (625, 10))

        if self.game_over:
            self.draw_game_over()
        else:
            pygame.display.flip()

    def draw_game_over(self):
        # draw game over text
        game_over_text = self.font.render("Game Over!", True, BLACK)
        restart_text = self.font.render("Press R to Restart", True, BLACK)
        score_text = self.font.render(f"Final Score: {self.score}", True, BLACK)
        
        # center the text
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(score_text, score_rect)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over:
                        self.dino.jump()
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run() 