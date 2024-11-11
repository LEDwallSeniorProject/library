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

try:
    from evdev import InputDevice, categorize, ecodes
    import asyncio

    mode = "board"
except:
    import pygame

    mode = "debug"


class Controller:
    def __init__(self):
        self.function_map = {}

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
                "LB": pygame.K_q,
                "RB": pygame.K_e,
                "UP": pygame.K_w,
                "DOWN": pygame.K_s,
                "LEFT": pygame.K_a,
                "RIGHT": pygame.K_d,
                "A": pygame.K_l,
                "B": pygame.K_k,
                "Y": pygame.K_j,
                "X": pygame.K_i,
            }

    def add_function(self, button, function):
        self.function_map[self.button_map[button]] = function

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
