import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Base class to handle game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resopurces"""
        pygame.init()

        self.settings = Settings()

        # configure screen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption(self.settings.game_title)

        self.bg = pygame.image.load("images/bg.png")
        self.bg = pygame.transform.scale(
            self.bg, (self.settings.screen_width, self.settings.screen_height)
        )

        # configure game objects
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # clock is used to manage frame rate
        self.clock = pygame.time.Clock()

    def run_game(self):
        """Start the main game loop"""
        while True:
            self._check_events()  # detect and change state
            self.ship.update()  # update game objects
            self._update_bullets()
            self._update_screen()  # render all
            self.clock.tick(self.settings.frame_rate)  # set clock to desired frame rate

    def _check_events(self):
        """Handle keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()  # update bullets - sprite group

        for bullet in self.bullets.copy():  # cannot modify list while in the loop
            if bullet.rect.bottom <= 0:  # that's why we iterate over copy
                self.bullets.remove(bullet)  # and then removing it from actual group

    def _create_fleet(self):
        """Create the fleet of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 5 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien_at(current_x, current_y)
                current_x += 2 * alien_width
            # Row complete; reset x and increment y
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien_at(self, x_position, y_position):
        """Create and place alien in the row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_screen(self):
        """Update screen images, and flip to the new frame"""
        # self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.bg, [0, 0])
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()  # refresh the screen (flip the page)


if __name__ == "__main__":
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
