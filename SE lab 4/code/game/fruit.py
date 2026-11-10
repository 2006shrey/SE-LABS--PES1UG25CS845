
import random
import pygame


class Fruit:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.radius = 14
        self.x = random.randint(30, screen_width - 30)
        self.y = -self.radius * 2
        self.base_speed = random.uniform(4.0, 6.5)
        self.speed = self.base_speed

        # Choose the type of falling object
        self.kind = random.choices(
            ["normal", "rotten", "bomb"],
            weights=[70, 15, 15],
            k=1
        )[0]

        if self.kind == "normal":
            self.color = random.choice([
                (230, 45, 45),    # Apple
                (245, 140, 30),   # Orange
                (160, 60, 200),   # Grape
            ])
        elif self.kind == "rotten":
            self.color = (90, 110, 35)  # Rotten fruit
        else:
            self.color = (25, 25, 25)   # Bomb

    def update(self, speed_multiplier=1.0):
        self.y += self.speed * speed_multiplier

    def is_missed(self, screen_height):
        return self.y > screen_height

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def render(self, surface):
        center = (int(self.x), int(self.y))

        pygame.draw.circle(
            surface, self.color, center, self.radius
        )

        if self.kind == "normal":
            pygame.draw.circle(
                surface,
                (255, 255, 255),
                (int(self.x - 4), int(self.y - 4)),
                3
            )

        elif self.kind == "rotten":
            pygame.draw.circle(
                surface,
                (45, 55, 20),
                center,
                5
            )
            pygame.draw.circle(
                surface,
                (200, 200, 100),
                (int(self.x + 5), int(self.y - 4)),
                3
            )

        elif self.kind == "bomb":
            pygame.draw.circle(
                surface,
                (220, 40, 40),
                (int(self.x), int(self.y - self.radius - 3)),
                4
            )
            pygame.draw.line(
                surface,
                (255, 180, 40),
                (int(self.x), int(self.y - self.radius - 3)),
                (int(self.x + 5), int(self.y - self.radius - 9)),
                2
            )
