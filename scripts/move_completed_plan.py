import os
import shutil
from datetime import datetime

ACTIVE_DIR = 'docs/active_plans'
COMPLETED_DIR = 'docs/completed_plans'


def move_completed_plans():
    for filename in os.listdir(ACTIVE_DIR):
        if not filename.endswith('.md'):
            continue
        path = os.path.join(ACTIVE_DIR, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'status: closed' in content:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            new_filename = f"{filename.replace('.md', '')}_{timestamp}.md"
            new_path = os.path.join(COMPLETED_DIR, new_filename)
            shutil.move(path, new_path)
            meta_path = os.path.join(COMPLETED_DIR, f"{new_filename.replace('.md', '.meta.yaml')}")
            with open(meta_path, 'w', encoding='utf-8') as meta:
                meta.write(f"plan: {filename}\nstatus: closed\narchived_at: {timestamp}\n")
            print(f"Moved {filename} -> {new_filename}")


if __name__ == '__main__':
    move_completed_plans()