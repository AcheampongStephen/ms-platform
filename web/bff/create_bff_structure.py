import os

folders = [
    "src/config",
    "src/middleware",
    "src/routes",
    "src/services",
    "src/utils",
    "tests/integration",
    "tests/unit",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("BFF folder structure created successfully")
