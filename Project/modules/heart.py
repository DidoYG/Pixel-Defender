from .entity import Entity


class Heart(Entity):
    """
    Class representing a Heart entity, which can restore health in the game.

    Inherits from the Entity class and adds attributes and methods specific
        to the Heart's behavior, such as moving and restoring health.

    Attributes:
        restore_amount (int): The amount of health restored by the heart.
        is_claimed (bool): Indicates whether the heart has been claimed
            or gone off-screen.
    """
    def __init__(self, width, height, x_pos, y_pos, speed,
                 image_path, restore_amount):
        """
        Initializes a Heart instance with specific attributes related to size,
            position, speed, and healing amount.

        Args:
            width (int): The width of the heart entity.
            height (int): The height of the heart entity.
            x_pos (int): The initial x-coordinate of the heart on the screen.
            y_pos (int): The initial y-coordinate of the heart on the screen.
            speed (int): The speed at which the heart moves downward.
            image_path (str): The file path to the heart's image.
            restore_amount (int): The amount of health the heart
                restores when collected.

        Attributes Initialized:
            is_claimed (bool): Initially set to False, indicating that
                the heart has not yet been collected or gone out of bounds.
        """
        super().__init__(width, height, x_pos, y_pos, speed, image_path)
        self.restore_amount = restore_amount
        self.is_claimed = False

    def move(self, direction, screen_w, screen_h):
        """
        Moves the heart down the screen and checks if it has gone
            out of bounds.

        Args:
            direction (int): The direction of movement (e.g., 1 for downward).
            screen_w (int): The width of the screen (unused in this case).
            screen_h (int): The height of the screen.

        Behavior:
            - Updates the heart's vertical position based on its speed and
                the direction provided.
            - Updates the `placeholder` position used for drawing the heart
                on the screen.
            - If the heart moves off the bottom of the screen, it is marked
                as `is_claimed = True`, allowing it to be removed and replaced.
        """
        self.y_pos += self.speed * direction
        self.placeholder.y = self.y_pos

        if self.placeholder.y >= screen_h + self.height:
            self.is_claimed = True
