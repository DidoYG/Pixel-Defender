import copy
import os
import random
import sys

import pygame

from .spaceship import Spaceship
from .bullet import Bullet
from .heart import Heart
from .button import Button
from .input_field import InputField

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Pixel Defender")

SCREEN_W = 700
SCREEN_H = 900
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
DEFAULT_FILE = 'scores/score-list.txt'
CLOCK = pygame.time.Clock()


def cap_fps():
    """
    The 'cap_fps' function ensures that the game runs smoothly by limiting the
    number of frames per second to 60. This keeps the game from running
    too fast on more powerful machines, creating a consistent experience.
    """
    CLOCK.tick(60)


def get_surface(font, text, color):
    """
    Renders a text surface.

    Args:
        font (pygame.font.Font): The font object used to render the text.
        text (str/int): The text of the surface.
        color (tuple): The color of the text.

    Returns:
        pygame.Surface: A surface object containing the rendered text.
    """
    return font.render(text, True, color)


def display_text(surface, x_pos, y_pos):
    """
    Displays any arbitrary text at a given position on the screen.

    Args:
        surface (pygame.Surface): A rendered text surface.
        x_pos (int): The X-coordinate where the text will spawn.
        y_pos (int): The Y-coordinate where the text will spawn.

    Displays:
        Text at a given position on the screen.
    """
    SCREEN.blit(surface, (x_pos, y_pos))


def check_collisions(bullet, x_pos, y_pos, width, height):
    """
    Checks if a bullet has collided with an object based on its position.

    Args:
        bullet (Bullet): The bullet object whose position is being checked.
        x_pos (int): The X-coordinate of the object to check against.
        y_pos (int): The Y-coordinate of the object to check against.
        width (int): The width of the object.
        height (int): The height of the object.

    Returns:
        bool: True if the bullet has collided with the object, False otherwise.
    """
    if (bullet.is_fired and y_pos <= bullet.y_pos <= y_pos + height and
            x_pos <= bullet.x_pos <= x_pos + width):
        return True
    else:
        return False


def move_bullets(bullet, direction):
    """
    Moves and draws bullets if they have been fired.

    Args:
        bullet (Bullet): The bullet object that will be moved and drawn.
        direction (int): The direction in which the bullet should move.
    """
    if bullet.is_fired:
        bullet.move(direction, SCREEN_W, SCREEN_H)
        bullet.draw(SCREEN)


def reset_bullets(bullet):
    """
    Resets the bullet to its default position off-screen and marks it as
        not fired.

    Args:
        bullet (Bullet): The bullet object to reset.
    """
    bullet.is_fired = False
    bullet.x_pos = SCREEN_W
    bullet.y_pos = SCREEN_H


def load_sound(path, volume):
    """
    Loads a sound from a given path and sets its volume.

    Args:
        path (str): The file path to the sound file.
        volume (float): The volume level to set for the sound. If volume is -1,
                        the volume is not modified.

    Returns:
        pygame.mixer.Sound: A sound object that can be played during the game.
    """
    sound = pygame.mixer.Sound(path)
    if volume != -1:
        sound.set_volume(volume)

    return sound


def get_rand_spawn(location_list, rand_num):
    """
    Generates a random spawn location for an object and ensures it doesn't
    overlap with the previous spawn location.

    Args:
        location_list (dict): A dictionary containing the previous spawn
            location and the new spawn location.
        rand_num (int): A random number (1, 2, or 3) representing
            a potential spawn zone.

    The function modifies the 'spawn_location' and 'previous_location' in the
    location_list to ensure that two consecutive objects don't spawn in
    the same location.
    """

    # It check for previous location.
    if location_list['previous_location'] == 0:
        location_list['previous_location'] = rand_num

        # The spawn location is set between on of these 3.
        if rand_num == 1:
            location_list['spawn_location'] = random.randint(75, 175)
        elif rand_num == 2:
            location_list['spawn_location'] = random.randint(325, 375)
        elif rand_num == 3:
            location_list['spawn_location'] = random.randint(525, 625)

    # If there is a previous location it recursively gets a different one.
    elif (location_list['previous_location'] >= 1 and
            location_list['previous_location'] <= 3):
        locations = [1, 2, 3]
        locations.remove(location_list['previous_location'])
        location_list['previous_location'] = 0
        get_rand_spawn(location_list,
                       random.choice([locations[0], locations[1]]))


