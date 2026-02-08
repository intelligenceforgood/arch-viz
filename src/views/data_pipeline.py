from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import Run
from diagrams.gcp.database import SQL
from diagrams.gcp.ml import AIPlatform, VisionAPI
from diagrams.gcp.storage import Storage

with Diagram(
    "Data Pipeline",
    show=False,
    filename="output/data_pipeline",
    outformat="svg",
    direction="LR",
):

    with Cluster(label="Ingestion"):
        upload = Run("API Upload")
        queue = PubSub("Processing Queue")

    with Cluster(label="Worker Processing"):
        worker = Run("Worker Service")

        with Cluster(label="Extraction"):
            ocr = VisionAPI("Document AI")

        with Cluster(label="Security"):
            pii_vault = SQL("PII Vault")

        with Cluster(label="Storage"):
            raw_bucket = Storage("Raw Evidence")
            clean_bucket = Storage("Redacted Evidence")
            case_db = SQL("Case\nMetadata")

    with Cluster(label="Indexing"):
        vector_db = AIPlatform("Vertex AI\nVector Search")

    # Flow
    upload >> Edge(label="1. Enqueue") >> queue
    queue >> Edge(label="2. Pull") >> worker

    worker >> Edge(label="3. Store Raw") >> raw_bucket
    worker >> Edge(label="4. Extract Text") >> ocr
    worker >> Edge(label="5. Tokenize PII") >> pii_vault
    worker >> Edge(label="6. Store Clean") >> clean_bucket
    worker >> Edge(label="7. Update Case") >> case_db

    # Indexing flow
    case_db >> Edge(style="dashed", label="8. Sync") >> vector_db
