from PIL import Image, ImageDraw, ImageFont
from random import randint, choice, shuffle
import os
from math import ceil
import json


def scale_image(input_path, output_path, scale_factor):
    # Open an image file
    with Image.open(input_path) as img:
        # Get original dimensions
        original_size = img.size
        print(f"Original size: {original_size}")

        # Calculate the new size
        new_size = (
            int(original_size[0] * scale_factor),
            int(original_size[1] * scale_factor),
        )

        # Resize the image
        img_resized = img.resize(new_size)

        # Save the scaled image
        img_resized.save(output_path)
        print(f"Saved resized image to: {output_path}")


def scale_images_in_directory(input_dir, output_dir, scale_factor):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process all PNG files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".png"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            scale_image(input_path, output_path, scale_factor)


def generate_random_solution():
    # I The Arrow in the middle must point towards this Rune
    # II Always the rune 1 rune onward from the "Halaster" Rune
    # III A rune ((Level / 3) + 1) spots onwards from the II
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


def assign_door_to_level(dict): 
    random_level_order = []
    return_dict = {}
    return_solution = {}
    return_runeset = {}

    solution = dict["Solution"]
    runeset = dict["Runeset"]

    for i in range(22):
        if i != 5:
            random_level_order.append(i)
    shuffle(random_level_order)

    for i in random_level_order:
        return_solution[i] = solution[i]
        return_runeset[i] = runeset[i]

    return_dict["Runeset"] = return_runeset
    return_dict["Solution"] = return_solution

    return return_dict


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


def assign_runes_to_level():
    # I The Arrow in the middle must point towards this Rune
    # II Always the rune 1 rune onward from the "Halaster" Rune
    # III A rune ((Level / 3) rounded up) spots onwards from the II
    

    all_rune_states = [] 
    all_rune_solutions = []
    return_dict = {}
    index = 0

    while index != 21:
        index = len(all_rune_states)
        '''
        This part below simulates the III rule of soliving the puzzle by doing the calculations early. since, players look at levels 1-21, 
        not 0-20, like the program this part is just set up so that the 0 gets rounded to 1 and 20 gets rounded to 5
        '''
        third_rune_step = max(ceil(index / 5), 1)
        if index == 20:
            third_rune_step = 5


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
        while x < 20:
            result_copy = result.copy()

            '''
            The first is an attempt to fix an edgecase. 
            
            "II Always the rune 1 rune onward from the "Halaster" Rune"
            This means that the second rune can never be "Halaster" rune, since every rune in list is unique.
            Furthermore, if the first rune is "Halaster", then the second rune must be placed next to it.
            '''

            if first_rune == "Halaster":
                asukoht = 1
            else:
                asukoht = randint(2, 8)

            result_copy[asukoht] = second_rune  # assign the second rune
            result_copy[asukoht - 1] = "Halaster" # type: ignore # assign the spot to its left to "Halaster" Rune

            third_placement_index = asukoht + third_rune_step
            if third_placement_index != 9: # all runes are unique, the third rune cannot be itself/the second rune
                third_placement_index -= 9 # a list can iterate into the negative, we dont need to check if number is  higher then 9

                if (result_copy[third_placement_index] == True and third_rune not in result_copy):
                    result_copy[third_placement_index] = third_rune # assign the third rune

                    return_runeset = replace_missing_runes(result_copy)

                    all_rune_states.append(return_runeset) # Add the result to both returnlists
                    all_rune_solutions.append(solution)

                    break

            x += 1
        if x == 20:
            all_rune_states = "See solution ei sobi." 
            # I didnt bother to math it out, if its possible to not find a solution, so this is here just incase.
            break
        
    return_dict["Runeset"] = all_rune_states
    return_dict["Solution"] = all_rune_solutions        
    return return_dict


def shift_list_to_right(lst, index):
    index = index % len(lst)
    return lst[-index:] + lst[:-index]


def place_runes_onto_dials(runedials_dict):
    myFont = ImageFont.truetype('arial.ttf', 150)
    arrowa = Image.open("./assets/utility_assets/Arrow.png")

    for index, runeset_key in enumerate(runedials_dict.keys()):
        background_img = Image.open("./assets/utility_assets/door_puzzle_templates/" + str(index + 1) + ".png" )
        return_img = background_img.copy()

        runeset = runedials_dict[runeset_key]
        cordinates = [(618, 270), (850, 353), (970, 580), 
                      (930, 825), (745, 990), (495, 990), 
                      (310, 825), (265, 580), (390, 365)]
        
        shift_int = randint(0,8)
        shift_list_to_right(runeset, shift_int)
        arrow_turn_degrees = shift_int * -40

        for jndex, rune in enumerate(runeset):
            rune = Image.open("./assets/utility_assets/runes/" + rune + ".png")
            return_img.paste(rune, cordinates[jndex], rune) #param 1: image to paste, param 2: xy, param 3: mask >:))

        arrow = arrowa.rotate(arrow_turn_degrees, center=(744, 774))
        return_img.paste(arrow, (0, 0), arrow)
        return_img_draw = ImageDraw.Draw(return_img)
        return_img_draw.text((30, 30), "Level " + str(runeset_key + 1), fill=(0, 0, 0), font=myFont)
        return_img.save("./assets/utility_assets/runedial_output/Level_" + str(runeset_key+1) + '.png', quality=95)


def save_to_json(solution_data, filename="./assets/main_assets/json/solution.json"):
    with open(filename, "w") as json_file:
        json.dump(solution_data, json_file, indent=4)


input_directory = "./assets/utility_assets"
output_directory = "./assets/utility_assets"
scale_factor = 0.3

#scale_images_in_directory(input_directory, output_directory, scale_factor)

runedial_dict = assign_runes_to_level()
organised_runedial_dict = assign_door_to_level(runedial_dict)
place_runes_onto_dials(organised_runedial_dict["Runeset"])
save_to_json(organised_runedial_dict["Solution"])