import os

folders = ["app", "tests"]

for folder in folders:
    # Create folder
    os.makedirs(folder, exist_ok=True)

    # Create __init__.py inside it
    init_file = os.path.join(folder, "__init__.py")
    with open(init_file, "w") as f:
        pass  # creates an empty file

print("Folders and __init__.py files created successfully")
