from fastapi import FastAPI
from fastapi.responses import Response
from sentence_transformers import SentenceTransformer

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")
VECTOR_DIM = 384

@app.post("/embed")
def embed(body: dict):
    inputs = body.get("inputs")
    if isinstance(inputs, str):
        inputs = [inputs]
    vectors = model.encode(inputs).tolist()
    if len(vectors) == 1:
        return {"embeddings": vectors[0]}
    return {"embeddings": vectors}


@app.post("/vectors")
def vectors(body: dict):
    text = body.get("text", "")
    vector = model.encode([text]).tolist()[0]
    return {"text": text, "vector": vector, "dim": VECTOR_DIM}


@app.get("/meta")
def meta():
    return {"name": "embedder", "version": "1.0.0"}


@app.get("/.well-known/ready")
@app.get("/.well-known/live")
def readiness():
    return Response(status_code=204)
