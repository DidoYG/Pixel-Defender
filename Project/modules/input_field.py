import pygame

from .entity import Entity

pygame.init()


class InputField(Entity):
    """
    Class representing an input field for text input in the game.

    Inherits from the Entity class and adds attributes and methods specific
        to handling user text input and interaction.

    Attributes:
        font (pygame.font.Font): The font used for rendering the text
            inside the input field.
        active_color (tuple): The color of the input field when it is active.
        inactive_color (tuple): The color of the input field when it
            is inactive.
        color (tuple): The current color of the input field, depending
            on whether it is active or inactive.
        is_active (bool): A flag indicating whether the input field
            is currently active (clicked and ready for input).
        text (str): The current text inputted into the field.
        rect (pygame.Rect): The rectangular area of the input field.
    """
    def __init__(self, width, height, x_pos, y_pos, speed, image_path,
                 font, active_color, inactive_color):
        """
        Initializes an InputField instance with size, position, color,
            and font for rendering text input.

        Args:
            width (int): The width of the input field.
            height (int): The height of the input field.
            x_pos (int): The x-coordinate position of the input
                field on the screen.
            y_pos (int): The y-coordinate position of the input
                field on the screen.
            speed (int): Not used in the input field but required by the
                Entity base class.
            image_path (str): Not used for rendering in this class, but passed
                to the base Entity class.
            font (pygame.font.Font): The font used to render the text inside
                the input field.
            active_color (tuple): The color of the input field when
                it's active.
            inactive_color (tuple): The color of the input field when
                it's inactive.

        Attributes Initialized:
            color (tuple): Initially set to the `inactive_color`, but changes
                based on the input field's state.
            is_active (bool): Initially set to False, indicating that the
                input field is not active.
            text (str): The text string that stores user input, initially
                an empty string.
            rect (pygame.Rect): A rectangle representing the size and position
                of the input field for collision detection.
        """
        super().__init__(width, height, x_pos, y_pos, speed, image_path)
        self.font = font
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.color = self.inactive_color
        self.is_active = False
        self.text = ""
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width,
                                self.height)

    def move(self, direction, screen_w, screen_h):
        """
        Abstract method implementation for the movement of the input field.

        Args:
            direction (int): Direction of movement (not used in this class).
            screen_w (int): Screen width (not used in this class).
            screen_h (int): Screen height (not used in this class).

        This method is a placeholder for moving the input field, but in
            this implementation, it does nothing.
        """
        pass

    def draw(self, screen):
        """
        Override of the base draw method in Entity.
        Draws the input field on the screen, including the current text.

        Args:
            screen (pygame.Surface): The surface on which the input field
                and text will be drawn.

        Behavior:
            - Renders the current text inside the input field.
            - Adjusts the input field's width dynamically based on the
                length of the text.
            - Draws a rectangle around the input field to indicate
                its boundaries.
        """
        txt_surface = self.font.render(self.text, True, self.color)
        width = max(self.rect.width, txt_surface.get_width() + 10)
        self.rect.w = width
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def handle_event(self, event):
        """
        Process events related to the input field, such as mouse clicks and
        keyboard input.

        Args:
            event (pygame.event.Event): The event object representing
                user input,
            which can be a mouse event (clicks) or keyboard
                event (key presses).

        Functionality:
            - Activates the input field when the user clicks inside
                its rectangular area, deactivates it if clicked outside.
            - Adjusts the input field's color to reflect whether
                it is active or inactive.
            - If active, processes keyboard input, handling text entry,
                including the backspace key for deleting characters.

        Behavior:
            - When the mouse clicks inside the input field, it becomes active,
                allowing text input. Clicking outside deactivates it.
            - When deactivated (clicked outside), returns the current text in
                the input field.
            - While active, processes keyboard input:
                - Backspace deletes the last character.
                - Other keys append characters to the current text.

        Returns:
            str or None: If the input field is deactivated after being active
            (i.e., when the user clicks outside the field), the current
            text is returned. Otherwise, returns None.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            was_active = self.is_active

            # Select or deselect the input field depending on click position
            if self.rect.collidepoint(event.pos):
                self.is_active = True
            else:
                self.is_active = False

            # Update the color based on whether the input field is active
            self.color = (
                    self.active_color
                    if self.is_active
                    else self.inactive_color
                )

            # If the field was active and now it's inactive, return the text
            if was_active and not self.is_active:
                return self.text

        if event.type == pygame.KEYDOWN and self.is_active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Remove the last character.
            else:
                self.text += event.unicode  # Add the entered character.

        return None
