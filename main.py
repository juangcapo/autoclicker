import time
import threading
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Listener, Key, KeyCode

mouse = MouseController()
keyboard = KeyboardController()
DELAY = 0.1  # seconds between clicks

alt_held = False
holding = False
w_held = False

class Clicker(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.running = False
        self.alive = True

    def run(self):
        while self.alive:
            while self.running:
                mouse.click(Button.left)
                time.sleep(DELAY)
            time.sleep(0.05)

clicker = Clicker()
clicker.start()

def normalize(key):
    if isinstance(key, KeyCode) and key.char:
        return key.char.lower()
    return None

def release_mouse():
    global holding
    if holding:
        mouse.release(Button.left)
        holding = False

def release_w():
    global w_held
    if w_held:
        keyboard.release('w')
        w_held = False

def on_press(key):
    global alt_held, holding, w_held
    if key in (Key.alt, Key.alt_l, Key.alt_r, Key.alt_gr):
        alt_held = True
        return
    if not alt_held:
        return

    if key == Key.up:
        if w_held:
            release_w()
            print("W released")
        else:
            keyboard.press('w')
            w_held = True
            print("W holding")
        return

    c = normalize(key)
    if c == 't':
        release_mouse()
        clicker.running = not clicker.running
        print("clicking" if clicker.running else "stopped")
    elif c == 'f':
        if holding:
            release_mouse()
            print("released")
        else:
            clicker.running = False
            mouse.press(Button.left)
            holding = True
            print("holding")
    elif c == 'q':
        clicker.running = False
        release_mouse()
        release_w()
        print("stopped")

def on_release(key):
    global alt_held
    if key in (Key.alt, Key.alt_l, Key.alt_r, Key.alt_gr):
        alt_held = False

print("Alt+T toggle | Alt+F hold click | Alt+Up hold W | Alt+Q stop | Ctrl+C to exit")

try:
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
except KeyboardInterrupt:
    clicker.alive = False
    clicker.running = False
    release_mouse()
    release_w()