import os

folders = [
    ".github/workflows/reusable",
    "services/users/app/tests",
    "services/orders/app/tests",
    "services/payments/app/tests",
    "services/inventory/app/tests",
    "web/frontend/src",
    "web/bff/src",
    "packages/contracts",
    "infra/terraform/global",
    "infra/terraform/nonprod",
    "infra/terraform/prod",
    "infra/terraform/modules",
    "infra/helm/charts/users",
    "infra/helm/charts/orders",
    "infra/helm/charts/payments",
    "infra/helm/charts/inventory",
    "infra/helm/charts/web-frontend",
    "infra/helm/charts/web-bff",
    "infra/helm/platform",
    "ansible",
    "docs/runbooks",
    "scripts",
    "tests/integration",
    "tests/e2e",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("Folder structure created successfully")
