from PIL import Image, ImageDraw, ImageFont
from random import randint, choice, shuffle
from math import ceil
import json
import os, sys

def generate_random_solution():
    # The main rules for solution generation:
    # 1. rune is the one that the arrow in the middle points towards
    # 2. rune is always the rune 1 rune onward from the "Halaster" Rune
    # 3. rune must be a rune, that is ((Level / 3) + 1) rounded up spots onwards from the second rune
    runes = [
        "Anarath",
        "Angras",
        "Halaster",
        "Korombos",
        "Laebos",
        "Lammath",
        "Nchasme",
        "Savaros",
        "Ullathar",
    ]
    empty_list = []

    while len(empty_list) < 3:
        rune = choice(runes)
        if len(empty_list) != 1 or rune != "Halaster":  # second button clause
            if len(empty_list) != 2 or rune != "Halaster":
                if rune not in empty_list:
                    empty_list.append(rune)
    return empty_list


def generate_random_order(name, append_dict={}): 
    random_level_order = []
    '''
    This generates a list with numbers 0-21, but leaves out 5, since the level it refers to
    is the Level 6: The Lost Level, which doesnt have a door like that.
    '''
    for i in range(1, 23):
        if i != 6:
            random_level_order.append(i)
    shuffle(random_level_order)

    append_dict[name] = random_level_order
    return append_dict


def replace_missing_runes(partial):
    '''
    This function finds takes a random rune, checks if its in the partial runeset, if not
    finds the first empty slot and puts it in ;)
    '''
    runes = [
        "Anarath",
        "Angras",
        "Halaster",
        "Korombos",
        "Laebos",
        "Lammath",
        "Nchasme",
        "Savaros",
        "Ullathar",
    ]
    shuffle(runes)
    for rune in runes:
        if rune not in partial:
           partial[partial.index(True)] = rune

    return partial


def generate_runedial_positions(return_dict):
    # I The Arrow in the middle must point towards this Rune
    # II Always the rune right of the "Halaster" Rune
    # III A rune ((Level / 5) rounded up) spots onwards from the second rune
    
    all_rune_states = {} 
    all_rune_solutions = {}
    level_order = return_dict["level_order"]

    while len(all_rune_states) < 21: 

        level = level_order[len(all_rune_states)]

        '''
        This part below simulates the III rule of soliving the puzzle by doing the calculations early. since, players look at levels 1-21, 
        not 0-20, like the program this part is just set up so that the 0 gets rounded to 1 and 20 gets rounded to 5
        '''
        third_rune_step = max(ceil(level / 5), 1)

        solution = generate_random_solution() #Generates a possible solution ["Rune_name", "Rune_name", "Rune_name"]
        first_rune = solution[0]
        second_rune = solution[1]
        third_rune = solution[2]

        result = [True, True, True, True, True, True, True, True, True]
        result[0] = first_rune  # assign first_rune to the 

        '''
        Code Below starts assigning second and third solution runes placcements.
        The code is a bit messy I guess, but if its stupied and works, its still stupied... yet it works
        '''

        x = 0
        while x < 20: # basically it tries up to 20 times to randomly add the last rune:)
            result_copy = result.copy()

            '''
            The first is an attempt to fix an edgecase. 
            
            "II Always the rune 1 rune onward from the "Halaster" Rune"
            This means that the second rune can never be "Halaster" rune, since every rune in list is unique.
            Furthermore, if the first rune is "Halaster", then the second rune must be placed next to it.
            '''

            if first_rune == "Halaster":
                placement = 1
            else:
                placement = randint(2, 8)

            result_copy[placement] = second_rune  # assign the second rune
            result_copy[placement - 1] = "Halaster" # type: ignore # assign the spot to its left to "Halaster" Rune

            third_placement_index = placement + third_rune_step
            if third_placement_index != 9: # all runes are unique, the third rune cannot be itself/the second rune
                third_placement_index -= 9 # a list can iterate into the negative, we dont need to check if number is  higher then 9

                if (result_copy[third_placement_index] == True and third_rune not in result_copy):
                    result_copy[third_placement_index] = third_rune # assign the third rune

                    return_runeset = replace_missing_runes(result_copy)

                    all_rune_states[level] = return_runeset # Add the result to both returnlists
                    all_rune_solutions[level] = {"hex":len(all_rune_states), "solution":solution}
                    break

            x += 1
        if x == 20:
            all_rune_states = "This solution doesnt fit." 
            # I didnt bother to math it out, if its possible to not find a solution, so this is here just incase.
            break
        
    return_dict["runeset"] = all_rune_states
    return_dict["solution"] = all_rune_solutions       
    return return_dict


