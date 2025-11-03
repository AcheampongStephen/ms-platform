import os

folders = [
    "app",
    "tests",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    init_file = os.path.join(folder, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            pass  # creates an empty __init__.py

print("Base structure created with __init__.py files")
