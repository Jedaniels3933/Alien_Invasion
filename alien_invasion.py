import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()    # Create a clock object to control the frame rate
        self.settings = Settings() # Create an instance of the Settings class
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set to fullscreen
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))  # Uncomment to disable fullscreen

        self.settings.screen_width = self.screen.get_rect().width  # Set the screen dimensions to the display's dimensions  
        self.settings.screen_height = self.screen.get_rect().height  # Set the screen dimensions to the display's dimensions

        pygame.display.set_caption("Alien Invasion")  # Set the window title
        self.ship = Ship(self)  # Create an instance of the Ship class
        self.bullets = pygame.sprite.Group() # Create a group to store bullets in
        self.aliens = pygame.sprite.Group()  # Create a group to store aliens in

        self._create_fleet() # Create the fleet of aliens
        self.bg_color = (230, 230, 230)  # Set the background color

    def _create_fleet(self):
        """Create a fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_x_space = self.settings.screen_width - 2 * alien_width
        available_y_space = self.settings.screen_height - 3 * alien_height
        
        number_aliens_x = available_x_space // (2 * alien_width)
        number_rows = available_y_space // (2 * alien_height)
        
        for row in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_width + 2 * alien_width * alien_number, 
                                   alien_height + 2 * alien_height * row)
    
    def _create_alien(self, x_position, y_position):
        """Create an alien and add it to the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def run_game(self):
        # Start the main loop for the game
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self.update_aliens()
            self.bullets.update()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            print(len(self.bullets))
            self._update_screen()
            self.clock.tick(60)  # Set the frame rate to 60 frames per second

    def _check_events(self):
        # Watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Handles key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Handles key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()



    def update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()  
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")
            self._ship_hit()
        

    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.settings.ships_left > 0:
            self.settings.ships_left -= 1
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            print(self.settings.ships_left)
        else:
            sys.exit()


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    

       
        

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()  # Draw the ship on the screen
        self.aliens.draw(self.screen)


        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()  # Run the game





