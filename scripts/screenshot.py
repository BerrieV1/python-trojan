import subprocess
from basemodule import BaseModule
import pyautogui
import datetime
import time


class Screenshot(BaseModule):
    def run(self):
        while time.time() < (time.time() + 120):
            now = datetime.datetime.now()
            screenshot = pyautogui.screenshot()
            screenshot.save(fr'../screenshots/{now.strftime("%Y-%m-%d_%H-%M-%S")}.jpg')
            time.sleep(10)

    def install_requirements(self):
        libraries = ["pyautogui"]
        for library in libraries:
            subprocess.check_call(["pip", "install", library])
