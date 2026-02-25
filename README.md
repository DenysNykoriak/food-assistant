# Food Assistant

A RAG (Retrieval Augmented Generation) app that answers questions about food products. It retrieves relevant products from a vector store and uses an LLM to generate answers.

## Architecture

- **core-api** – Hono API with assistant endpoints that query Weaviate and call an LLM
- **rag-pipeline** – Python pipeline that loads product data into Weaviate
- **embedder** – FastAPI service that embeds text using SentenceTransformers (all-MiniLM-L6-v2)
- **weaviate** – Vector database for product embeddings
- **LLM** – Docker-based model (e.g. Qwen) for generating answers

## Motivation

This is not a production setup. In production, the embedder would likely use APIs from AI companies (OpenAI, etc.) instead of a self-hosted model. The same applies to the main LLM that answers questions. This project is intended to explore RAG and run everything locally without external services.

## Quick Start

1. Start infrastructure: `docker compose -f iac/docker-compose.yaml up`
2. Download products data csv file and place it in the `data` directory with the name `products.csv`
3. Run RAG pipeline to index products: `python modules/rag-pipeline/src/main.py`
4. Start API: `cd modules/core-api && bun run dev`

## Technologies

| Layer          | Stack                                                                 |
| -------------- | --------------------------------------------------------------------- |
| core-api       | TypeScript, Bun, Hono, AI SDK (OpenAI-compatible), Weaviate client, Zod |
| rag-pipeline   | Python, pandas, weaviate-client                                       |
| embedder       | FastAPI, SentenceTransformers (all-MiniLM-L6-v2)                      |
| Infrastructure | Docker, Weaviate, LLM (Docker/API)                                    |

## License

See [LICENSE](LICENSE).
