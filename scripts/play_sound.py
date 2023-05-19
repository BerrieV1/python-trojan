import subprocess
from basemodule import BaseModule
from playsound import playsound


class Play_sound(BaseModule):
    def run(self):
        playsound("../sounds/suprise.mp3")

    def install_requirements(self):
        libraries = ["playsound"]
        for library in libraries:
            subprocess.check_call(["pip", "install", library])