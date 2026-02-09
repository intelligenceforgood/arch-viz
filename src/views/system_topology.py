from diagrams import Cluster, Diagram, Edge
from diagrams.azure.database import SQLDatabases
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import Run
from diagrams.gcp.database import SQL
from diagrams.gcp.devtools import Scheduler
from diagrams.gcp.ml import AIPlatform, VisionAPI
from diagrams.gcp.network import LoadBalancing
from diagrams.gcp.security import Iam
from diagrams.gcp.storage import Storage
from diagrams.onprem.client import User, Users

with Diagram(
    "System Topology",
    show=False,
    filename="output/system_topology",
    outformat="svg",
    direction="LR",
):

    with Cluster(label="External Users"):
        victim = User("Victim\n(Intake Form)")
        analyst = Users("Analysts\n(Console)")

    with Cluster(label="GCP Project (i4g-prod)"):

        with Cluster(label="Ingress & Auth"):
            lb = LoadBalancing("Global LB")
            auth = Iam("IAP\n(Google Sign-In)")

        with Cluster(label="Compute (Cloud Run)"):
            api = Run("Core API\n(FastAPI)")
            worker = Run("Worker\n(Jobs)")
            ui = Run("UI Console\n(Next.js)")

        with Cluster(label="Data & Storage"):
            db = SQL("Cloud SQL\n(Cases)")
            vault = SQL("PII Vault\n(Encrypted)")
            buckets = Storage("GCS Buckets\n(Evidence/Reports)")

        with Cluster(label="AI & Processing"):
            ocr = VisionAPI("Document AI\n(OCR)")
            vector = AIPlatform("Vertex AI\n(Vector Search)")

        with Cluster(label="Async / Event Bus"):
            pubsub = PubSub("Task Queue")
            scheduler = Scheduler("Weekly Refresh")

    with Cluster(label="Legacy / External"):
        azure_db = SQLDatabases("Azure SQL\n(Historical)")

    # User Access
    victim >> lb >> ui
    analyst >> lb >> ui
    ui >> auth
    ui >> api

    # API Interactions
    api >> db
    api >> vault
    api >> pubsub
    api >> vector

    # Worker Processing
    pubsub >> worker
    worker >> ocr
    worker >> buckets
    worker >> db
    worker >> vault

    # Scheduled Jobs
    scheduler >> worker
    worker >> Edge(label="Sync") >> azure_db
