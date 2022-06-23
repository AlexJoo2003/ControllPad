# LaunchpadSoundboard
A launchpad MINI from Albeton Live is going to be used as a tool to do pre-specified commands. These commands include but are not limited to: Open an application, Play a sound through the microphone, or Search something on the internet.


# INSTALATION
#### Libraries included:
- webbrowser - for opening the default browser with a specified link
- json - all the commands with the specified arguments are going to be stored in a JSON file
- os - to launch any application with a specified path
- [FMMT666/launchpad.py](https://github.com/FMMT666/launchpad.py/blob/master/launchpad_py/launchpad.py) - to read and control inputs from the launchpad
- pygame - to play sounds
- tkinter - to create the GUI
- pystray - to be able to use the system tray
- pillow (PIL) - to make the icon in the system tray have an image

You can download the python files and run them with python as is. For that you would need to `pip install` all the libraries above and then simply run `py controllPad.py`

You could also compile it on your machine following these steps:
```
> git clone https://github.com/AlexJoo2003/ControllPad.git
> cd ControllPad
> pip install -U pyinstaller
> pyinstaller program.spec
> mv images/ dist/program/images/
> mv commands.json dist/program/commands.json
```
The folder in `dist` is going to contain all the necessary files. To run, double click the `controllPad.exe`.

# Usage
Once running, the `controllPad.exe` a green icon should appear in your system tray. You can right-click it to open settings, or just simply open `settings.exe`. In the settings, you will be presented with a grid of buttons following the layout of an Ableton Live's Launchpad Mini product. The top row are the pages, and the side row are special buttons, neither of them are configurable. The grid in the middle has square buttons, which upon click give the user 4 options: assign the button to play music, start an application, search the web or delete function. After properly following the instructions, the button will be assigned a function and will light up green/yellow/red.

![Preview](https://github.com/AlexJoo2003/ControllPad/blob/main/images/preview.png "Preview of the settings.exe")

In order to actually call the function, the Launchpad Mini needs to be connected to the computer, prior to running the application. Every time a new function has been assigned, the launchpad buttons can be refreshed by pressing the F button on the side, or by right-clicking the icon in the system tray and selecting "Refresh". Pressing any green buttons in the main grid will do the assigned function.

What the vertical row of buttons do (You can click on them in settings to view their function there too):
- A - raise the volume
- B - lower the volume
- C - stop the sound
- F - refresh the buttons
- G - launch `settings.exe`
- H - close `controllPad.exe`

# Play sounds so people in the call can hear it too

So far, only you will be able to listen to the sounds you play on the launchpad. In order to make it so everyone hears the sounds, you need to use Voicemeeter Banana and and CABLE Input. [This video on Youtube](https://www.youtube.com/watch?v=8c1LPeyVjdE) made by Tekh, describes how to use these tools to achieve this goal. In the end, instead of setting up your browser to be the source of sound, do that for the controllPad.exe and it will worl.

---
Tested only on Windows 10 and Python 3.9.6
So far only supports LaunchPad mini