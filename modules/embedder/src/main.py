from fastapi import FastAPI
from sentence_transformers import SentenceTransformer

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")


@app.post("/embed")
def embed(body: dict):
    inputs = body.get("inputs")
    if isinstance(inputs, str):
        inputs = [inputs]
    vectors = model.encode(inputs).tolist()
    if len(vectors) == 1:
        return {"embeddings": vectors[0]}
    return {"embeddings": vectors}