def load_aliens(alien_list):
    """
    Loads a specified number of alien spaceships into the alien_list
    at random spawn locations. Each alien can be one of three types
    with different attributes.

    Args:
        alien_list (list): The list to which the alien spaceship instances
        will be appended.
    """

    # A dictionary with previous locations.
    rand_location = {"spawn_location": 0, "previous_location": 0}

    for i in range(0, 2):
        alien_type = random.randint(1, 3)

        get_rand_spawn(rand_location, random.randint(1, 3))

        if alien_type == 1:
            alien_list.append(copy.copy(Spaceship(100, 100,
                                        rand_location['spawn_location'],
                                        -1, 3, 'raw/alien_small.png', 1,
                                        Bullet(5, 20, 0, 0, 30, 'N/A', 10),
                                        50, False)))
        elif alien_type == 2:
            alien_list.append(copy.copy(Spaceship(120, 120,
                                        rand_location['spawn_location'],
                                        -1, 1.5, 'raw/alien_medium.png', 1,
                                        Bullet(5, 20, 0, 0, 30, 'N/A', 25),
                                        75, False)))
        elif alien_type == 3:
            alien_list.append(copy.copy(Spaceship(150, 150,
                                        rand_location['spawn_location'],
                                        -1, 0.75, 'raw/alien_big.png', 1,
                                        Bullet(5, 20, 0, 0, 30, 'N/A', 50),
                                        100, False)))


def get_heart():
    """
    Creates and returns a copy of a Heart object.

    Returns:
        Heart: A new Heart object with predefined attributes.
    """
    return copy.copy(Heart(80, 80, 350, -1, 1, 'raw/heart.png', 30))


def quit_game():
    """
    Quits the game and closes the Pygame window.

    This function also terminates the program execution.
    """
    pygame.quit()
    sys.exit()


def play_game():
    """
    Initiates the main game loop by calling the main_game function.
    """
    game_loop()


def check_file_path(path):
    """
    Checks if the provided file path is valid and exists.

    Args:
        path (str): The file path to be validated.

    Returns:
        bool: True if the file exists and has a valid text format,
              False otherwise.
    """
    res = False

    if path == DEFAULT_FILE:
        res = True
    else:
        # Exception handling in case of an invalid path or
        # unsupported format.
        try:
            if path.lower().endswith((".txt")):
                if os.path.exists(path):
                    res = True
                else:
                    print("Warning: The file", path, "does not exist.")
            else:
                print("Warning: The file", path,
                      "does not have a supported text format.")
        except pygame.error as e:
            print("Pygame error:", e)
        except Exception as e:
            print("Unexpected error:", e)

    return res


def write_scores(name, path, score):
    """
    Appends a player's score to the specified file.

    Args:
        name (str): The name of the player.
        path (str): The file path where the score will be written.
        score (int): The score to be recorded.

    Returns:
        bool: True if the score was successfully written, False otherwise.
    """
    res = False

    # Exception handling in case of an error with writing.
    try:
        with open(path, 'a') as file:
            file.write(f"{name} - Score: {score}\n")
        res = True
    except Exception as e:
        print("Unexpected error:", e)

    return res


def read_scores(score_list, path):
    """
    Reads scores from the default score file and populates the score_list.

    Args:
        score_list (list): The list to which the read scores will be appended.

    Returns:
        bool: True if the scores were successfully read, False otherwise.
    """
    res = False

    # Exception handling in case of an error with reading.
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                parts = line.split(": ")

                if len(parts) == 2:
                    score = int(parts[1].strip())
                    score_list.append((line, score))

        res = True
    except Exception as e:
        print("Unexpected error:", e)

    return res


