import argparse
from pathlib import Path

import pandas as pd
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

    if not weaviate_client.collections.exists("Product"):
        weaviate_client.collections.create(
            "Product",
            properties=[
                wvc.config.Property(name="content", data_type=wvc.config.DataType.TEXT),
            ],
            vector_config=[
                wvc.config.Configure.Vectors.text2vec_transformers(
                    name="content_vector",
                    source_properties=["content"],
                )
            ],
        )

    products = weaviate_client.collections.use("Product")
    with products.batch.fixed_size(batch_size=200) as batch:
        for content in contents:
            batch.add_object(properties={"content": content})


main()

weaviate_client.close()