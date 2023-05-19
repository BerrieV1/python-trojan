import os
import subprocess
from basemodule import BaseModule
from playsound import playsound
from datetime import datetime


class Play_sound(BaseModule):
    def run(self):
        audio_file = os.path.dirname(__file__) + 'suprise.mp3'
        playsound(audio_file)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("../sounds/logs.txt", "a") as sounds_file:
            sounds_file.write(f"Sound played at {current_time}\n")

    def install_requirements(self):
        libraries = ["playsound"]
        for library in libraries:
            subprocess.check_call(["pip", "install", library])
