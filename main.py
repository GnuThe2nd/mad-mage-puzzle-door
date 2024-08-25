import tkinter as tk
import json
import os, sys


def create_rune_memory(solution):  # Rune memory creation
    rune_list, correct_guesses = load_save_from_json()
    if rune_list == None:
        rune_list = {}
        correct_guesses = []
        for key in solution.keys():
            rune_list[key] = []
    return rune_list, correct_guesses


def show_frame(from_frame, to_frame):
    from_frame.forget()
    to_frame.tkraise()
    to_frame.pack()


def pyramid_generation(rune_states):
    buttons = []
    for i in range(21):
        button = tk.Button(
            frame_pyramid,
            bg="gray",
            fg="black",
            padx=10,
            pady=5,
            height=3,
            width=5,
            command=lambda m=i: show_frame(frame_pyramid, keypad_frame_list[m]),
        )
        buttons.append(button)

    unlock_button = tk.Button(
        frame_pyramid,
        bg="gray",
        fg="black",
        text="Unlock",
        padx=8,
        pady=5,
        height=3,
        width=7,
        command=lambda: solve(rune_states, solution),
    )

    poem_label = tk.Label(
        frame_pyramid,
        text="Keys from above, now down they rest, align them right to pass the test.        Solve with care, or fate you'll meet,       for those who err shall turn concrete.",
        wraplength=220,
    )

    pyramid_recoloring(buttons)

    # row 1
    buttons[0].grid(row=1, column=2, columnspan=2, padx=2, pady=2)

    poem_label.grid(row=2, column=6, rowspan=2)
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


def keypad_generation(frame, keydial_rune_states):
    keypad_buttons = []
    for rune_number in range(9):
        button = tk.Button(
            frame,
            bg="gray",
            fg="black",
            image=rune_images[rune_number],
            command=lambda m=rune_number, n=frame: select(m, n),
            padx=10,
            pady=5,
            height=130,
            width=130,
        )

        keypad_buttons.append(button)

    keypad_reset = tk.Button(
        frame,
        bg="gray",
        fg="black",
        text="Reset",
        command=lambda m=frame: reset(m),
        padx=10,
        pady=5,
        height=5,
        width=5,
    )
    keypad_return = tk.Button(
        frame,
        bg="gray",
        fg="black",
        text="Return",
        command=lambda: show_frame(frame, frame_pyramid),
        padx=10,
        pady=5,
        height=5,
        width=5,
    )

    # disabling keys, depending on save_data.json
    for key in keydial_rune_states:
        rune_index = runes.index(key)
        keypad_buttons[rune_index].config(state=tk.DISABLED)

    # putting keypad, reset and return on screen
    count = 0
    for i in range(3):
        for j in range(3):
            keypad_buttons[count].grid(row=i, column=j, padx=2, pady=2)
            count += 1

    keypad_return.grid(row=1, column=5)
    keypad_reset.grid(row=2, column=5)


def pyramid_recoloring(buttons):
    # re_coloring pyrimid panels, depending on if solved or not
    for i in range(21):
        j = i
        if i >= 5: #skip the number 5 cuz that layer dont exist homeboy this code sucks what oyu expect. Might refactor later
            j +=1
        if rune_states[str(j)] != []:
            buttons[i].config(bg="Turquoise")
       

    for solved in correct_guesses: # type: ignore
        button_thing = buttons[solved]
        button_thing.config(bg="green")
        button_thing.config(state=tk.DISABLED)


def load_runes(image_name_list):
    returnlist = []
    for name in image_name_list:
        img = tk.PhotoImage(
            file=resource_path("./assets/main_assets/runes/" + name + ".png")
        )
        returnlist.append(img)
    return returnlist


def select(index, frame):
    frame_index = keypad_frame_list.index(frame)
    if len(rune_states[str(frame_index)]) < 3:
        frame_children = frame.winfo_children()  # get frame children
        clicked_button = frame_children[index]  # Find the Button that was clicked
        clicked_button.config(state=tk.DISABLED)  # Disable the button
        rune_states[str(frame_index)].append(runes[index])  # Add rune index to memory
        frame_pyramid.winfo_children()[frame_index].config(bg="Turquoise") # type: ignore


def reset(frame):
    frame_index = keypad_frame_list.index(frame)
    frame_children = frame.winfo_children()
    for child in frame_children:
        child.config(state=tk.NORMAL)
    rune_states[str(frame_index)].clear()

    frame_pyramid.winfo_children()[frame_index].config(bg="Gray") # type: ignore


def solve(current_solution, solution):
    for i in range(21):
        if i >= 5:
            i += 1 
        if current_solution[str(i)] == solution[str(i)]:
            button = frame_pyramid.winfo_children()[i]
            button.config(state=tk.DISABLED) # type: ignore
            button.config(bg="green") # type: ignore
            if i not in correct_guesses: #type: ignore
                correct_guesses.append(i) # type: ignore
    if current_solution == solution:
        show_frame(frame_pyramid, frame_unlock)


def load_solution_from_json(filename="./assets/main_assets/json/solution.json"):
    try:
        with open(filename, "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None, None


def save_to_json(solution, correct_guesses, filename="save_data.json"):
    data = {"solution": solution, "correct_guesses": correct_guesses}
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)


def load_save_from_json(filename="save_data.json"):
    try:
        with open(filename, "r") as json_file:
            data = json.load(json_file)
        return data["solution"], data["correct_guesses"]
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None, None


def save_progress():
    save_to_json(rune_states, correct_guesses)
    main.destroy()


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS # type: ignore
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    # Basic Setup
    main = tk.Tk()
    main.title("Mad Mages Puzzle Door")
    main.geometry("700x420")
    main.resizable(False, False)
    main.iconbitmap(resource_path("./assets/main_assets/icon.ico"))

    background_img = tk.PhotoImage(file=resource_path("./assets/main_assets/main_background.png"))
    background_label = tk.Label(main, image=background_img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    number_1 = tk.PhotoImage(file=resource_path("./assets/main_assets/I.png"))
    

    solution = load_solution_from_json()
    print(solution)

    runes =[
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
    # creates images for the runes
    rune_images = load_runes(runes)

    # creates/loads memory for every keypad frame
    rune_states, correct_guesses = create_rune_memory(solution)

    # Create the pyramid frame and populate
    frame_pyramid = tk.Frame(main, background="")
    frame_pyramid.pack()
    pyramid_generation(rune_states)

    # create keypad frames and populate
    keypad_frame_list = []
    for index in range(21):
        if index >= 5:
            index = 1
        new_frame = tk.Frame(main, background="")
        keypad_generation(new_frame, rune_states[str(index)])
        keypad_frame_list.append(new_frame)

    # create door unlock frame and populate
    frame_unlock = tk.Frame(main)
    quit_button = tk.Button(
        frame_unlock,
        text="The giant door opens slowly...",
        command=lambda: save_progress(),
    )
    quit_button.pack(ipadx=5, ipady=5, expand=True, side="top")

    # Main Loop
    frame_pyramid.tkraise()
    main.protocol("WM_DELETE_WINDOW", lambda: save_progress())

    main.mainloop()
