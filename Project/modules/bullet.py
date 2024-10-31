from .entity import Entity


class Bullet(Entity):
    """
    Class representing a Bullet entity.

    Inherits from the Entity class and adds attributes and methods specific
        to a bullet's behavior, such as firing, damage, and movement.

    Attributes:
        damage (int): The amount of damage the bullet deals.
        is_fired (bool): Indicates whether the bullet has been fired.
    """
    def __init__(self, width, height, x_pos, y_pos, speed, image_path, damage):
        """
        Initializes a Bullet instance.

        Args:
            width (int): The width of the bullet.
            height (int): The height of the bullet.
            x_pos (int): The initial x-coordinate of the bullet.
            y_pos (int): The initial y-coordinate of the bullet.
            speed (int): The speed at which the bullet moves.
            image_path (str): The file path to the bullet's image.
            damage (int): The damage value the bullet inflicts when it
                hits a target.

        Attributes Initialized:
            is_fired (bool): Initially set to False, indicating the bullet
                hasn't been fired.
        """
        super().__init__(width, height, x_pos, y_pos, speed, image_path)
        self.damage = damage
        self.is_fired = False

    def set_coordinates(self, x, y):
        """
        Sets the bullet's coordinates and marks it as fired.

        Args:
            x (int): The x-coordinate where the bullet is spawned.
            y (int): The y-coordinate where the bullet is spawned.

        Behavior:
            - Sets the bullet's position to the given (x, y) coordinates.
            - Marks the bullet as fired by setting `is_fired` to True.
        """
        self.x_pos = x
        self.y_pos = y
        self.is_fired = True

    def move(self, direction, screen_w, screen_h):
        """
        Moves the bullet in a given direction and checks if it's out of bounds.

        Args:
            direction (int): The direction in which the bullet should
                move (e.g., -1 for upward, 1 for downward).
            screen_w (int): The width of the screen.
            screen_h (int): The height of the screen.

        Behavior:
            - Updates the bullet's y-coordinate based on its speed and the
                direction of movement.
            - If the bullet goes outside the vertical bounds of the screen,
                it is marked as not fired (`is_fired = False`),
              allowing it to be re-fired.
        """
        self.y_pos += self.speed * direction

        if self.y_pos <= 0 or self.y_pos >= screen_h:
            self.is_fired = False
