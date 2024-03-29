from pyautocad import Autocad, APoint
import socket
import time
from functools import partial

# Connect python to AutoCAD
acad = Autocad() 
acad.prompt("Hello, Autocad from Python\n")
# acad.doc returns ActiveDocument: Returns a Document object that represents the the document with the focus. If there are no documents open, an error occurs.
print (acad.doc.Name)


# Our example command is to draw a line from (0,0) to (5,5)
# command_str = 'ucs z 90 '  # notice that the last SPACE is equivalent to hiting ENTER
# You should separate the command's arguments also with SPACE

# Send the command to the drawing
# acad.doc.SendCommand(command_str)


HOST = ''
PORT = 13000


def zoom(x):
    command_str = 'zoom ' + str(x) + ' '
    acad.doc.SendCommand(command_str)
    

def up(x):
    command_str = '-pan 0,' + str(x) + '  '
    acad.doc.SendCommand(command_str)
    

def down(x):
    command_str = '-pan 0,-' + str(x) + '  '
    acad.doc.SendCommand(command_str)


def left(x):
    command_str = '-pan -' + str(x) + ',0  '
    acad.doc.SendCommand(command_str)


def right(x):
    command_str = '-pan ' + str(x) + ',0  '
    acad.doc.SendCommand(command_str)
    

def clockwise(x):
    command_str = 'ucs z ' + str(x) + ' plan  '
    acad.doc.SendCommand(command_str)


def anticlockwise(x):
    command_str = 'ucs z -' + str(x) + ' plan  '
    acad.doc.SendCommand(command_str)


def zoom_fit():
    command_str = 'zoom O all  '
    acad.doc.SendCommand(command_str)


def run_command(cmd, x):
    commands = {
        "resume": partial(zoom,x),
        "zoom": partial(zoom, x),
        "app": partial(up, x),
        "up": partial(up, x),
        "down": partial(down, x),
        "left": partial(left, x),
        "write": partial(right, x),
        "right": partial(right, x),
        "clockwise": partial(clockwise, x),
        "anti-clockwise": partial(anticlockwise, x),
        "anticlockwise": partial(anticlockwise, x),
        "fit": zoom_fit
    }
    try:
        commands[cmd]()
    except KeyError:
        pass

def text_to_command(texts):
    commands = [
        "resume",
        "zoom",
        "app",
        "up",
        "down",
        "left",
        "right",
        "write",
        "clockwise",
        "anti-clockwise",
        "anticlockwise",
        "fit"
    ]
    
    numbers = {
        "one": 1,
        "want": 1,
        "1": 1,
        "two": 2,
        "too": 2,
        "to": 2,
        "2": 2,
        "three": 3,
        "tree": 3,
        "3": 3,
        "four": 4,
        "for": 4,
        "4": 4,
        "five": 5,
        "5": 5,
        "six": 6,
        "6": 6,
        "seven": 7,
        "7": 7,
        "eight": 8,
        "ate": 8,
        "8": 8,
        "nine": 9,
        "9": 9,
        "ten": 10,
        "tan": 10,
        "10": 10
    }

    for i, text in enumerate(texts):
        if text in commands:
            txtlist = texts[i+1:i+3]
            if text in ["clockwise", "anticlockwise", "anti-clockwise"]:
                x = 90
            elif text == "zoom":
                x = 1
            else:
                x = 50
            for txt in txtlist:
                try:
                    x = float(txt)
                    break
                except ValueError:
                    continue
            for number in numbers:
                if number in txtlist:
                    x = numbers[number]
                    break
            run_command(text, x)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    print("Connection established.")
    while True:
        data, addr = s.recvfrom(1024)
        texts = data.decode('utf-8').rstrip().lower().split()
        print(texts)
        text_to_command(texts)


if __name__ == '__main__':
    main()
