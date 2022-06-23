try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("error loading launchpad.py")
import json
import os
from pygame import mixer
import webbrowser
import pystray
import PIL.Image
from threading import Thread


if launchpad.Launchpad().Check(0):
    lp = launchpad.Launchpad()
    if lp.Open(0):
        print("Launchpad Mk1/S/Mini")
else:
    print("Launchpad not available")
    exit()


COMMANDS = {}
CURRENT_PAGE = 1
CURRENT_BUTTON_SOUND = [-1,-1]
SOUND_IS_PAUSED = False
STOP = False


def read_commands():
    global COMMANDS
    global CURRENT_PAGE
    with open("commands.json", 'r') as file:
        COMMANDS = json.load(file)
        CURRENT_PAGE = COMMANDS["Current Page"]

def delete_buttons():
    lp.ButtonFlush()
    lp.Reset()

def draw_buttons():
    delete_buttons()
    commands = COMMANDS[f"Page {CURRENT_PAGE}"]
    lp.LedCtrlXY(CURRENT_PAGE-1,0, 0, 1)
    for key in commands:
        if commands[key]["color"] == "green":
            lp.LedCtrlXY(int(key.split(",")[0]),int(key.split(",")[1])+1, 0, 1)
        elif commands[key]["color"] == "yellow":
            lp.LedCtrlXY(int(key.split(",")[0]),int(key.split(",")[1])+1, 1, 1)
        elif commands[key]["color"] == "red":
            lp.LedCtrlXY(int(key.split(",")[0]),int(key.split(",")[1])+1, 1, 0)
    lp.LedCtrlXY(8,1,0,1)
    lp.LedCtrlXY(8,2,0,1)
    lp.LedCtrlXY(8,3,0,1)
    lp.LedCtrlXY(8,7,1,0)
    lp.LedCtrlXY(8,8,0,1)

def change_current_page(new_page):
    commands = {}
    with open("commands.json", 'r') as file:
        commands = json.load(file)
    commands["Current Page"] = new_page
    with open("commands.json", 'w') as file:
        json.dump(commands, file)
    read_commands()
    draw_buttons()

def button_press(button):
    read_commands()
    if f"{button[0]},{button[1]}" in COMMANDS[f"Page {CURRENT_PAGE}"]:
        command = COMMANDS[f"Page {CURRENT_PAGE}"][f"{button[0]},{button[1]}"]["command"]
        path = COMMANDS[f"Page {CURRENT_PAGE}"][f"{button[0]},{button[1]}"]["path"]
        color = COMMANDS[f"Page {CURRENT_PAGE}"][f"{button[0]},{button[1]}"]["color"]
        if command == "play":
            global CURRENT_BUTTON_SOUND

            if CURRENT_BUTTON_SOUND == button:
                toggle_sound()
            else:
                CURRENT_BUTTON_SOUND = button
                play_sound(path)
        elif command == "start":
            start_app(path)
        elif command == "search":
            search_link(path)

def play_sound(path):
    stop_sound()
    global SOUND_IS_PAUSED
    SOUND_IS_PAUSED = False
    mixer.music.load(path)
    mixer.music.play()
def stop_sound():
    global SOUND_IS_PAUSED
    CURRENT_BUTTON_SOUND = [-1,-1]
    SOUND_IS_PAUSED = False
    mixer.music.stop()
    draw_buttons()
def toggle_sound():
    global SOUND_IS_PAUSED
    global BLINKING
    if SOUND_IS_PAUSED:
        BLINKING = True
        mixer.music.unpause()
    else:
        BLINKING = False
        mixer.music.pause()
        draw_buttons()
    SOUND_IS_PAUSED = not SOUND_IS_PAUSED

def adjust_volume(higher, amount):
    read_commands()
    global COMMANDS
    current_volume = COMMANDS["Current Volume"]
    if higher:
        current_volume += amount
        if current_volume > 2:
            current_volume = 2
    else:
        current_volume -= amount
        if current_volume < 0:
            current_volume = 0
    current_volume = round(current_volume, 1)
    COMMANDS["Current Volume"] = current_volume
    mixer.music.set_volume(current_volume)
    with open("commands.json", 'w') as file:
        json.dump(COMMANDS, file)




def start_app(path):
    os.startfile(path)

def search_link(link):
    webbrowser.get().open(link, new=2)


def stray_icon_clicked(icon, item):
    if str(item) == "Open Settings":
        start_app("./settings.exe")
    elif str(item) == "Exit":
        icon.stop()
        global STOP
        STOP = True

def stray_icon():
    stray_image = PIL.Image.open("images/GreenCircleBtn.png")
    icon = pystray.Icon("Controll Pad", stray_image, menu=pystray.Menu(
        pystray.MenuItem("Open Settings", stray_icon_clicked),
        pystray.MenuItem("Exit", stray_icon_clicked)

    ))
    icon.run()
    


mixer.init()
mixer.music.set_volume(1)

read_commands()
draw_buttons()

# buts = lp.ButtonStateXY()             Use in whileloop, gets currently pressed button and state [x, y, bool]
# lp.ButtonFlush()                      Flushes all the buttons
# lp.LedCtrlXY(x, y, red, green)        Controls the collor of a button, (1,1) is orange, the circle buttons can't be green

adjust_volume(True, 0)

stray_thread = Thread(target=stray_icon)
stray_thread.start()

while True:
    if STOP:
        break
    buts = lp.ButtonStateXY()
    if buts:
        if not buts[-1]: # On button release
            buts = buts[0:2]
            if buts[1] == 0:
                stop_sound()
                change_current_page(buts[0]+1)
                continue
            if buts[0] == 8:
                button = buts[1]
                if button == 1:
                    adjust_volume(True, 0.1)
                elif button == 2:
                    adjust_volume(False, 0.1)
                elif button == 3:
                    stop_sound()
                elif button == 5:
                    pass
                elif button == 6:
                    pass
                elif button == 7:
                    break
                elif button == 8:
                    start_app("./settings.exe")
                    pass
                continue
            buts[1] -= 1
            button_press(buts)
            continue
            
stray_thread.join()
lp.Reset()  # turn all LEDs off
lp.Close()  # close the Launchpad (will quit with an error due to a PyGame bug)