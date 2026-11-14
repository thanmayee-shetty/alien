
import random
import pygame


class RetroBackground:
    """Create a classic monochrome arcade background."""

    def __init__(self, screen_size):
        self.width, self.height = screen_size

        self.black = (0, 0, 0)
        self.green = (110, 255, 150)
        self.dim_green = (35, 95, 55)

        # Generate stars at random positions.
        self.stars = []

        for _ in range(90):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            speed = random.uniform(0.25, 1.0)

            self.stars.append([x, y, speed])

        # Pre-render CRT scanlines for better performance.
        self.scanlines = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA
        )

        for y in range(0, self.height, 4):
            pygame.draw.line(
                self.scanlines,
                (0, 0, 0, 45),
                (0, y),
                (self.width, y)
            )

    def update(self):
        """Move stars slowly down the screen."""

        for star in self.stars:
            star[1] += star[2]

            if star[1] >= self.height:
                star[1] = 0
                star[0] = random.randint(0, self.width)

    def draw(self, screen):
        """Draw the background and CRT effects."""

        screen.fill(self.black)

        for x, y, speed in self.stars:
            brightness = self.green if speed > 0.7 else self.dim_green

            pygame.draw.rect(
                screen,
                brightness,
                (int(x), int(y), 2, 2)
            )

        # CRT scanline effect.
        screen.blit(self.scanlines, (0, 0))

        # Subtle arcade screen border.
        pygame.draw.rect(
            screen,
            self.dim_green,
            screen.get_rect().inflate(-20, -20),
            2
        )
