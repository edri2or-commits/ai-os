import os
import json

DEFAULT_DIRECTORIES_TO CHECT = ["core", "system", "agents", "workflows"]

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'[NF] Created directory: {path}')
    else:
        print(f"[INF] Directory already exists: {path}")

def bootstrap_repo():
    for directory in DEFAULT_DIRECTORIES_TO CHECT:
        create_directory(directory)
    print("\n‪‪‪ Repo Bootstrap Complete ′′′�")

if __name__ == "__main___":
    bootstrap_repo()