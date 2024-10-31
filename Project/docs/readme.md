General Information:

"Pixel Defender" is a game inspired by the famous game "Space Invaders". The game follows a similar logic, with a player spaceship is trying to kill the aliens that invade them. I have made an "instructions" file that you can see for more info. It is in the same docs folder and it is called Instructions.pdf. So my game has several menus. Main menu, main game menu, game over menu, pause menu, and save scores menu. All these menus make the GUI. They can be navigated with mouse or keyboard keys, depending on the menu.

Classes and Hierarchy Structure:

The game consists of 6 classes. Entity is the base one. It is an abstract class with pure virtual method move. Its derived classes are Spaceship, Bullet, Heart, Button, InputField. Each is a child of Entity and utilizes some of its foundation data members and methods. All classes except Button and InputField override the abstract method move and give it a particular logic. The Button and InputField classes do not need to use this method and use "pass" to make it an inactive method.
Class Bullet is part of the composition of class Spaceship. 
Class Button and class InputField override the draw method of class Entity. Because they neither use images nor are simple rectangles, they have a special draw method that displays a text in them and handles mouse hover and click action.
For more information about the classes, their hierarchy, data members, and methods, you can read the documentation strings in every one of them.

Special Functions:

In main there are some fundamental functions like ones for menus and navigation, and one for collision detection.
The menus functions are separate, each representing one menu with navigation buttons. The other important function is for checking collisions. It gets the bullet x and y position and compares it to the position and size of the targeted entity. If the bullet is in the entity's hitbox, then it is killed.

Algorithms and File I/O:

The program reads and writes into text file, where it saves scores. The reading function is what displays the highest scores of the game. To do that the read function extracts the entries of the file and sorts them in a descending way. This is done with the built in sort method of the list structure in Python. After the sort only the first 5 results are printed on the screen.

Media and Images:

All the images I have used are done by me. The pixel art .png icons are made using a pixel art painter. I have saved the pixel art project with all the icons in the raw folder: Models.pixil
The sounds were taken from this royalty free [website](https://pixabay.com/). The sounds are open and free to use.

PEP8 requirements:

For the formatting of the code I have used a VS Code extension called "Flake8" which dynamically checks whether the code follows those rules. If it catches that something is wrong then it underlines that part in red, implying that it should be fixed.