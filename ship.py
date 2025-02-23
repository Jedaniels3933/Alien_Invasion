import pygame 

class Ship:
    def __init__(self, ai_game):
        # Initialize the ship and set its starting position
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        # Store a float for the ship's horizontal position
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # Update the ship's position based on the movement flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed  
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed  

        # Update rect object from self.x
        self.rect.x = int(self.x)  # Convert float to int for pixel positioning

    def blitme(self):
        self.screen.blit(self.image, self.rect)



