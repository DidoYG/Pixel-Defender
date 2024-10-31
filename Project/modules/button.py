import pygame

from .entity import Entity

pygame.init()

WHITE = (255, 255, 255)


class Button(Entity):
    """
    Class "Button"

    A graphical button that can be displayed on a screen, with hover effects
        and an optional action when clicked.

    Attributes:
        text (str): The label or text displayed on the button.
        font (pygame.font.Font): The font used to render the text.
        color (tuple): The color of the button in normal state.
        hover_color (tuple): The color of the button when hovered
            over by the mouse.
        action (callable, optional): A function to be called when the
            button is clicked.
    """
    def __init__(self, width, height, x_pos, y_pos, speed, image_path, text,
                 font, color, hover_color, action=None):
        """
        Initializes the Button instance.

        Args:
            width (int): The width of the button.
            height (int): The height of the button.
            x_pos (int): The x-coordinate position of the button on the screen.
            y_pos (int): The y-coordinate position of the button on the screen.
            speed (int): The movement speed of the button (if applicable).
            image_path (str): The path to the image used for the
                button background (from Entity).
            text (str): The text displayed on the button.
            font (pygame.font.Font): The font used to render the button's text.
            color (tuple): The button's color in normal state.
            hover_color (tuple): The color of the button when hovered.
            action (callable, optional): The function to be executed when the
                button is clicked.
        """
        super().__init__(width, height, x_pos, y_pos, speed, image_path)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def move(self, direction, screen_w, screen_h):
        """
        Placeholder for the move method.
        This button does not have movement logic.

        Args:
            direction (int): Direction of movement (not used).
            screen_w (int): Screen width (not used).
            screen_h (int): Screen height (not used).
        """
        pass

    def draw(self, screen, mouse_pos):
        """
        Override of the base draw method in Entity.
        Draws the button on the screen and handles hover state
        and click events.

        Args:
            screen (pygame.Surface): The screen or surface where
                the button is drawn.
            mouse_pos (tuple): The current position of the mouse cursor.

        Behavior:
            - Changes the button color to `hover_color` when the
                mouse is over it.
            - Executes the `action` when the button is clicked (mouse pressed).
        """
        if (self.x_pos < mouse_pos[0] < self.x_pos + self.width and
                self.y_pos < mouse_pos[1] < self.y_pos + self.height):
            pygame.draw.rect(screen, self.hover_color,
                             (self.x_pos, self.y_pos, self.width, self.height))

            if pygame.mouse.get_pressed()[0] == 1 and self.action:
                self.action()
        else:
            pygame.draw.rect(screen, self.color, (self.x_pos, self.y_pos,
                                                  self.width, self.height))
        # Render and center the text within the button
        button_text = self.font.render(self.text, True, WHITE)
        screen.blit(button_text, (self.x_pos +
                                  (self.width // 2 -
                                   button_text.get_width() // 2), self.y_pos +
                                  (self.height // 2 -
                                   button_text.get_height() // 2)))
