import os
from abc import ABC, abstractmethod

import pygame

pygame.init()

WHITE = (255, 255, 255)


class Entity(ABC):
    """
    Abstract base class representing a generic entity in the game.

    Attributes:
        width (int): The width of the entity.
        height (int): The height of the entity.
        x_pos (int): The x-coordinate position of the entity on the screen.
        y_pos (int): The y-coordinate position of the entity on the screen.
        speed (int): The speed at which the entity moves.
        image_path (str): The file path to the image used for the entity.
        has_image (bool): Indicates whether the entity has an image.
        image (pygame.Surface): The loaded image for the
            entity (if applicable).
        placeholder (pygame.Rect): A placeholder rectangle for positioning
            the image.
    """
    def __init__(self, width, height, x_pos, y_pos, speed, image_path):
        """
        Initializes the base Entity instance with size, position,
            speed, and image.

        Args:
            width (int): The width of the entity.
            height (int): The height of the entity.
            x_pos (int): The x-coordinate of the entity on the screen.
            y_pos (int): The y-coordinate of the entity on the screen.
                        If set to -1, the entity is placed just
                            off-screen (above the screen).
            speed (int): The speed at which the entity moves.
            image_path (str): The file path to the entity's image.

        Behavior:
            - If y_pos is set to -1, the entity is positioned just
                above the screen.
            - Calls `check_imagePath` to validate and load the
                image if provided.
            - `has_image` is initialized to False and updated if a valid
                image is found.
        """
        self.width = width
        self.height = height
        self.x_pos = x_pos
        if y_pos == -1:
            self.y_pos = -height
        else:
            self.y_pos = y_pos
        self.speed = speed
        self.has_image = False
        self.check_imagePath(image_path)

    def check_imagePath(self, image_path):
        """
        Validates and loads an image from the provided path.

        Args:
            image_path (str): The file path to the image for the entity.

        Behavior:
            - Skips image loading if 'N/A' is passed as the image path.
            - Checks if the file extension is supported (PNG, JPG, JPEG).
            - Verifies the existence of the file on disk.
            - If valid, the image is loaded, scaled, and a placeholder
                rectangle is created.
            - Sets `has_image` to True if the image is successfully loaded.
            - Prints warnings if the image path is invalid, unsupported,
                or the file is not found.

        Exceptions:
            - Catches `pygame.error` if there is an issue loading the image.
            - Catches general exceptions and prints any unexpected errors.
        """
        if image_path != 'N/A':
            # Exception handling in case of an invalid path or
            # unsupported format.
            try:
                if image_path.lower().endswith((".png", ".jpg", ".jpeg")):
                    if os.path.exists(image_path):
                        self.image = pygame.image.load(
                            image_path).convert_alpha()
                        self.image = pygame.transform.scale(self.image,
                                                            (self.width,
                                                             self.height))
                        self.placeholder = self.image.get_rect(
                                center=(self.x_pos, self.y_pos)
                            )
                        self.has_image = True
                        # Resetting the x and y to be the upper-left corner.
                        self.x_pos -= self.width / 2
                        self.y_pos -= self.height / 2
                    else:
                        print("Warning: The file", image_path,
                              "does not exist.")
                else:
                    print("Warning: The file", image_path,
                          "does not have a supported image format.")
            except pygame.error as e:
                print("Pygame error:", e)
            except Exception as e:
                print("Unexpected error:", e)

    @abstractmethod
    def move(self, direction, screen_w, screen_h):
        """Abstract method to move the entity."""
        pass

    def draw(self, screen):
        """
        Draws the entity on the provided screen surface.

        Args:
            screen (pygame.Surface): The surface where the entity
                will be drawn.

        Behavior:
            - If `has_image` is True, the image is drawn using the
                placeholder rectangle.
            - If `has_image` is False, a white rectangle representing
                the entity is drawn.
        """
        if self.has_image:
            screen.blit(self.image, self.placeholder)
        else:
            pygame.draw.rect(screen, WHITE,
                             (self.x_pos, self.y_pos, self.width, self.height))
