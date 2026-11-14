import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A classic green pixel-art player cannon."""

    _PATTERN = (
        "000000111111000000",
        "000011111111110000",
        "000111111111111000",
        "001111111111111100",
        "011111111111111110",
        "111111111111111111",
        "111111111111111111",
        "111111111111111111",
    )

    PIXEL_SIZE = 3
    SHIP_GREEN = (45, 255, 35)

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Build a crisp pixel-art sprite with a transparent background.
        self.image = self._create_image()
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    @classmethod
    def _create_image(cls):
        """Convert the ship's pixel pattern into a Pygame surface."""
        width = len(cls._PATTERN[0]) * cls.PIXEL_SIZE
        height = len(cls._PATTERN) * cls.PIXEL_SIZE
        image = pygame.Surface((width, height), pygame.SRCALPHA)

        for row_index, row in enumerate(cls._PATTERN):
            for column_index, pixel in enumerate(row):
                if pixel == "1":
                    pygame.draw.rect(
                        image,
                        cls.SHIP_GREEN,
                        (
                            column_index * cls.PIXEL_SIZE,
                            row_index * cls.PIXEL_SIZE,
                            cls.PIXEL_SIZE,
                            cls.PIXEL_SIZE,
                        ),
                    )

        return image

    def update(self):
        """Update the ship's position based on movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
