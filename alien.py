import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A classic arcade alien with a two-frame pixel animation."""

    # Each character represents one pixel: 1 = lit, 0 = transparent.
    # The two frames alternate the alien's legs for a walking animation.
    _FRAME_1 = (
        "000110000110",
        "000011001100",
        "000111111110",
        "001101101100",
        "011111111111",
        "110011110011",
        "110011110011",
        "000110000110",
    )

    _FRAME_2 = (
        "000110000110",
        "000011001100",
        "000111111110",
        "001101101100",
        "011111111111",
        "001100001100",
        "011001100110",
        "110000000011",
    )

    PIXEL_SIZE = 3
    ANIMATION_INTERVAL = 400  # milliseconds

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self._frames = (
            self._make_frame(self._FRAME_1),
            self._make_frame(self._FRAME_2),
        )
        self._frame_index = 0
        self._last_animation_time = pygame.time.get_ticks()

        # Use the first frame to establish the sprite's size and hitbox.
        self.image = self._frames[self._frame_index]
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    @classmethod
    def _make_frame(cls, pattern):
        """Convert a text pixel pattern into a transparent Pygame surface."""
        width = len(pattern[0]) * cls.PIXEL_SIZE
        height = len(pattern) * cls.PIXEL_SIZE
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        alien_white = (238, 245, 238)

        for row_index, row in enumerate(pattern):
            for column_index, pixel in enumerate(row):
                if pixel == "1":
                    pygame.draw.rect(
                        surface,
                        alien_white,
                        (
                            column_index * cls.PIXEL_SIZE,
                            row_index * cls.PIXEL_SIZE,
                            cls.PIXEL_SIZE,
                            cls.PIXEL_SIZE,
                        ),
                    )

        return surface

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (
            self.rect.right >= screen_rect.right
            or self.rect.left <= 0
        )

    def update(self):
        """Move the alien and animate its legs."""
        self.x += (
            self.settings.alien_speed
            * self.settings.fleet_direction
        )
        self.rect.x = round(self.x)

        # Change animation frame without slowing down the game loop.
        now = pygame.time.get_ticks()
        if now - self._last_animation_time >= self.ANIMATION_INTERVAL:
            self._frame_index = 1 - self._frame_index
            self.image = self._frames[self._frame_index]
            self._last_animation_time = now
