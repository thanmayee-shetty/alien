
import os
import pygame


class RetroMenu:
    """Draw the classic arcade main menu."""

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.green = (110, 255, 150)
        self.dim_green = (35, 95, 55)

        font_path = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "fonts",
            "PressStart2P-Regular.ttf"
        )

        if os.path.exists(font_path):
            self.title_font = pygame.font.Font(font_path, 42)
            self.menu_font = pygame.font.Font(font_path, 18)
            self.small_font = pygame.font.Font(font_path, 12)
        else:
            self.title_font = pygame.font.SysFont(
                "couriernew", 58, bold=True
            )
            self.menu_font = pygame.font.SysFont(
                "couriernew", 24, bold=True
            )
            self.small_font = pygame.font.SysFont(
                "couriernew", 17, bold=True
            )

        self.start_rect = pygame.Rect(
            0, 0,
            min(420, int(self.screen_rect.width * 0.55)),
            65
        )

        self.start_rect.center = (
            self.screen_rect.centerx,
            int(self.screen_rect.height * 0.70)
        )

        # Small pixel alien design.
        self.alien_pattern = [
            "00100100",
            "00011000",
            "00111100",
            "01111110",
            "11011011",
            "11111111",
            "10100101",
            "00100100"
        ]

    def draw_alien(self):
        """Draw a pixel alien in the menu."""

        pixel_size = 7
        alien_width = len(self.alien_pattern[0]) * pixel_size
        alien_height = len(self.alien_pattern) * pixel_size

        start_x = self.screen_rect.centerx - alien_width // 2
        start_y = int(self.screen_rect.height * 0.43)

        for row, line in enumerate(self.alien_pattern):
            for col, pixel in enumerate(line):
                if pixel == "1":
                    pygame.draw.rect(
                        self.screen,
                        self.green,
                        (
                            start_x + col * pixel_size,
                            start_y + row * pixel_size,
                            pixel_size,
                            pixel_size
                        )
                    )

    def draw_centered_text(self, text, font, color, y):
        """Render text centered horizontally."""

        image = font.render(text, True, color)
        rect = image.get_rect(
            center=(self.screen_rect.centerx, y)
        )

        self.screen.blit(image, rect)

    def draw(self):
        """Draw the complete main menu."""

        center_x = self.screen_rect.centerx
        height = self.screen_rect.height

        # Game title.
        self.draw_centered_text(
            "ALIEN",
            self.title_font,
            self.green,
            int(height * 0.16)
        )

        self.draw_centered_text(
            "INVASION",
            self.title_font,
            self.green,
            int(height * 0.24)
        )

        # Decorative separator.
        pygame.draw.line(
            self.screen,
            self.dim_green,
            (center_x - 180, int(height * 0.31)),
            (center_x + 180, int(height * 0.31)),
            2
        )

        self.draw_alien()

        self.draw_centered_text(
            "DEFEND THE EARTH",
            self.small_font,
            self.dim_green,
            int(height * 0.55)
        )

        # Blinking start prompt.
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            pygame.draw.rect(
                self.screen,
                self.green,
                self.start_rect,
                2
            )

            self.draw_centered_text(
                "START GAME",
                self.menu_font,
                self.green,
                self.start_rect.centery
            )

        self.draw_centered_text(
            "ARROWS: MOVE    SPACE: FIRE",
            self.small_font,
            self.dim_green,
            int(height * 0.84)
        )

        self.draw_centered_text(
            "PRESS Q TO QUIT",
            self.small_font,
            self.dim_green,
            int(height * 0.89)
        )

        self.draw_centered_text(
            "INSERT COIN",
            self.small_font,
            self.green,
            int(height * 0.95)
        )
