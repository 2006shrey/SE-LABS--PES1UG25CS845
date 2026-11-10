
import pygame
from game.basket import Basket
from game.fruit import Fruit
from game.particles import ParticleSystem


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.basket = Basket(width, height)
        self.fruits = []
        self.particle_system = ParticleSystem()

        self.score = 0
        self.lives = 3
        self.spawn_delay = 750
        self.min_spawn_delay = 250
        self.last_spawn_time = pygame.time.get_ticks()
        self.game_state = "PLAYING"

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 28)

    def handle_event(self, event):
        if self.game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

    def update(self):
        if self.game_state != "PLAYING":
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.basket.move_left()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.basket.move_right()

        self.particle_system.update()

        now = pygame.time.get_ticks()
    
# Increase difficulty as score increases
        difficulty_level = self.score // 5

        self.spawn_delay = max(
        self.min_spawn_delay,
        750 - (difficulty_level * 75)
        )

        if now - self.last_spawn_time >= self.spawn_delay:
            self.fruits.append(Fruit(self.width))
            self.last_spawn_time = now

        basket_rect = self.basket.rect

        speed_multiplier = 1 + (self.score // 5) * 0.1

        for fruit in self.fruits[:]:
            fruit.update(speed_multiplier)

            if basket_rect.colliderect(fruit.rect):
                                # Create splash particles when caught
                if fruit.kind != "bomb":
                    self.particle_system.emit(
                        fruit.x,
                        fruit.y,
                        fruit.color
                    )

                if fruit.kind == "normal":
                    self.score += 1

                else:
                    self.lives -= 1

                self.fruits.remove(fruit)

                if self.lives <= 0:
                    self.lives = 0
                    self.game_state = "GAME_OVER"
                    break

                continue

            if fruit.is_missed(self.height):
                                # Create splash particles when fruit hits the floor
                if fruit.kind != "bomb":
                    self.particle_system.emit(
                        fruit.x,
                        self.height - 25,
                        fruit.color
                    )

                # Missing a normal fruit costs one life.
                # Missing harmful objects has no penalty.
                if fruit.kind == "normal":
                    self.lives -= 1

                self.fruits.remove(fruit)

                if self.lives <= 0:
                    self.lives = 0
                    self.game_state = "GAME_OVER"
                    break

    def reset(self):
        self.basket = Basket(self.width, self.height)
        self.fruits.clear()
        self.score = 0
        self.lives = 3
        self.last_spawn_time = pygame.time.get_ticks()
        self.game_state = "PLAYING"

    def render(self, screen):
        screen.fill((28, 32, 40))

        ground_y = self.height - 25

        pygame.draw.rect(
            screen,
            (45, 50, 60),
            (0, ground_y, self.width, 25)
        )

        self.basket.render(screen)
        self.particle_system.render(screen)

        for fruit in self.fruits:
            fruit.render(screen)

        score_surf = self.font_medium.render(
            f"Score: {self.score}",
            True,
            (255, 220, 80)
        )
        screen.blit(score_surf, (25, 20))

        lives_surf = self.font_medium.render(
            f"Lives: {self.lives}",
            True,
            (240, 80, 80)
        )

        screen.blit(
            lives_surf,
            (self.width - lives_surf.get_width() - 25, 20)
        )

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render(
                "GAME OVER",
                True,
                (235, 70, 70)
            )

            screen.blit(
                over_surf,
                (
                    self.width // 2 - over_surf.get_width() // 2,
                    self.height // 2 - 40
                )
            )

            final_surf = self.font_medium.render(
                f"Final Score: {self.score}",
                True,
                (255, 255, 255)
            )

            screen.blit(
                final_surf,
                (
                    self.width // 2 - final_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )

            restart_surf = self.font_medium.render(
                "Press [R] to Play Again",
                True,
                (200, 200, 200)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    self.height // 2 + 50
                )
            )
