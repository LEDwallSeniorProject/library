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
import logging

# TODO: change this to make it like the others
# Detection of Platform for import
if re.search("armv|aarch64", platform.machine()) and re.search(
    "csledpi", platform.node()
):
    import asyncio, evdev
    mode = "board"

else:
    import keyboard, pygame
    mode = "workstation"

class Controller:
    def __init__(self):
        self.function_map = {}
        self.debug = True

        # setup the LEDwall with evdev for controller inputs
        if mode == "board":
            while self.gamepad is None:
                try:
                    # autodetection of gamepad
                    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
                    if(len(devices) > 0):
                        self.gamepad = evdev.InputDevice(devices[0].path)
                except:
                    logging.debug("No gamepad found") if self.debug
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

            # setup evdev async/await functions
            asyncio.ensure_future(self._gamepad_event(self.gamepad))
            self.loop = asyncio.get_event_loop()
            self.loop.run_forever()

        # setup workstation mode with pygame and keyboard input
        elif mode == "workstation":
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

    # asyncio gamepad_event function -- internal use only
    async def _gamepad_events(self,device):
        async for event in device.async_read_loop():
            logging.debug(f"_gamepad_events", device.path, evdev.categorize(event), sep=': ') if self.debug

            if event.type == evdev.ecodes.EV_KEY:
                    key_event = evdev.categorize(event)
                    if (key_event.keystate == key_event.key_down or 
                        key_event.keystate == key_event.key_hold):
                            button = list(self.button_map.keys())[list(self.button_map.values()).index(key_event.keycode)]

                            logging.debug(f"_gamepad_events: button {button} function {self.function_map[button]["functionName"]}") if self.debug
                            self.function_map[button]["function"]()

    def add_function(self, button, function):
        if mode == "board":
            self.function_map[button] = {
                "functionName":  function,
                "function": globals().get(function),
                "button": button,
            }

        elif mode == "workstation":
            logging.debug(f"Key: {self.button_map[button]}") if self.debug
            keyboard.add_hotkey(self.button_map[button], function)

        else:
            logging.warning(f"Unhandled mode: {mode}, button: {button}, function: {function}")
