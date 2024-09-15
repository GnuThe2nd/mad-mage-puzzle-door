# The Mad Mages Puzzle Door V.1

This is a puzzle door add-on for the D&D module "Waterdeep: Dungeon of the Mad Mage", inspired by [Factorio Space Exploration](https://spaceexploration.miraheze.org/wiki/Main_Page) Alternate Ending puzzle. This page is for the DM's eyes only, as it contains code and "solution" for the door. 

The project offers:

- A way to inspire the players to keep exploring every level fully.
- A puzzle door entry to the Mad Mages Lair, that cannot be solved without exploring every level (except the Lost Level).
- A simple way to generate a random solution for each campaign.
- 21 custom Runedial door handouts, one for each level.
- A final Mad Mages Puzzle Door.exe file, that you can share with the players to solve on their own computer.

In summery, the project adds a puzzle door for every level (except Lost Level) and culminates with the giant puzzle door at the Mad Mages Lair.

- [The Mad Mages Puzzle Door V.1](#the-mad-mages-puzzle-door-v1)
  - [The story of how it came to be](#the-story-of-how-it-came-to-be)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Compile](#compile)
  - [Usage in game](#usage-in-game)
    - [Runedial Door](#runedial-door)
    - [Runedial Handouts](#runedial-handouts)
      - [Level Indicator](#level-indicator)
    - [Runedial](#runedial)
    - [The Arrow](#the-arrow)
    - [Hexagon Scheme](#hexagon-scheme)
  - [Solution](#solution)
    - [Step 1. - Assembly](#step-1---assembly)
    - [Step 2. - Translation](#step-2---translation)
    - [Step 3. - Solving the Runedials](#step-3---solving-the-runedials)
  - [Future Developement plans](#future-developement-plans)
  - [Author](#author)

## The story of how it came to be

I have been a DM since 2019 and wanted to run "Waterdeep: Dungeon of the Mad Mage" for my group. In combination with "Keys From the Golden Vault", I planned it as a stealthy heist campaign, yet failed to realise that the all players would make fragile stealthy characters, with great utility but little combat power. Now, for those who don't know, the Mad Mage's Dungeon is not exactly what anyone would call "safe". Thus it came apparent, that my players would most likely try to sneak through the entire thing, with zero to non interraction with any of the cool stuff. So I put my brain to work.

My plan was simple: Every level of the Undermountiain would have a "puzzle" door that requires a key to unlock it, and to get the keys, the players would have to explore all of the dungeon and possibly finish a heist. The first level was a blast and it seemed my idea worked out well.

Some time after I was watching DoshDoshington's Factorio Space Exploration run on Youtube and thought that the alternate ending puzzle was very interresting and decided to adapt it to D&D. Sadly, Factorio requires the player to do 3D vector math and since my table harboured players with nonexsistant mathematical backgrounds... I ended up writing this project.

In basic summery, I use a combination of Elder Runes and hexagons. There were exactly 9 Elder Runes, which made for a nice keydial and there were almost enough levels to build a nice pyramid out of the hexagons. I went ahead with this small passion project and had fun doing it. 

Feel free to use this project however you see fit.

Preview of the final program:
![Github Readme pyramid](https://github.com/user-attachments/assets/38209536-3dfe-47e4-9792-dc60a2386e50)
![Github readme keydial](https://github.com/user-attachments/assets/dcef43aa-44c0-4079-99c9-460843f3284c)

## Getting Started

If you wish to compile the code yourself, please refer to [Compile](#Compile).

Otherwise, follow these steps:
1. Create a new folder
2. Download *Setup.exe* and *Mad Mages Puzzle Door.exe*
3. Put them in the folder you created
4. Run *Setup.exe*
5. Once *Setup.exe* has finished, run *Mad Mages Puzzle Door.exe* once. Make sure that the solution.json file is in the same folder as *Mad Mages Puzzle Door.exe*

After this, you can print out or send them the handouts digitally. Once they reach the very last layer, you can send them the *Mad Mages Puzzle Door.exe* to solve. You do not have to send them any other files, the solution.json file must be in the same folder only once, when you run the *Mad Mages Puzzle Door.exe* for the first time. I advise against sedning them the solution.json file, since it can be read by the players to figure out the solution.

### Prerequisites

This project was built in Python using:

- TKinter GUI.
- Python Image Library (PIL)
- Pyinstaller

You must have these dependancies installed to compile the program from scratch. It is designed to be packed into an .exe file and then ran.

### Compile

I used pyinstaller to compile both programs to an exe file. To install pyinsatller you can do

> $ pip install pyinstaller

To install PIL, do

> $ pip install pillow

#### Compile Setup.py
Here is the pyinstaller command to compile Setup.py to *Setup.exe*

> $ pyinstaller --noconfirm --onefile --console --name "Setup" --add-data "path_to_assets_folder;assets/" --add-data "path_to_Main.py;." "path_to_Setup.py"

After this, you can just run Setup.exe and it will generate an output folder with:

1. The Runedial handouts
2. solution.json

#### Compile Main.py
Here is the pyinstaller command to compile Main.py to *Mad Mages Puzzle Door.exe*

> $ pyinstaller  --noconfirm --onefile --windowed --name "Mad Mages Puzzle Door" --distpath "output" --specpath "output/TEMP" --workpath "output/TEMP" --add-data "{asset_folder_path};./assets/main_assets/" --icon "{icon_path}" "{script_path}"'

After this, you can just run *Mad Mages Puzzle Door.exe*. Make sure that before running, the solution.json file is generated and in the same folder, but you only need to do it once. After this you can send the *Mad Mages Puzzle Door.exe* to your players and let them have a go at it.

## Usage in game

The next section is dedicated to explaining the puzzle and how to integrate it to your own campaign.

### Runedial Door

The idea behind Puzzle isn't that complicated: all you as a DM have to do, is every time the players find the stairs downwards, give them the handout of the door that corresponds to the level they are entering. This means, that they also have to have a key already to even enter the dungeons first level, which you can give them in any way you see fit.

Im curretly in the progress of making a document that suggest places for the doors, as well as suggestions for how the keys can be aquired.

[Document link once its ready.]

The Puzzle has mainly 2 components:

1. The Runedial Handouts
2. The Mad Mage's Puzzle Door

### Runedial Handouts

An example runedial looks like this:


It's 4 components are:

1. Level indicator
2. Runedial
3. Arrow
4. Hexagon Scheme

![Level_1_example](https://github.com/user-attachments/assets/59bce3b0-c48e-43b4-98b2-7c57d9496657)

You'll find an explanetion for all of them below.

#### Level Indicator

The Level Indicator at the top left corner of each handout is pretty much that: a level indicator. It shows you which handout to give to players when they are entering a new level and the players must later use the levels number as one of the hints to solving the very last puzzle.

#### Runedial

The Runedial is the big circular tablet at the middle of the handout. It consists of 9 smaller circles, each showing an Elder Rune glowing in red. The "key" to gain access to the next level isn't actually important, so feel free to make up any key for each level taht you wish. The keys they found are more of a red herring, making them seem important, while the real solution at the end comes from the order that the runes are placed in the dial. This will all be explained under the Solution tab.

For now, the Runedial works like a old rotary telephone: you pull the circle around and after release it returns to it's standard position, which is indicated by the arrow. The arrow also serves a part in the final puzzle, which will be explained later.

#### The Arrow

The arrow is the isosceles triangle in the middle of the dial. One of the triangles tips is more pointy then other, which is used to point at what the arrow is looking towards. For now, this arrow is used to just show, where the rotation of the rotary dial returns to.

#### Hexagon Scheme

This is the very base of the puzzle. Below the Runedial, a decorated hexagon is shown, with smaller hexagons around it. The hexagon paterns overlap, and start creating shapes, until a pyramid is formed.

[Hexagons overlaping.img-> hexagon pyramid.img]

## Solution

This final puzzle can only be solved, once **ALL** runedials have been found. Note that there are 21 handouts and 22 levels before the last lair. Since the Lost level (number 6) is meant to be accessed through a tunnel dug by Umber Hulks, that level does not have a puzzle door handout.

#### Step 1. - Assembly

As stated in the hexagon chapter, the hexagons, when overlapped with eachother start to slowly create a pyramid. Step 1 is finished, once the pyramid has been created.

![Hex solution](https://github.com/user-attachments/assets/d1edede3-82a9-4649-a8fd-0575656b6e07)

#### Step 2. - Translation

The bigger hexagon is meant to represent the location of the runedial and the smaller hexagon an adjacent runedials. So this pyramid can be translated as such. Step 2 is finished once the pyramid has been translated.
![Translated Pyramid](https://github.com/user-attachments/assets/80ba2a08-9481-4fa8-b03c-6ab273d488e0)

#### Step 3. - Solving the Runedials



## Future Developement plans

- GUI improvements
- General Code Cleanup
- Image generation improvements

## Author

Karl Martin Puna - \*Everything you see in this project :)
