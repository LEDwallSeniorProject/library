# Controller mappings:
# Player 1:                          Player 2:
#   | LB |              | RB |                 | LB2 |            | RB2 |
#
#       ---               ---                     ---               ---
#      | UP |            | X |                  | UP2 |            | X2 |
#  --           --     --     --             --          --     --       --
# | LEFT    RIGHT |   | Y     A |          | LEFT2    RIGHT2 | | Y2      A2 | 
#  --           --     --     --             --          --     --       --
#     | DOWN |           | B |                 | DOWN2 |           | B2 |
#       ---                                       ---               ---
#       SELECT      START                           SELECT2    START2

# Keyboard to controller mappings:
# -------------------------------
# Player 1:                          Player 2:
# | Q |            | E |             | U |           | O |
#
#     ---           ---                  ---          ---
#    | W |         | T |                | I |        | [ |
#  --     --     --     --            --     --    --     --
# | A     D |   | F     G |          | J     L |  | ;     ' | 
#  --     --     --     --            --     --    --     --
#    | S |         | V |                | K |        | / |
#     ---                                ---          ---
# SELECT: Z                           SELECT: M
# START:  C                           START: .

import copy
import time
import re
import platform
import logging
import threading

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
    def __init__(self, debug = False):

        # debug state
        self.debug = debug
        if self.debug: logging.basicConfig(level=logging.DEBUG)

        # map of functions for evdev
        self.function_map = {}

        # gamepad objects
        self.gamepad = None
        self.gamepad2 = None

        # variables for evdev loop thread
        self.t = None

        # setup the LEDwall with evdev for controller inputs
        if mode == "board":
            while self.gamepad is None:
                try:
                    # autodetection of gamepad
                    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
                    for device in devices:
                        logging.debug(f"{device.path}, {device.name}, {device.phys}")
                        if re.search("8BitDo Zero 2 gamepad", device.name):
                            if self.gamepad is None:
                                self.gamepad = evdev.InputDevice(device.path)
                            elif self.gamepad2 is None:
                                self.gamepad2 = evdev.InputDevice(device.path)
                            else:
                                logging.info(f"Two controllers already mapped. Skipping {device.path} - {device.name}")
                except:
                    logging.info("No gamepad found - sleeping 1 second") 
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
                "START": 24,
                "SELECT": 49,
            }

            # setup evdev async/await functions for gamepad1
            asyncio.ensure_future(self._gamepad_events(self.gamepad))
            if self.gamepad2 is not None: asyncio.ensure_future(self._gamepad_events(self.gamepad2))
            self.loop = asyncio.get_event_loop()
            self.t = threading.Thread(target=self._loop_thread, args=(self.loop,), daemon=True).start()

        # setup workstation mode with pygame and keyboard input
        elif mode == "workstation":
            self.button_map = {
                # controller for player one, use WASD and nearby keps
                "LB": "q",
                "RB": "e",
                "UP": "w",
                "DOWN": "s",
                "LEFT": "a",
                "RIGHT": "d",
                "A": "g",
                "B": "v",
                "Y": "f",
                "X": "t",
                "SELECT": "z",
                "START": "c",
                # controller for player two, use IJKL and nearby keys
                "LB2": "u",
                "RB2": "o",
                "UP2": "i",
                "DOWN2": "k",
                "LEFT2": "j",
                "RIGHT2": "l",
                "A2": "'",
                "B2": "/",
                "Y2": ";",
                "X2": "[",
                "SELECT2": "m",
                "START2": ".",
            }


        # debug output
        logging.debug(self.button_map)

    # asyncio gamepad_event function -- internal use only
    async def _gamepad_events(self,device):
        device_num = "1" if device is self.gamepad else "2"
        async for event in device.async_read_loop():
            #logging.debug(f"_gamepad_events {device_num}: {device.path} {evdev.categorize(event)}") 

            if event.type == evdev.ecodes.EV_KEY:
                    key_event = evdev.categorize(event)
                    if (key_event.keystate == key_event.key_down or 
                        key_event.keystate == key_event.key_hold):
                            if key_event.keycode in evdev.ecodes.ecodes:
                                # map key_event.keycode to integer number
                                logging.debug(f"_gamepad_events {device_num}: Integer keycode value: {evdev.ecodes.ecodes[key_event.keycode]}")
                                button_code = evdev.ecodes.ecodes[key_event.keycode]
                                # map the button_code integer number to the internal UP/DOWN/LEFT/RIGHT/etc
                                try:
                                    button = list(self.button_map.keys())[list(self.button_map.values()).index(button_code)]
                                    logging.debug(f"_gamepad_events {device_num}: button {button}")
                                except ValueError as v:
                                    logging.debug(f"_gamepad_events {device_num}: button_code {button_code} not recognized.")
                                    next

                                # if on the second gamepad, update the button to the "<blah>2" button
                                if int(device_num) == 2:
                                    origbutton = copy.deepcopy(button)
                                    button = f"{button}2"
                                    logging.debug(f"_gamepad_events {device_num}: button {origbutton} remapped to {button}")

                                # check to see if a mapped function exists for that
                                if button in self.function_map:
                                    logging.debug(f"_gamepad_events {device_num}: button {button} calls function {self.function_map[button]['function']}")
                                    self.function_map[button]["function"]()
                                else:
                                    logging.debug(f"_gamepad_events {device_num}: button {button} is not mapped to a function.")
                            else:
                                logging.info(f"_gamepad_events {device_num}: {key_event.keycode} not recognized.")

    # asyncio loop_thread function -- internal use only
    def _loop_thread(self,loop):
        try:
            asyncio.set_event_loop(loop)
            loop.run_forever()
        except:
            logging.info(f"System exit caught - exiting")
            loop.stop()

    def add_function(self, button, function):
        if mode == "board":
            self.function_map[button] = {
                "function": function,
                "button": button,
            }
            logging.debug(f"add_function: Key: {button}, {self.function_map[button]['function']}")

        elif mode == "workstation":
            logging.debug(f"add_function: Key: {self.button_map[button]}") 
            keyboard.add_hotkey(self.button_map[button], function)

        else:
            logging.warning(f"Unhandled mode: {mode}, button: {button}, function: {function}")
