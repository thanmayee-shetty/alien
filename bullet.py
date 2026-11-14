import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A small pixel projectile fired from the player's ship."""

    BULLET_WHITE = (238, 245, 238)
    BULLET_CORE = (255, 255, 255)

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Keep the original settings-based rectangle for collision detection.
        self.rect = pygame.Rect(
            0,
            0,
            self.settings.bullet_width,
            self.settings.bullet_height,
        )
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        self.y -= self.settings.bullet_speed
        self.rect.y = round(self.y)

    def draw_bullet(self):
        """Draw a crisp, narrow pixel projectile inside the existing hitbox."""
        # Keep the projectile visible even if the configured hitbox is narrow.
        center_x = self.rect.centerx
        top = self.rect.top
        width = self.rect.width
        height = self.rect.height

        # Bright tip.
        pygame.draw.rect(
            self.screen,
            self.BULLET_CORE,
            (center_x - 1, top, min(3, width), min(3, height)),
        )

        # Main shaft.
        shaft_top = top + min(3, height)
        shaft_height = max(1, height - 5)
        pygame.draw.rect(
            self.screen,
            self.BULLET_WHITE,
            (center_x, shaft_top, 1, shaft_height),
        )

        # Small side pixels give it a chunky arcade projectile silhouette.
        if width >= 3 and height >= 7:
            pygame.draw.rect(
                self.screen,
                self.BULLET_WHITE,
                (center_x - 1, top + height // 2, 1, 2),
            )
            pygame.draw.rect(
                self.screen,
                self.BULLET_WHITE,
                (center_x + 1, top + height // 2, 1, 2),
            )
