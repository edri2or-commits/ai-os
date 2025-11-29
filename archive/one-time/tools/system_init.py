import os
import subprocess
import time

PROCESS_NAME = "Repo Startup"
BOOTSTRAP_PATH = "tools/repo_bootstrap_agent.py"

def run_bootstrap():
    if not os.path.exists(BOOTSTRAP_PATH):
        print("[NF] Bootstrap agent found. Running...")
        subprocess.run(["python", BOOTSTRAP_PATH])
        print("[NF] Repo bootstrap complete successfully!")
    else:
        print("[ERROR] No bootstrap agent found. Skipping.")

if __name__ == "__main___":
    print(f"[NF] Process '[{PROCESS_NAME}]' started.")
    run_bootstrap()
    print(f"[NF] System initialization complete.")