import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
from threading import Thread
import time
from functools import partial
import json

window = tk.Tk()

CURRENT_PAGE = 1
COMMANDS = {}
with open("commands.json", 'r') as file:
    COMMANDS = json.load(file)


# Setting up the default settings on the window
window.title("Controll Pad")
window.geometry("500x500")
window.resizable(False, False) 
window.configure(bg="black")
# The Button Frame
frame = tk.Frame(window)
frame.pack(side="top", expand=True, fill="both")
# The background image
backgroundImage = tk.PhotoImage(file="images/BackgroundImage.png")
whiteSquareBtnImage = tk.PhotoImage(file="images/WhiteSquareBtn.png")
greenSquareBtnImage = tk.PhotoImage(file="images/GreenSquareBtn.png")
yellowSquareBtnImage = tk.PhotoImage(file="images/YellowSquareBtn.png")
redSquareBtnImage = tk.PhotoImage(file="images/RedSquareBtn.png")

whiteCircleBtnImage = tk.PhotoImage(file="images/WhiteCircleBtn.png")
yellowCircleBtnImage = tk.PhotoImage(file="images/YellowCircleBtn.png")
greenCircleBtnImage = tk.PhotoImage(file="images/GreenCircleBtn.png")

def writeCommand(button, command, path, color):
    commands = readCommands()
    
    commands[f"Page {CURRENT_PAGE}"][f"{button[0]},{button[1]}"] = {
        "command": command,
        "path": path,
        "color": color
    }
    COMMANDS = commands
    with open("commands.json", 'w') as file:
        json.dump(commands, file)

    refresh_buttons()

def readCommands():
    global COMMANDS
    commands = {}
    with open("commands.json", 'r') as file:
        commands = json.load(file)
    COMMANDS = commands
    return commands

def deleteCommand(button):
    commands = {}
    with open("commands.json", 'r') as file:
        commands = json.load(file)
    
    commands[f"Page {CURRENT_PAGE}"].pop(f"{button[0]},{button[1]}", None)
    COMMANDS = commands

    with open("commands.json", 'w') as file:
        json.dump(commands, file)

    refresh_buttons()

def buttonClickEvent(button):
    global CURRENT_PAGE
    if type(button) == type([]):
        readCommands()
        button_is_used = button in getUsedButtonsThisPage()
        path = ""
        command = ""
        if button_is_used:
            print(COMMANDS)
            command = COMMANDS[f"Page {CURRENT_PAGE}"][f"{button[0]},{button[1]}"]["command"]
            path = COMMANDS[f"Page {CURRENT_PAGE}"][f"{button[0]},{button[1]}"]["path"]
            if "/" in path and not path.startswith("http://"):
                path = path.split("/")[-1]
        color = "green"
        # if color_answer:
        #     if color_answer == 1:
        #         color = "green"
        #     elif color_answer == 2:
        #         color = "yellow"
        #     elif color_answer == 3:
        #         color = "red"
        # else:
        #     print("Operation cancelled by user")
        #     return 0

        answer = simpledialog.askinteger(f"The button is already used to {command} {path}", "1 - Play an mp3 file, 2 - open an .exe file, 3 - search in a browser, 4 - delete command", parent=window, minvalue=1, maxvalue=4)
        if answer == 1:
            color = "green"
            filename = filedialog.askopenfilename(parent=window, initialdir='/', title="Select a music file", filetypes=[("MP3", "*.mp3")])
            if filename:
                print("Adding a command to play an mp3 file ", filename, button)
                writeCommand(button, "play", filename, color)
            else:
                print("Failed to get a file path")
        elif answer == 2:
            color = "red"
            filename = filedialog.askopenfilename(parent=window, initialdir='/', title="Select an executable file", filetypes=[("EXE", "*.exe")])
            if filename:
                print("Adding a command to open an executable ", filename, button)
                writeCommand(button, "start", filename, color)
            else:
                print("Failed to get a file path")
        elif answer == 3:
            color = "yellow"
            link = simpledialog.askstring("Input", "Write the url here", parent=window)
            if link:
                print("Adding a command to search for a link ", link, button)
                writeCommand(button, "search", link, color)
            else:
                print("Failed to get the link")
        elif answer == 4 and button_is_used:
            answer = messagebox.askyesno("Do You Want To Continue", f"This button is used to {command} {path}. The command will be deleted.")
            if answer:
                deleteCommand(button)
                print("Deleting a command from", button)
            else:
                print("Operation cancelled by user")
                return 0
        else:
            print("Operation cancelled by user")
    elif type(button) == type(1):
        CURRENT_PAGE = button
        refresh_buttons()
        print("Change the page to number ", button)
    elif type(button) == type('a'):
        if button == 'A':
            messagebox.showinfo("Special Button A", "This button is used to raise the volume of the sounds")
        if button == 'B':
            messagebox.showinfo("Special Button B", "This button is used to lower the volume of the sounds")
        if button == 'C':
            messagebox.showinfo("Special Button C", "This button is used to stop all sounds from playing")
        if button == 'F':
            messagebox.showinfo("Special Button F", "This button is used to Refresh the Launchpad Buttons")
        if button == 'G':
            messagebox.showinfo("Special Button G", "This button is used to open these settings")
        if button == 'H':
            messagebox.showinfo("Special Button H", "This button is used to exit the Controll Pad")
        print("Special command")