def main_menu():
    """
    Displays the main menu of the game.

    The main menu includes options to start the game, view high scores,
    and quit the game. It renders buttons for each option and responds
    to user input, allowing navigation through the menu. The menu title
    is displayed prominently at the top.

    The function runs in a loop, checking for quit events and updating
    the display at a controlled frame rate.

    Returns:
        None
    """
    font_button = pygame.font.SysFont("Arial", 50)
    font_title = pygame.font.SysFont("Arial", 80)

    title_surface = get_surface(font_title, "Pixel Defender", WHITE)

    play_bt = Button(200, 80, SCREEN_W // 2 - 100, SCREEN_H // 2, 0, 'N/A',
                     "Play", font_button, BLACK, DARK_GRAY, play_game)
    scores_bt = Button(300, 80, SCREEN_W // 2 - 150, SCREEN_H // 2 + 125, 0,
                       'N/A', "High Scores", font_button, BLACK, DARK_GRAY,
                       input_file_menu)
    quit_bt = Button(200, 80, SCREEN_W // 2 - 100, SCREEN_H // 2 + 250, 0,
                     'N/A', "Quit", font_button, BLACK, DARK_GRAY, quit_game)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        SCREEN.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        display_text(
                title_surface,
                SCREEN_W // 2 - title_surface.get_width() // 2,
                300 - title_surface.get_height() // 2
            )

        play_bt.draw(SCREEN, mouse_pos)
        scores_bt.draw(SCREEN, mouse_pos)
        quit_bt.draw(SCREEN, mouse_pos)

        pygame.display.flip()
        cap_fps()

    quit_game()


def pause_menu():
    """
    Displays the pause menu and handles user interaction.

    The menu allows the player to resume the game by pressing the SPACE
    key or quit the game by clicking the quit button. The pause menu
    shows the paused status and the options available to the player.

    This function runs a loop that processes events, updates the display,
    and checks for user input. When the player resumes the game, the
    function will return; if they quit, the game will terminate.

    It uses the Button class for the quit button and the display_text
    function to show text on the screen.

    Returns:
        None
    """
    font_button = pygame.font.SysFont("Arial", 40)
    font_title = pygame.font.SysFont("Arial", 50)

    title_surface = get_surface(font_title, "Paused", WHITE)
    resume_surface = get_surface(font_button, "Resume (SPACE)", WHITE)

    quit_bt = Button(200, 80, SCREEN_W // 2 - 100, SCREEN_H // 2 + 120, 0,
                     'N/A', "Quit", font_button, BLACK, DARK_GRAY, quit_game)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        SCREEN.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return

        display_text(
            title_surface,
            SCREEN_W // 2 - title_surface.get_width() // 2,
            300 - title_surface.get_height() // 2
        )

        display_text(
            resume_surface,
            SCREEN_W // 2 - resume_surface.get_width() // 2,
            SCREEN_H // 2 - resume_surface.get_height() // 2
        )

        quit_bt.draw(SCREEN, mouse_pos)

        pygame.display.flip()
        cap_fps()

    quit_game()


def game_over_menu(text, score, draw_score=None, draw_health=None):
    """
    Displays the game over menu when the player loses.

    This function presents options for the player to either save their score,
    retry the game, or quit. It shows a message indicating the game over state,
    as well as the player's score and health if the respective draw functions
    are provided.

    Parameters:
        text (str): The message to display to the player indicating the
            game is over.
        score (int): The score achieved by the player, to be saved
            if requested.
        draw_score (function, optional): A function to draw the score on
            the screen. Defaults to None.
        draw_health (function, optional): A function to draw the player's
            health on the screen. Defaults to None.

    Returns:
        None
    """
    font_button = pygame.font.SysFont("Arial", 40)
    font_title = pygame.font.SysFont("Arial", 50)

    title_surface = get_surface(font_title, text, WHITE)

    save_score_bt = Button(200, 80, SCREEN_W // 2 - 100, SCREEN_H // 2, 0,
                           'N/A', "Save Score", font_button, BLACK, DARK_GRAY,
                           lambda: save_score_menu(score))
    retry_bt = Button(200, 80, SCREEN_W // 2 - 100, SCREEN_H // 2 + 120, 0,
                      'N/A', "Retry", font_button, BLACK, DARK_GRAY, play_game)
    quit_bt = Button(200, 80, SCREEN_W // 2 - 100, SCREEN_H // 2 + 240, 0,
                     'N/A', "Quit", font_button, BLACK, DARK_GRAY, quit_game)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        SCREEN.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        display_text(
                title_surface,
                SCREEN_W // 2 - title_surface.get_width() // 2,
                300 - title_surface.get_height() // 2
            )

        save_score_bt.draw(SCREEN, mouse_pos)
        retry_bt.draw(SCREEN, mouse_pos)
        quit_bt.draw(SCREEN, mouse_pos)
        draw_score()
        draw_health()

        pygame.display.flip()
        cap_fps()

    quit_game()


