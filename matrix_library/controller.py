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
    def __init__(self):

        # debug state
        self.debug = True
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
                    logging.debug("No gamepad found") 
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

            # # setup evdev async/await functions for gamepad2
            # if self.gamepad2 is not None:
            #     asyncio.ensure_future(self._gamepad_events(self.gamepad2))
            #     self.loop2 = asyncio.get_event_loop()
            #     self.t2 = threading.Thread(target=self._loop_thread, args=(self.loop2,), daemon=True).start()

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

        # debug output
        logging.debug(self.button_map)


    # destructor - need this to stop any threads
    # def __del__(self):
    #     logging.info("Stopping controller")
    #     if self.t is not None:
    #         del self.t

    # asyncio gamepad_event function -- internal use only
    async def _gamepad_events(self,device):
        async for event in device.async_read_loop():
            logging.debug(f"_gamepad_events: {device.path} {evdev.categorize(event)}") 

            if event.type == evdev.ecodes.EV_KEY:
                    key_event = evdev.categorize(event)
                    if (key_event.keystate == key_event.key_down or 
                        key_event.keystate == key_event.key_hold):
                            if key_event.keycode in evdev.ecodes.ecodes:
                                # map key_event.keycode to integer number
                                logging.debug(f"_gamepad_events: Integer keycode value: {evdev.ecodes.ecodes[key_event.keycode]}")
                                button_code = evdev.ecodes.ecodes[key_event.keycode]
                                # map the button_code integer number to the internal UP/DOWN/LEFT/RIGHT/etc
                                button = list(self.button_map.keys())[list(self.button_map.values()).index(button_code)]
                                logging.debug(f"_gamepad_events: button {button}")

                                # check to see if a mapped function exists for that
                                if button in self.function_map:
                                    logging.debug(f"_gamepad_events: button {button} calls function {self.function_map[button]['function']}")
                                    self.function_map[button]["function"]()
                                else:
                                    logging.debug(f"_gamepad_events: button {button} is not mapped to a function.")
    
    # asyncio loop_thread function -- internal use only
    def _loop_thread(self,loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def add_function(self, button, function):
        if mode == "board":
            self.function_map[button] = {
                "function": function,
                "button": button,
            }
            logging.debug(self.function_map)

        elif mode == "workstation":
            logging.debug(f"Key: {self.button_map[button]}") 
            keyboard.add_hotkey(self.button_map[button], function)

        else:
            logging.warning(f"Unhandled mode: {mode}, button: {button}, function: {function}")
