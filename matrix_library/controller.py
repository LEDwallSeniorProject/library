# Keyboard to controller mappings:
# -------------------------------
#
#  |   Q   |          |   E   |
#
#     ---                ---
#    | W |              | I |
#  --     --        ---  ---  ---
# | A     D |      | J |     | L |
#  --     --        ---  ---  ---
#    | S |              | K |
#     ---                ---

import time
import re
import platform
from threading import Thread

# TODO: change this to make it like the others
# Detection of Platform for import
if re.search("armv|aarch64", platform.machine()) and re.search(
    "csledpi", platform.node()
):
    from evdev import InputDevice, categorize, ecodes
    import asyncio

    mode = "board"

else:
    import pygame
    import keyboard

    mode = "debug"


class Controller:
    def __init__(self):
        self.function_map = {}
        self.threads = []

        if mode == "board":
            while self.gamepad is None:
                try:
                    self.gamepad = InputDevice("/dev/input/event2")
                except:
                    print("No gamepad found")
                    time.sleep(1)
            self.button_map = {
                "LB": 37,
                "RB": 50,
                "UP": 46,
                "DOWN": 32,
                "LEFT": 18,
                "RIGHT": 33,
                "A": 34,
                "B": 36,
                "Y": 23,
                "X": 35,
            }
        else:
            self.button_map = {
                "LB": "q",
                "RB": "e",
                "UP": "w",
                "DOWN": "s",
                "LEFT": "a",
                "RIGHT": "d",
                "A": "l",
                "B": "k",
                "Y": "j",
                "X": "i",
            }

    def add_function(self, button, function):
        if mode == "board":
            t = Thread(target=self.worker, args=(button, function), daemon=True)
            t.start()
            print(f"Thread started: {button}")
            self.threads.append(t)
        else:
            print(f"Key: {self.button_map[button]}")
            keyboard.add_hotkey(self.button_map[button], function)

    def worker(self, button, function):
        while True:
            for event in self.gamepad.read_loop():
                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)
                    if (
                        key_event.keycode == self.button_map[button]
                        and key_event.keystate == key_event.key_down
                    ):
                        print("running function")
                        function()

    def check_key_presses(self):
        if mode == "board":
            for event in self.gamepad.read_loop():
                if event.type == ecodes.EV_KEY:
                    if event.value == 1:
                        if event.code in self.button_map.values():
                            try:
                                self.function_map[event.code]()
                            except:
                                pass
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in self.button_map.values():
                        try:
                            self.function_map[event.key]()
                        except:
                            pass