def getButtonColor(button):
    commands = readCommands()[f"Page {CURRENT_PAGE}"]
    if f"{button[0]},{button[1]}" in commands:
        return commands[f"{button[0]},{button[1]}"]["color"]
    return "green"

def getUsedButtonsThisPage():
    used_buttons = []
    commands = {}
    with open("commands.json", 'r') as file:
        commands = json.load(file)
    COMMANDS = commands

    for command in commands[f"Page {CURRENT_PAGE}"]:
        buttonPos = [int(command.split(',')[0]), int(command.split(',')[1])]
        used_buttons.append(buttonPos)


    return used_buttons

def draw_buttons():
    backgroundImageLabel = tk.Label(frame, image = backgroundImage, borderwidth=0)
    backgroundImageLabel.place(x=0,y=0)

    used_buttons = getUsedButtonsThisPage()

    for x in range(8): # Grid buttons
        for y in range(8):
            x_pos = 28+x*50
            y_pos = 82+y*50
            if x >= 5: # Becuase of misalignment, need to adjust positions of buttons by 1 pixel after 5th row and column.
                x_pos -= 1
            if y >= 5:
                y_pos -= 1
            btn = tk.Button(frame, height=41, width=41, bg="black", borderwidth=0, activebackground='black', command=partial(buttonClickEvent, [x,y]))
            if [x,y] in used_buttons:
                color = getButtonColor([x,y])
                if color == "green":
                    btn["image"] = greenSquareBtnImage
                elif color == "yellow":
                    btn["image"] = yellowSquareBtnImage
                elif color == "red":
                    btn["image"] = redSquareBtnImage
            else:
                btn["image"] = whiteSquareBtnImage
            btn.place(x=x_pos,y=y_pos)
    for x in range(8): # Page Buttons
        x_pos = 33+x*50
        y_pos = 38
        btn = tk.Button(frame, height=30, width=30, bg="black", borderwidth=0, activebackground='black', command=partial(buttonClickEvent, x+1))
        if x+1 == CURRENT_PAGE:
            btn["image"] = greenCircleBtnImage
        else:
            btn["image"] = whiteCircleBtnImage
        btn.place(x=x_pos,y=y_pos)
    letters = "ABCDEFGH"
    for x in range(8): # Letter Buttons
        x_pos = 430
        y_pos = 87+x*50
        if x >= 6:
            y_pos -= 3
        tk.Button(frame, height=30, width=30, image=whiteCircleBtnImage, bg="black", borderwidth=0, activebackground='black', command=partial(buttonClickEvent, letters[x])).place(x=x_pos,y=y_pos)

def delete_buttons():
    for widgets in frame.winfo_children():
        widgets.destroy()

def refresh_buttons():
    delete_buttons()
    draw_buttons()

draw_buttons()

window.mainloop()