def save_score_menu(score):
    """
    Displays the input menu for saving the player's score.

    This function allows the player to enter their name and specify a file
    path to save their score. If no file path is given then the default one
    is used. It provides feedback on the save status and offers the option
    to go back to the previous menu.

    Parameters:
        score (int): The score achieved by the player to be saved.

    Returns:
        None
    """
    font_text = pygame.font.SysFont("Arial", 40)
    font_path = pygame.font.SysFont("Arial", 25)

    text = "Save (s)"
    name = "Player"
    path = DEFAULT_FILE

    is_saved = False

    save_surface = get_surface(font_text, text, WHITE)
    return_surface = get_surface(font_text, "Go back (b)", WHITE)
    name_surface = get_surface(font_text, "Name", WHITE)
    path_surface = get_surface(font_text, "File path (optional)", WHITE)

    name_field = InputField(350, 50, SCREEN_W // 2 - 175, SCREEN_H // 2, 0,
                            'N/A', font_text, WHITE, DARK_GRAY)
    path_field = InputField(680, 35, SCREEN_W // 2 - 340, SCREEN_H // 2 + 180,
                            0, 'N/A', font_path, WHITE, DARK_GRAY)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            res_name = name_field.handle_event(event)
            if res_name is not None:
                name = res_name
            res_path = path_field.handle_event(event)
            if res_path is not None:
                path = res_path

        SCREEN.fill(BLACK)

        if name == "":
            name = "Player"

        if path == "":
            path = DEFAULT_FILE

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_s] and not is_saved and not name_field.is_active
                and not path_field.is_active):
            if check_file_path(path):
                if write_scores(name, path, score):
                    text = "Score saved!"
                    save_surface = get_surface(font_text, text, WHITE)
                    is_saved = True
                else:
                    text = "Score NOT saved!"
                    save_surface = get_surface(font_text, text, WHITE)
            else:
                text = "Invalid path!"
                save_surface = get_surface(font_text, text, WHITE)
        if (keys[pygame.K_b] and not name_field.is_active and
                not path_field.is_active):
            return

        display_text(
                save_surface,
                SCREEN_W // 2 - save_surface.get_width() // 2,
                200 - save_surface.get_height() // 2
            )
        display_text(
                return_surface,
                SCREEN_W // 2 - return_surface.get_width() // 2,
                300 - return_surface.get_height() // 2
            )
        display_text(
                name_surface,
                SCREEN_W // 2 - name_surface.get_width() // 2,
                420 - name_surface.get_height() // 2
            )
        display_text(
                path_surface,
                SCREEN_W // 2 - path_surface.get_width() // 2,
                600 - path_surface.get_height() // 2
            )
        name_field.draw(SCREEN)
        path_field.draw(SCREEN)

        pygame.display.flip()
        cap_fps()

    quit_game()


def top_scores_menu(user_path="", is_user_given=False):
    """
    Displays the scores menu, showing the top 5 scores from the score list.

    This function reads the scores from the file and a user provided one,
    if such is given. Then displays them on the screen in descending order.
    If there are fewer than 5 scores, placeholders are displayed for the
    remaining positions. The user can return to the previous main menu by
    pressing the 'b' key.

    The function handles events for quitting the game and rendering
    the scores on the screen. The menu refreshes at a controlled frame
    rate.

    Args:
        user_path (str, optional): The file path provided by the user to
            load the scores. Defaults to an empty string.
        is_user_given (bool, optional): A flag indicating whether the user has
            specified a custom file path for the score list. Defaults to False.

    Returns:
        None
    """
    font_text = pygame.font.SysFont("Arial", 40)
    text = "Top 5 Scores"

    score_list = []

    title_surface = get_surface(font_text, text, WHITE)
    quit_surface = get_surface(font_text, "Go back (b)", WHITE)

    if is_user_given:
        if not read_scores(score_list, user_path):
            text = "Error reading user file!"
            title_surface = get_surface(font_text, text, WHITE)

    if read_scores(score_list, DEFAULT_FILE):
        score_list.sort(key=lambda x: x[1], reverse=True)
    else:
        text = "Error reading file!"
        title_surface = get_surface(font_text, text, WHITE)

    if len(score_list) < 5:
        for i in range(len(score_list), 5):
            score_list.append(("___", 0))

    score_1 = get_surface(font_text, score_list[0][0], WHITE)
    score_2 = get_surface(font_text, score_list[1][0], WHITE)
    score_3 = get_surface(font_text, score_list[2][0], WHITE)
    score_4 = get_surface(font_text, score_list[3][0], WHITE)
    score_5 = get_surface(font_text, score_list[4][0], WHITE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        SCREEN.fill(BLACK)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_b]:
            return

        display_text(
                title_surface,
                SCREEN_W // 2 - title_surface.get_width() // 2,
                150 - title_surface.get_height() // 2
            )
        display_text(
                score_1,
                SCREEN_W // 2 - score_1.get_width() // 2,
                300 - score_1.get_height() // 2
            )
        display_text(
                score_2,
                SCREEN_W // 2 - score_2.get_width() // 2,
                375 - score_2.get_height() // 2
            )
        display_text(
                score_3,
                SCREEN_W // 2 - score_3.get_width() // 2,
                450 - score_3.get_height() // 2
            )
        display_text(
                score_4,
                SCREEN_W // 2 - score_4.get_width() // 2,
                525 - score_4.get_height() // 2
            )
        display_text(
                score_5,
                SCREEN_W // 2 - score_5.get_width() // 2,
                600 - score_5.get_height() // 2
            )
        display_text(
                quit_surface,
                SCREEN_W // 2 - quit_surface.get_width() // 2,
                750 - quit_surface.get_height() // 2
            )

        pygame.display.flip()
        cap_fps()

    quit_game()


