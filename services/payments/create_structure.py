import os

folders = ["app", "tests"]

for f in folders:
    os.makedirs(f, exist_ok=True)
    init_file = os.path.join(f, "__init__.py")
    with open(init_file, "w") as file:
        file.write("")  # creates an empty __init__.py

print("Folders created and __init__.py files added")
