
import random
import pygame


class Particle:
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        self.color = color

        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-4, 1)
        self.radius = random.randint(2, 4)
        self.life = 30

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15
        self.life -= 1

    def render(self, surface):
        if self.life > 0:
            pygame.draw.circle(
                surface,
                self.color,
                (int(self.x), int(self.y)),
                self.radius
            )


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color):
        for _ in range(12):
            self.particles.append(
                Particle(x, y, color)
            )

    def update(self):
        for particle in self.particles[:]:
            particle.update()

            if particle.life <= 0:
                self.particles.remove(particle)

    def render(self, surface):
        for particle in self.particles:
            particle.render(surface)
