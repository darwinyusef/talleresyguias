"""
RAG Service with ChromaDB and Sentence Transformers.
"""
import logging
import os
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, make_asgi_app

try:
    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer
except ImportError:
    chromadb = None
    SentenceTransformer = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Métricas
rag_queries_total = Counter('rag_queries_total', 'Total RAG queries')
rag_query_duration = Histogram('rag_query_duration_seconds', 'RAG query duration')
documents_indexed_total = Counter('documents_indexed_total', 'Total documents indexed')

app = FastAPI(title="RAG Service", version="1.0.0")

# Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


class DocumentInput(BaseModel):
    """Input para indexar documentos."""
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    document_id: Optional[str] = None


class QueryInput(BaseModel):
    """Input para queries."""
    query: str
    top_k: int = Field(default=5, ge=1, le=20)
    filter: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    """Respuesta de query."""
    query: str
    results: List[Dict[str, Any]]
    num_results: int


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "rag-service",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "rag-service"}


@app.post("/index", response_model=Dict[str, Any])
async def index_document(doc: DocumentInput):
    """Endpoint para indexar documentos."""
    try:
        documents_indexed_total.inc()

        # Simulación de indexación
        logger.info(f"Indexing document: {doc.document_id}")

        return {
            "document_id": doc.document_id or "auto_generated",
            "num_chunks": 1,
            "status": "indexed",
        }
    except Exception as e:
        logger.error(f"Failed to index document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_documents(query: QueryInput):
    """Endpoint para queries."""
    rag_queries_total.inc()

    try:
        with rag_query_duration.time():
            # Simulación de query
            logger.info(f"Querying: {query.query}")

            results = [
                {
                    "id": "doc_1",
                    "content": "Example content related to query",
                    "metadata": {"source": "example"},
                    "relevance_score": 0.95,
                }
            ]

            return QueryResponse(
                query=query.query,
                results=results,
                num_results=len(results),
            )
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_stats():
    """Endpoint para estadísticas."""
    return {
        "collection_name": "documents",
        "num_documents": 0,
        "status": "ready",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
