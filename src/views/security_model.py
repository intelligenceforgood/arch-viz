from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.compute import Run
from diagrams.gcp.database import SQL
from diagrams.gcp.network import LoadBalancing
from diagrams.gcp.security import Iam, KeyManagementService
from diagrams.onprem.client import User, Users

with Diagram(
    "Security Model",
    show=False,
    filename="output/security_model",
    outformat="svg",
    direction="TB",
):

    with Cluster(label="Principals"):
        victim = User("Victim")
        analyst = Users("Analyst")
        admin = Users("Admin")

    with Cluster(label="Identity & Access"):
        lb = LoadBalancing("Global LB")
        iap = Iam("Identity-Aware Proxy\n(IAP)")

    with Cluster(label="Service Layer"):
        ui = Run("UI Console\n(Next.js)")
        api = Run("Core API\n(FastAPI)")

    with Cluster(label="Data Protection"):
        kms = KeyManagementService("Cloud KMS")
        vault = SQL("PII Vault\n(Isolated Project)")

    # Authentication Flow — IAP handles Google Sign-In
    victim >> Edge(label="1. HTTPS Request") >> lb
    analyst >> Edge(label="1. HTTPS Request") >> lb

    # IAP enforces authentication before traffic reaches Cloud Run
    lb >> Edge(label="2. Google Sign-In") >> iap
    iap >> Edge(label="3. X-Goog-Authenticated-User-Email") >> ui

    # Authorized Request
    ui >> Edge(label="4. API Call + X-API-KEY") >> api

    # Data Access
    api >> Edge(label="5. Decrypt PII") >> kms
    kms >> Edge(label="6. Read/Write") >> vault
