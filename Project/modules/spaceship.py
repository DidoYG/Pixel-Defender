from .entity import Entity


class Spaceship(Entity):
    """
    Class representing a spaceship in the game.

    Attributes:
        health (int): Health of the spaceship.
        bullet (Bullet): An instance of the Bullet class representing
            the bullet that the spaceship can shoot.
        shoot_delay (int): The time interval between successive shots.
        is_player (bool): A flag indicating whether the spaceship is
            controlled by the player or is an enemy.
        is_killed (bool): A flag indicating whether the spaceship
            has been destroyed.
        shoot_timer (int): A timer that counts up to the shoot delay to
            manage shooting intervals.
    """
    def __init__(self, width, height, x_pos, y_pos, speed, image_path, health,
                 bullet, shoot_delay, is_player):
        """
        Initializes the Spaceship with the given parameters.

        Args:
            width (int): Width of the spaceship.
            height (int): Height of the spaceship.
            x_pos (int): Initial X position of the spaceship.
            y_pos (int): Initial Y position of the spaceship.
            speed (int): Movement speed of the spaceship.
            image_path (str): Path to the image representing the spaceship.
            health (int): Initial health of the spaceship.
            bullet (Bullet): An instance of the Bullet class for shooting.
            shoot_delay (int): The time delay between shots.
            is_player (bool): Indicates if this spaceship is controlled
                by the player.
        """
        super().__init__(width, height, x_pos, y_pos, speed, image_path)
        self.health = health
        self.is_killed = False
        self.bullet = bullet
        self.shoot_delay = shoot_delay
        self.is_player = is_player
        self.shoot_timer = 0

    def shoot(self, sound):
        """
        Fires a bullet from the spaceship.

        This method sets the bullet's coordinates and plays the shooting sound.

        Args:
            sound (pygame.mixer.Sound): The sound to play when shooting.
        """
        # Different spawning locations for the bullet.
        y = self.placeholder.y

        if not self.is_player:
            y += self.height

        sound.play()
        self.bullet.set_coordinates(self.placeholder.x + self.width / 2 -
                                    self.bullet.width / 2, y)

    def alien_shoot(self, sound):
        """
        Allows the alien spaceship to shoot.

        The method increments the shoot_timer until it reaches the shoot_delay.
        Once the delay is reached and the spaceship is visible on screen,
        the bullet is fired.

        Args:
            sound (pygame.mixer.Sound): The sound to play when shooting.
        """
        self.shoot_timer += 1
        # The alien can shoot once its half has appeared on the screen.
        if (self.shoot_timer >= self.shoot_delay and self.y_pos +
                self.height / 2 >= 0):
            self.shoot(sound)
            self.shoot_timer = 0

    def move(self, direction, screen_w, screen_h):
        """
        Moves the spaceship based on the specified direction.

        The movement logic varies depending on whether the spaceship is
        controlled by the player or is an alien.

        Args:
            direction (int): Direction of movement; positive values move
                right (player) or down (alien), and negative values move
                    left (player) or up (alien).
            screen_w (int): Width of the game screen to constrain
                player movement.
            screen_h (int): Height of the game screen to determine if
                the alien spaceship goes off-screen.
        """
        if self.is_player:
            self.x_pos += self.speed * direction

            if self.x_pos <= 0:
                self.x_pos = 0
            elif self.x_pos + self.width >= screen_w:
                self.x_pos = screen_w - self.width

            self.placeholder.x = self.x_pos
        else:
            self.y_pos += self.speed * direction
            self.placeholder.y = self.y_pos

            if self.placeholder.y + self.height >= screen_h - 120:
                self.is_killed = True
