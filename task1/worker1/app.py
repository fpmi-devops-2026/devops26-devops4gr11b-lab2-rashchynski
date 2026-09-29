import os
import random
import shutil

DATA_DIR = "/var/data"
RESULT_FILE = "/var/result/data.txt"

def main():
    if not os.path.exists(DATA_DIR):
        print(f"Error: Directory {DATA_DIR} does not exist.")
        return

    files = [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
    
    if not files:
        print(f"No files found in {DATA_DIR}")
        return

    selected_file = random.choice(files)
    source_path = os.path.join(DATA_DIR, selected_file)
    
    os.makedirs(os.path.dirname(RESULT_FILE), exist_ok=True)
    
    shutil.copyfile(source_path, RESULT_FILE)
    print(f"[Worker 1] Selected file '{selected_file}' and copied to '{RESULT_FILE}'")

if __name__ == "__main__":
    main()