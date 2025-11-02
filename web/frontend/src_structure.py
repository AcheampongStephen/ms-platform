import os

folders = [
    "src/api",
    "src/components/common",
    "src/components/layout",
    "src/components/features",
    "src/pages/Home",
    "src/pages/Products",
    "src/pages/ProductDetail",
    "src/pages/Cart",
    "src/pages/Auth",
    "src/hooks",
    "src/store",
    "src/utils",
    "src/styles",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("Frontend folder structure created")
