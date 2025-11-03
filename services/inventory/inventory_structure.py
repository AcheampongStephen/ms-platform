import os

# Folders you want to create
folders = ["app", "tests"]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    init_path = os.path.join(folder, "__init__.py")
    with open(init_path, "w") as f:
        pass

print("Folders created and __init__.py files added")
