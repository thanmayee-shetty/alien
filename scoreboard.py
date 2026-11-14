import os
import pygame
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """Display the classic arcade score, high score, level, and lives."""

    # Monochrome arcade palette.
    WHITE = (238, 245, 238)
    GREEN = (45, 255, 35)
    DIM_GREEN = (35, 95, 55)

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Load the same pixel font used by the retro menu, if available.
        font_path = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "fonts",
            "PressStart2P-Regular.ttf",
        )

        if os.path.exists(font_path):
            self.label_font = pygame.font.Font(font_path, 10)
            self.value_font = pygame.font.Font(font_path, 12)
            self.small_font = pygame.font.Font(font_path, 8)
        else:
            # Readable fallback if the optional pixel font is not installed.
            self.label_font = pygame.font.SysFont(
                "couriernew", 18, bold=True
            )
            self.value_font = pygame.font.SysFont(
                "couriernew", 20, bold=True
            )
            self.small_font = pygame.font.SysFont(
                "couriernew", 14, bold=True
            )

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Render the current score in arcade green."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"

        self.score_label_image = self.label_font.render(
            "SCORE", True, self.WHITE
        )
        self.score_image = self.value_font.render(
            score_str, True, self.GREEN
        )

        self.score_label_rect = self.score_label_image.get_rect()
        self.score_label_rect.left = self.screen_rect.left + 28
        self.score_label_rect.top = 14

        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.score_label_rect.right + 20
        self.score_rect.centery = self.score_label_rect.centery

    def prep_high_score(self):
        """Render the high score in the center of the HUD."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"

        self.high_score_label_image = self.label_font.render(
            "HI-SCORE", True, self.WHITE
        )
        self.high_score_image = self.value_font.render(
            high_score_str, True, self.GREEN
        )

        self.high_score_label_rect = self.high_score_label_image.get_rect()
        self.high_score_label_rect.centerx = self.screen_rect.centerx
        self.high_score_label_rect.top = 10

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.high_score_label_rect.bottom + 7

    def prep_level(self):
        """Render the current level below the high score."""
        level_str = f"LEVEL {self.stats.level:02d}"
        self.level_image = self.small_font.render(
            level_str, True, self.DIM_GREEN
        )

        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = self.screen_rect.centerx
        self.level_rect.top = self.high_score_rect.bottom + 3

    def prep_ships(self):
        """Create small green ship icons for the remaining lives."""
        self.ships = Group()

        # Create compact copies of the player sprite for the lives display.
        icon_width = 25
        icon_height = 14
        gap = 7

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.image = pygame.transform.scale(
                ship.image, (icon_width, icon_height)
            )
            ship.rect = ship.image.get_rect()

            ship.rect.left = (
                self.screen_rect.right
                - 28
                - (self.stats.ships_left - ship_number) * (icon_width + gap)
            )
            ship.rect.top = 18
            self.ships.add(ship)

        self.lives_label_image = self.label_font.render(
            "LIVES", True, self.WHITE
        )
        self.lives_label_rect = self.lives_label_image.get_rect()
        self.lives_label_rect.right = (
            self.screen_rect.right
            - 28
            - self.stats.ships_left * (icon_width + gap)
            - 12
        )
        self.lives_label_rect.centery = 22

    def check_high_score(self):
        """Update the high score when the current score exceeds it."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw the complete arcade HUD."""
        self.screen.blit(self.score_label_image, self.score_label_rect)
        self.screen.blit(self.score_image, self.score_rect)

        self.screen.blit(
            self.high_score_label_image, self.high_score_label_rect
        )
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        self.screen.blit(self.lives_label_image, self.lives_label_rect)
        self.ships.draw(self.screen)

        # Thin green separator beneath the HUD.
        pygame.draw.line(
            self.screen,
            self.DIM_GREEN,
            (self.screen_rect.left + 18, 60),
            (self.screen_rect.right - 18, 60),
            1,
        )