def input_file_menu():
    """
    Displays the input file menu, allowing the user to provide a file path to
    load scores, or skip and view default scores.

    This menu provides an input field for the user to enter a custom file path.
    If a valid path is provided, the corresponding scores are combined with
    the default ones and then displayed. If the path is invalid, an error
    message is shown. The user can bypass the file input and view the default
    scores by pressing 's' without entering a path.

    Pressing 'b' allows the user to return to the previous menu.

    Returns:
        None
    """
    font_text = pygame.font.SysFont("Arial", 40)
    font_path = pygame.font.SysFont("Arial", 25)

    text = "See scores (s)"
    path = None

    proceed_surface = get_surface(font_text, text, WHITE)
    return_surface = get_surface(font_text, "Go back (b)", WHITE)
    path_surface = get_surface(font_text, "File path (optional)", WHITE)
    info_surface = get_surface(font_path, "* To skip file input just press "
                               "(s) without typing anything *", WHITE)

    path_field = InputField(680, 35, SCREEN_W // 2 - 340, SCREEN_H // 2 + 100,
                            0, 'N/A', font_path, WHITE, DARK_GRAY)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            res_path = path_field.handle_event(event)
            if res_path is not None:
                path = res_path

        SCREEN.fill(BLACK)

        if path == "":
            path = None

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_s] and not path_field.is_active):
            if path is not None:
                if check_file_path(path):
                    top_scores_menu(path, True)
                else:
                    text = "Invalid path!"
                    proceed_surface = get_surface(font_text, text, WHITE)
            else:
                top_scores_menu()
        if (keys[pygame.K_b] and not path_field.is_active):
            return

        display_text(
                proceed_surface,
                SCREEN_W // 2 - proceed_surface.get_width() // 2,
                200 - proceed_surface.get_height() // 2
            )
        display_text(
                return_surface,
                SCREEN_W // 2 - return_surface.get_width() // 2,
                300 - return_surface.get_height() // 2
            )
        display_text(
                path_surface,
                SCREEN_W // 2 - path_surface.get_width() // 2,
                500 - path_surface.get_height() // 2
            )
        display_text(
                info_surface,
                SCREEN_W // 2 - info_surface.get_width() // 2,
                750 - info_surface.get_height() // 2
            )
        path_field.draw(SCREEN)

        pygame.display.flip()
        cap_fps()

    quit_game()


