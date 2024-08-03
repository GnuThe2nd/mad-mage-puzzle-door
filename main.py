import tkinter as tk
from PIL import Image


def create_rune_memory():  # Rune memory creation
    rune_list = []
    for i in range(21):
        rune_dict = {}
        rune_dict["solved"] = False
        rune_dict["color"] = "gray"
        rune_dict["selected_runes"] = []
        for rune_id in range(9):
            rune_dict[rune_id] = True
        rune_list.append(rune_dict)
    return rune_list


def buttons_page():  # Pyramid buttons creation
    global buttons
    buttons = []
    for button_name in range(21):
        button = tk.Button(
            main,
            bg=rune_states[button_name]["color"],
            fg="black",
            padx=10,
            pady=5,
            height=3,
            width=5,
            command=lambda m=button_name: clear_page(
                go_to="keypad", pyramid_placement=m
            ),
        )
        buttons.append(button)

    unlock_button = tk.Button(
        main,
        bg="gray",
        fg="black",
        text="Unlock",
        padx=10,
        pady=5,
        height=4,
        width=7,
        command=lambda: solve(rune_states, generate_solution()),
    )

    # row 1
    buttons[0].grid(row=1, column=2, columnspan=2, padx=2, pady=2)

    # row 2
    buttons[1].grid(row=2, column=2, padx=2, pady=2)
    buttons[2].grid(row=2, column=3, padx=2, pady=2)

    # row 3
    buttons[3].grid(row=3, column=1, columnspan=2, padx=2, pady=2)
    buttons[4].grid(row=3, column=2, columnspan=2, padx=2, pady=2)
    buttons[5].grid(row=3, column=3, columnspan=2, padx=2, pady=2)

    unlock_button.grid(row=3, column=6, rowspan=2, padx=2, pady=2)
    # row 4
    buttons[6].grid(row=4, column=1, padx=2, pady=2)
    buttons[7].grid(row=4, column=2, padx=2, pady=2)
    buttons[8].grid(row=4, column=3, padx=2, pady=2)
    buttons[9].grid(row=4, column=4, padx=2, pady=2)

    # row 5
    buttons[10].grid(row=5, column=0, columnspan=2, padx=2, pady=2)
    buttons[11].grid(row=5, column=1, columnspan=2, padx=2, pady=2)
    buttons[12].grid(row=5, column=2, columnspan=2, padx=2, pady=2)
    buttons[13].grid(row=5, column=3, columnspan=2, padx=2, pady=2)
    buttons[14].grid(row=5, column=4, columnspan=2, padx=2, pady=2)

    # row 6
    buttons[15].grid(row=6, column=0, padx=2, pady=2)
    buttons[16].grid(row=6, column=1, padx=2, pady=2)
    buttons[17].grid(row=6, column=2, padx=2, pady=2)
    buttons[18].grid(row=6, column=3, padx=2, pady=2)
    buttons[19].grid(row=6, column=4, padx=2, pady=2)
    buttons[20].grid(row=6, column=5, padx=2, pady=2)


def button_keypad_page(pyramid_placement):  # Keypad buttons creation
    global keypad_buttons
    keypad_buttons = []
    for rune_number in range(9):
        button = tk.Button(
            main,
            bg="gray",
            fg="black",
            image=rune_images[rune_number],
            command=lambda m=rune_number, n=pyramid_placement: rune_choise_disable(
                m, n
            ),
            padx=10,
            pady=5,
            height=130,
            width=130,
        )
        if not rune_states[pyramid_placement][rune_number]:
            button.config(state=tk.DISABLED)

        keypad_buttons.append(button)

    keypad_reset = tk.Button(
        main,
        bg="gray",
        fg="black",
        text="Reset",
        command=lambda m=pyramid_placement: runes_reset(m),
        padx=10,
        pady=5,
        height=5,
        width=5,
    )
    keypad_return = tk.Button(
        main,
        bg="gray",
        fg="black",
        text="Return",
        command=lambda: clear_page(go_to="main"),
        padx=10,
        pady=5,
        height=5,
        width=5,
    )

    count = 0
    for i in range(3):
        for j in range(3):
            keypad_buttons[count].grid(row=i, column=j, padx=2, pady=2)
            count += 1

    keypad_return.grid(row=1, column=5)
    if not rune_states[pyramid_placement]["solved"]:
        keypad_reset.grid(row=2, column=5)


def clear_page(go_to, pyramid_placement=0):
    for widget in main.winfo_children():
        widget.destroy()
    if go_to == "main":
        buttons_page()
    elif go_to == "keypad":
        button_keypad_page(pyramid_placement)
    elif go_to == "winner":
        exitpage = tk.Button(
            main,
            text="The giant door opens before you...",
            command=lambda: main.destroy(),
        )
        exitpage.pack(side=tk.TOP, expand=True)


def combine_and_save(image_list):
    dst = Image.new(
        "RGB",
        (
            image_list[0].width + image_list[1].width + image_list[2].width,
            image_list[0].height,
        ),
    )
    dst.paste(image_list[0], (0, 0))
    dst.paste(image_list[1], (image_list[0].width, 0))
    dst.paste(image_list[2], (image_list[0].width + image_list[1].width, 0))

    imagename = []
    for image in image_list:
        imagename.append(image.filename.split("Runes")[1][1:].strip(".png"))

    dst.save("src/Runes/Combinations/" + "_".join(imagename) + ".png")


def runes_resize(image_name_list, width, height):
    returnlist = []
    for image in image_name_list:
        image_type = Image.open("./src/Runes/" + image + ".png")
        resize_image = image_type.resize((width, height))
        resize_image.save("src/Runes/Smaller_Runes/" + image + "resize.png")


def load_runes(image_name_list):
    returnlist = []
    for name in image_name_list:
        img = tk.PhotoImage(file="./src/Runes/Smaller_Runes/" + name + "resize.png")
        returnlist.append(img)
    return returnlist


def rune_choise_disable(number, pyramid_placement):
    if len(rune_states[pyramid_placement]["selected_runes"]) < 3:
        keypad_buttons[number].config(state=tk.DISABLED)
        rune_states[pyramid_placement][number] = False
        rune_states[pyramid_placement]["color"] = "turquoise"
        rune_states[pyramid_placement]["selected_runes"].append(number)


def runes_reset(pyramid_placement):
    for rune_id, rune in enumerate(keypad_buttons):
        rune.config(state=tk.NORMAL)
        rune_states[pyramid_placement][rune_id] = True
    rune_states[pyramid_placement]["color"] = "gray"
    rune_states[pyramid_placement]["selected_runes"] = []


def solve(rune_current_state, solution):
    # convert current runes to a matrix
    current_solution = []
    for rune in rune_current_state:
        current_solution.append(rune["selected_runes"])

    # refresh page and turn tiles green, where solution was correct
    for number in range(21):
        if current_solution[number] == solution[number]:
            rune_states[number]["solved"] = True
            rune_states[number]["color"] = "Green"
            buttons_page()

    # check if solutions match
    if current_solution == solution:
        clear_page("winner")


def generate_solution():
    solution = []
    for i in range(21):
        solution_part = [0, 1, 2]
        solution.append(solution_part)
    return solution


# Basic Setup
main = tk.Tk()
main.title("Mad Mages Puzzle Door")
main.geometry("500x420")
main.resizable(False, False)
main.iconbitmap("./src/icon.ico")

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

solution = []

rune_images = load_runes(runes)  # creates images for the runes
rune_states = create_rune_memory()  # creates memory for every door frame

# Main Loop
buttons_page()
main.mainloop()
