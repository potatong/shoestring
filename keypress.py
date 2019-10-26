from keyboard import *
import socket
import time

HOST = '127.0.0.1'
PORT = 65432


def zoom_in():
    SendInput(Keyboard(VK_CONTROL), Keyboard(VK_OEM_PLUS))
    time.sleep(0.2)
    SendInput(Keyboard(VK_CONTROL, KEYEVENTF_KEYUP))
    SendInput(Keyboard(VK_OEM_PLUS, KEYEVENTF_KEYUP))


def zoom_out():
    SendInput(Keyboard(VK_CONTROL), Keyboard(VK_OEM_MINUS))
    time.sleep(0.2)
    SendInput(Keyboard(VK_OEM_PLUS, KEYEVENTF_KEYUP))
    SendInput(Keyboard(VK_CONTROL, KEYEVENTF_KEYUP))


def up():
    SendInput(Keyboard(VK_UP))
    time.sleep(0.2)
    SendInput(Keyboard(VK_UP, KEYEVENTF_KEYUP))


def down():
    SendInput(Keyboard(VK_DOWN))
    time.sleep(0.2)
    SendInput(Keyboard(VK_DOWN, KEYEVENTF_KEYUP))


def left():
    SendInput(Keyboard(VK_LEFT))
    time.sleep(0.2)
    SendInput(Keyboard(VK_LEFT, KEYEVENTF_KEYUP))


def right():
    SendInput(Keyboard(VK_RIGHT))
    time.sleep(0.2)
    SendInput(Keyboard(VK_RIGHT, KEYEVENTF_KEYUP))


def clockwise():
    SendInput(Keyboard(VK_SHIFT), Keyboard(VK_CONTROL), Keyboard(VK_OEM_PLUS))
    time.sleep(0.2)
    SendInput(Keyboard(VK_OEM_PLUS, KEYEVENTF_KEYUP))
    SendInput(Keyboard(VK_CONTROL, KEYEVENTF_KEYUP))
    SendInput(Keyboard(VK_SHIFT, KEYEVENTF_KEYUP))


def anticlockwise():
    SendInput(Keyboard(VK_SHIFT), Keyboard(VK_CONTROL), Keyboard(VK_OEM_MINUS))
    time.sleep(0.2)
    SendInput(Keyboard(VK_OEM_MINUS, KEYEVENTF_KEYUP))
    SendInput(Keyboard(VK_CONTROL, KEYEVENTF_KEYUP))
    SendInput(Keyboard(VK_SHIFT, KEYEVENTF_KEYUP))


def previous_page():
    SendInput(Keyboard(VK_PRIOR))
    time.sleep(0.2)
    SendInput(Keyboard(VK_PRIOR, KEYEVENTF_KEYUP))


def next_page():
    SendInput(Keyboard(VK_NEXT))
    time.sleep(0.2)
    SendInput(Keyboard(VK_NEXT, KEYEVENTF_KEYUP))


def zoom_fit_to_width():
    SendInput(Keyboard(VK_CONTROL), Keyboard(KEY_3))
    time.sleep(0.2)
    SendInput(Keyboard(KEY_3, KEYEVENTF_KEYUP))
    SendInput(Keyboard(VK_CONTROL, KEYEVENTF_KEYUP))


def zoom_fit_to_page():
    SendInput(Keyboard(VK_CONTROL), Keyboard(KEY_0))
    time.sleep(0.2)
    SendInput(Keyboard(KEY_0, KEYEVENTF_KEYUP))
    SendInput(Keyboard(VK_CONTROL, KEYEVENTF_KEYUP))


def run_command(cmd):
    commands = {
        "in": zoom_in,
        "out": zoom_out,
        "up": up,
        "down": down,
        "left": left,
        "right": right,
        "clockwise": clockwise,
        "anticlockwise": anticlockwise,
        "previous": previous_page,
        "next": next_page,
        "width": zoom_fit_to_width,
        "page": zoom_fit_to_page
    }
    try:
        commands[cmd]()
    except KeyError:
        pass


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        print("Connection established.")
        with conn:
            while True:
                data = conn.recv(1024)
                cmd = data.decode('utf-8').rstrip().lower()
                print(cmd)
                run_command(cmd)


if __name__ == '__main__':
    main()