def game_loop():
    """
    Main game loop for Pixel Defender.

    Initializes the player, aliens, and other game elements, and
    handles the game mechanics such as movement, shooting,
    collision detection, and scoring. The game continues until
    the player runs out of health or quits the game.

    Returns:
        None
    """
    player = Spaceship(130, 130, 350, 780, 10, 'raw/player.png', 100,
                       Bullet(5, 20, 0, 0, 30, 'N/A', 1), 0, True)
    heart = get_heart()
    alien_list = []
    score = 0
    goal = 10
    level = 1

    font_stats = pygame.font.SysFont("Arial", 30)

    health_surface = get_surface(font_stats, f"Health: {player.health}", RED)
    score_surface = get_surface(font_stats, f"Score: {score}", GREEN)

    running = True
    is_game_over = False

    game_over_text = "YOU DIED"

    shoot_sound = load_sound('raw/shoot.mp3', 0.5)
    hit_sound = load_sound('raw/hit-taken.mp3', -1)
    kill_sound = load_sound('raw/enemy-killed.mp3', 0.8)
    game_over_sound = load_sound('raw/game-over.mp3', 0.8)
    health_sound = load_sound('raw/health-pickup.mp3', 0.5)
    background_song = load_sound('raw/theme-song.mp3', -1)

    background_song.play(-1)

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        SCREEN.fill(BLACK)
        display_text(score_surface, 30, 850)
        display_text(health_surface, 530, 850)

        if is_game_over:
            game_over_menu(
                game_over_text,
                score,
                lambda: display_text(score_surface, 30, 850),
                lambda: display_text(health_surface, 530, 850)
            )
        else:
            # Player controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move(-1, SCREEN_W, SCREEN_H)
            if keys[pygame.K_RIGHT]:
                player.move(1, SCREEN_W, SCREEN_H)
            if keys[pygame.K_p]:
                background_song.stop()
                pause_menu()
                background_song.play(-1)
            if keys[pygame.K_SPACE] and not player.bullet.is_fired:
                player.shoot(shoot_sound)

            # Load a number aliens based on the current level
            if len(alien_list) < level:
                load_aliens(alien_list)

            player.draw(SCREEN)

            move_bullets(player.bullet, -1)

            # Main loop that controls aliens
            for alien in alien_list:
                if not alien.is_killed:
                    alien.move(1, SCREEN_W, SCREEN_H)

                    # Check if the alien reaches the player
                    if alien.is_killed:
                        is_game_over = True
                        game_over_text = "ALIENS REACHED YOU"
                        player.health = 0
                        health_surface = get_surface(
                                font_stats,
                                f"Health: {player.health}",
                                RED
                            )
                        game_over_sound.play()
                        background_song.stop()
                        break

                    alien.draw(SCREEN)

                    # Alien shooting logic
                    if not alien.bullet.is_fired:
                        alien.alien_shoot(shoot_sound)

                    move_bullets(alien.bullet, 1)

                    # Check collisions with the player's bullet
                    if (check_collisions(player.bullet, alien.x_pos,
                                         alien.y_pos, alien.width,
                                         alien.height)):
                        alien.is_killed = True
                        reset_bullets(player.bullet)
                        score += 1

                        if score % 25 == 0:
                            level += 1

                        score_surface = get_surface(
                                font_stats,
                                f"Score: {score}",
                                GREEN
                            )
                        kill_sound.play()

                    # Check collisions with the alien's bullet
                    if (check_collisions(alien.bullet, player.x_pos,
                                         player.y_pos, player.width,
                                         player.height)):
                        player.health -= alien.bullet.damage
                        reset_bullets(alien.bullet)

                        if player.health < 0:
                            player.health = 0
                        health_surface = get_surface(
                                font_stats,
                                f"Health: {player.health}",
                                RED
                            )

                        hit_sound.play()

                    # Remove killed aliens from the list
                    if alien.is_killed:
                        alien_list.remove(alien)
                        del alien.bullet
                        del alien

                    # Check if player health is 0
                    if player.health <= 0:
                        is_game_over = True
                        game_over_sound.play()
                        background_song.stop()
                        break

            # Check if the score has reached the goal for health pickup
            if score >= goal:
                if not heart.is_claimed:
                    heart.move(1, SCREEN_W, SCREEN_H)
                    heart.draw(SCREEN)

                    # Check collisions with the player's bullet
                    if (check_collisions(player.bullet, heart.x_pos,
                                         heart.y_pos, heart.width,
                                         heart.height)):
                        heart.is_claimed = True
                        player.health += heart.restore_amount
                        reset_bullets(player.bullet)
                        goal += 10
                        health_sound.play()

                        if player.health > 100:
                            player.health = 100
                        health_surface = get_surface(
                                font_stats,
                                f"Health: {player.health}",
                                RED
                            )
                else:
                    del heart
                    heart = get_heart()

        pygame.display.flip()
        cap_fps()

    quit_game()


def start_game():
    """
    Initiates the game by displaying the main menu and
    subsequently allowing the user to quit the game.

    This function does not take any parameters and does not
    return any value. It calls the main_menu function to
    display the main game options and then calls quit_game
    to handle exiting the game.

    The game logic and flow are managed within these called functions.
    """
    main_menu()
    quit_game()
