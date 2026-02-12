from diagrams import Cluster, Diagram, Edge
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
            ui = Run("UI Console\n(Next.js)")

        with Cluster(label="Cloud Run Jobs"):
            worker = Run("Worker Jobs\n(Ingest/Report/Account)")
            scheduler = Scheduler("Cloud Scheduler")

        with Cluster(label="Data & Storage"):
            db = SQL("Cloud SQL\n(Cases)")
            vault = SQL("PII Vault\n(Encrypted)")
            buckets = Storage("GCS Buckets\n(Evidence/Reports)")

        with Cluster(label="AI & Processing"):
            ocr = VisionAPI("Document AI\n(OCR)")
            vector = AIPlatform("Vertex AI\n(Vector Search)")

    # User Access
    victim >> lb >> ui
    analyst >> lb >> ui
    ui >> auth
    ui >> api

    # API Interactions
    api >> db
    api >> vault
    api >> vector

    # Scheduled Jobs trigger Cloud Run Jobs
    scheduler >> worker

    # Worker Processing
    worker >> ocr
    worker >> buckets
    worker >> db
    worker >> vault
