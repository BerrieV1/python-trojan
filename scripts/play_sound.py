import subprocess
from basemodule import BaseModule
from playsound import playsound
from datetime import datetime


class Play_sound(BaseModule):
    def run(self):
        playsound("../sounds/suprise.mp3")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("../sounds/logs.txt", "a") as sounds_file:
            sounds_file.write(f"Sound played at {current_time}\n")

    def install_requirements(self):
        libraries = ["playsound==1.2.2"]
        for library in libraries:
            subprocess.check_call(["pip", "install", library])
