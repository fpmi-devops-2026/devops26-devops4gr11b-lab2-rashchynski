import os
import re

DATA_FILE = "/var/data/data.txt"
RESULT_FILE = "/var/result/result.txt"

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: File {DATA_FILE} does not exist.")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    numbers = [int(num) for num in re.findall(r'-?\d+', content)]

    if not numbers:
        print(f"No numbers found in {DATA_FILE}")
        return

    max_num = max(numbers)
    count_max = numbers.count(max_num)

    os.makedirs(os.path.dirname(RESULT_FILE), exist_ok=True)

    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        f.write(str(count_max))

    print(f"[Worker 2] Max number: {max_num}, Count: {count_max}")
    print(f"[Worker 2] Result successfully saved to {RESULT_FILE}")

if __name__ == "__main__":
    main()