def shift_list_to_right(lst, index):
    index = index % len(lst)
    return lst[-index:] + lst[:-index]


def generate_runedials(runedials_dict):

    myFont = ImageFont.truetype('arial.ttf', 150)
    arrowa = Image.open("./assets/utility_assets/Arrow.png")
    level_order = runedials_dict["level_order"]

    for hex_index, level in enumerate(level_order):

        print(f"Level {level}... ", end="", flush=True)

        background_img = Image.open(f"./assets/utility_assets/door_puzzle_templates/{hex_index}.png" )
        return_img = background_img.copy()
        
        runeset = runedials_dict["runeset"][level]
        cordinates = [(618, 270), (850, 353), (970, 580), 
                      (930, 825), (745, 990), (495, 990), 
                      (310, 825), (265, 580), (390, 365)]
        
        shift_int = randint(0,8)
        runeset = shift_list_to_right(runeset, shift_int)
        arrow_turn_degrees = shift_int * -40

        for index, rune in enumerate(runeset):
            rune = Image.open(f"./assets/utility_assets/runes/{rune}.png")
            return_img.paste(rune, cordinates[index], rune) #param 1: image to paste, param 2: xy, param 3: mask >:))

        arrow = arrowa.rotate(arrow_turn_degrees, center=(745, 775))
        return_img.paste(arrow, (0, 0), arrow)
        return_img_draw = ImageDraw.Draw(return_img)
        return_img_draw.text((30, 30), f"Level {level}", fill=(0, 0, 0), font=myFont)
        return_img.save(f"./assets/utility_assets/runedial_output/Level_{level}.png", quality=95)

        print("Done!")

    print("All runedial generations successful!")


def save_to_json(solution_data):
    exec_path="./assets/main_assets/json/solution.json"
    human_path = "./output/solution.json"
    with open(exec_path, "w") as exec_file:
        json.dump(solution_data["solution"], exec_file)
    with open(human_path, "w") as human_file:
        json.dump(solution_data["solution"], human_file, indent=4)

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS # type: ignore
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def generate_main_exe_file():
    icon_path = resource_path("./assets/main_assets/icon.ico")
    asset_folder_path = resource_path("./assets/main_assets")
    script_path = resource_path("./main.py")
    command = f'pyinstaller  --noconfirm --onefile --windowed --name "Mad Mages Puzzle Door" --distpath "output" --specpath "output/TEMP" --workpath "output/TEMP" --add-data "{asset_folder_path};./assets/main_assets/" --icon "{icon_path}" "{script_path}"' 
    os.system(command)

if __name__ == "__main__":

    print("Generating random level order runesets... ", end="", flush=True)
    runedial_dict = generate_random_order(name="level_order")
    print("Done!")

    print("Generating a runedial positions... ", end="", flush=True)
    runedial_dict_complete = generate_runedial_positions(runedial_dict)
    print("Done!")

    print("Generating Runeset Images:")
    generate_runedials(runedial_dict_complete)

    print("Saving solution to json... ", end="", flush=True)
    save_to_json(runedial_dict_complete)
    print("Done")

    print("Generating .exe file...", end="", flush=True)
    generate_main_exe_file()
    print("Done!")

    print("All generation completed!")