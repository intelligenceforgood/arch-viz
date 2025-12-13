from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.compute import Run
from diagrams.gcp.database import Firestore
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

    with Cluster(label="Identity Provider"):
        idp = Iam("Identity Platform\n(Firebase Auth)")

    with Cluster(label="Access Control"):
        lb = LoadBalancing("Global LB\n(IAP / Armor)")

    with Cluster(label="Service Layer"):
        api = Run("Core API")

    with Cluster(label="Data Protection"):
        kms = KeyManagementService("Cloud KMS")
        vault = Firestore("PII Vault")

    # Authentication Flow
    victim >> Edge(label="1. Sign In") >> idp
    analyst >> Edge(label="1. Sign In") >> idp

    # Token Exchange
    idp >> Edge(label="2. JWT Token", style="dashed") >> victim
    idp >> Edge(label="2. JWT Token", style="dashed") >> analyst

    # Authorized Request
    victim >> Edge(label="3. Request + Bearer Token") >> lb
    analyst >> Edge(label="3. Request + Bearer Token") >> lb

    lb >> Edge(label="4. Verify Token") >> api

    # Data Access
    api >> Edge(label="5. Decrypt PII") >> kms
    kms >> Edge(label="6. Read/Write") >> vault
