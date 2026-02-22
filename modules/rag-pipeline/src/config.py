from pathlib import Path
import os

PRODUCTS_CSV = Path(__file__).resolve().parent.parent.parent.parent / "data" / "products.csv"

EMBEDDER_URL = os.environ.get("EMBEDDER_URL")

WEAVIATE_HOST = os.environ.get("WEAVIATE_HOST")
WEAVIATE_PORT = os.environ.get("WEAVIATE_PORT")
WEAVIATE_SECURE = os.environ.get("WEAVIATE_SECURE")
WEAVIATE_GRPC_HOST = os.environ.get("WEAVIATE_GRPC_HOST")
WEAVIATE_GRPC_PORT = os.environ.get("WEAVIATE_GRPC_PORT")
WEAVIATE_GRPC_SECURE = os.environ.get("WEAVIATE_GRPC_SECURE")