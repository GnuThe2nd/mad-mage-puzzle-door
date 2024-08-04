import tkinter as tk


def create_rune_memory():  # Rune memory creation
    rune_list = []
    for i in range(21):
        clicked_runes = []
        rune_list.append(clicked_runes)
    return rune_list


def show_frame(from_frame, to_frame):
    from_frame.forget()
    to_frame.tkraise()
    to_frame.pack()


def pyramid_generation():
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
        text="Found above, now down they rest, align them right to pass the test, to see depressed ruler's sorrowed cry, while Kaisarion stands by.",
        wraplength=190,
    )
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


def keypad_generation(frame):
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

    count = 0
    for i in range(3):
        for j in range(3):
            keypad_buttons[count].grid(row=i, column=j, padx=2, pady=2)
            count += 1

    keypad_return.grid(row=1, column=5)
    keypad_reset.grid(row=2, column=5)


def load_runes(image_name_list):
    returnlist = []
    for name in image_name_list:
        img = tk.PhotoImage(file="./src/Runes/Smaller_Runes/" + name + "resize.png")
        returnlist.append(img)
    return returnlist


def select(index, frame):
    frame_index = keypad_frame_list.index(frame)
    if len(rune_states[frame_index]) < 3:
        frame_children = frame.winfo_children()  # get frame children
        clicked_button = frame_children[index]  # Find the Button that was clicked
        clicked_button.config(state=tk.DISABLED)  # Disable the button
        rune_states[frame_index].append(index)  # Add rune index to memory

        frame_pyramid.winfo_children()[frame_index].config(bg="Turquoise")


def reset(frame):
    frame_index = keypad_frame_list.index(frame)
    frame_children = frame.winfo_children()
    for child in frame_children:
        child.config(state=tk.NORMAL)
    rune_states[frame_index].clear()

    frame_pyramid.winfo_children()[frame_index].config(bg="Gray")


def solve(current_solution, solution):
    if current_solution == solution:
        show_frame(frame_pyramid, frame_unlock)
    else:
        for i in range(21):
            if current_solution[i] == solution[i]:
                button = frame_pyramid.winfo_children()[i]
                button.config(state=tk.DISABLED)
                button.config(bg="green")


def generate_solution():
    solution = []
    for i in range(21):
        solution_part = [0, 1, 2]
        solution.append(solution_part)
    return solution


# Basic Setup
main = tk.Tk()
main.title("Mad Mages Puzzle Door")
main.geometry("700x420")
main.resizable(False, False)
main.iconbitmap("./src/icon.ico")

solution = generate_solution()

# creates images for the runes
rune_images = load_runes(
    [
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
)

# creates memory for every door frame
rune_states = create_rune_memory()

# Create pyramid frame and populate
frame_pyramid = tk.Frame(main)
frame_pyramid.pack()
pyramid_generation()

# create keypad frames and populate
keypad_frame_list = []
for index in range(21):
    new_frame = tk.Frame(main)
    keypad_generation(new_frame)
    keypad_frame_list.append(new_frame)

# create unlock frame and populate
frame_unlock = tk.Frame(main)
quit_button = tk.Button(
    frame_unlock, text="The giant door opens slowly...", command=lambda: main.destroy()
)
quit_button.pack(ipadx=5, ipady=5, expand=True, side="top")
# Main Loop
frame_pyramid.tkraise()
main.mainloop()
