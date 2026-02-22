import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import requests
import weaviate

import config
import weaviate.classes as wvc

weaviate_client = weaviate.connect_to_custom(
    http_host=config.WEAVIATE_HOST,
    http_port=config.WEAVIATE_PORT,
    http_secure=config.WEAVIATE_SECURE,
    grpc_host=config.WEAVIATE_GRPC_HOST,
    grpc_port=config.WEAVIATE_GRPC_PORT,
    grpc_secure=config.WEAVIATE_GRPC_SECURE,
)

def row_to_content(row: pd.Series) -> str:
    return " ".join(str(v) for v in row.values if pd.notna(v) and str(v).strip())


def embed_one(content: str) -> wvc.data.DataObject | None:
    try:
        res = requests.post(
            f"{config.EMBEDDER_URL}/embed",
            json={"inputs": content},
            timeout=60,
        )
        res.raise_for_status()
        emb = res.json()["embeddings"]
        vector = emb[0] if isinstance(emb[0], list) else emb
        return wvc.data.DataObject(
            properties={"content": content},
            vector=vector,
        )
    except Exception:
        print(f"Error embedding: {content[:80]}...")
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip", type=int, default=0, help="Skip rows")
    parser.add_argument("--limit", type=int, default=100, help="Limit rows")
    parser.add_argument("--chunk-size", type=int, default=1000, help="Max chars per chunk")
    parser.add_argument("--chunk-overlap", type=int, default=100, help="Overlap between chunks")
    args = parser.parse_args()

    df = pd.read_csv(
        config.PRODUCTS_CSV,
        sep="\t",
        on_bad_lines="skip",
        skiprows=args.skip,
        nrows=args.limit,
    )
    df.reset_index(drop=True, inplace=True)

    contents = [row_to_content(row) for _, row in df.iterrows()]
    contents = [c for c in contents if c.strip()]

    data_to_embed: list[wvc.data.DataObject] = []
    max_workers = 8
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(embed_one, contents))
    data_to_embed = [r for r in results if r is not None]

    # Insert data into Weaviate
    ## Check if collection exists
    if not weaviate_client.collections.exists("Product"):
        weaviate_client.collections.create(
            "Product",
            vector_config=wvc.config.Configure.Vectors.self_provided()
        )

    ## Insert data
    products = weaviate_client.collections.use("Product")
    products.data.insert_many(data_to_embed)


main()

weaviate_client.close()