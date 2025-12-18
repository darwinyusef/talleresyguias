#!/usr/bin/env python3
"""
Script para probar el sistema RAG.
"""
import argparse
import logging
import sys
from pathlib import Path

import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

console = Console()


def index_sample_documents(base_url: str):
    """Indexa documentos de ejemplo."""
    console.print("[bold blue]Indexing sample documents...[/bold blue]")

    documents = [
        {
            "content": """
            PyTorch is an open-source machine learning framework developed by Meta AI.
            It provides a flexible and efficient platform for deep learning research and production.
            PyTorch uses dynamic computational graphs, making it intuitive and easy to debug.
            Key features include automatic differentiation, GPU acceleration, and extensive library support.
            """,
            "metadata": {
                "category": "technical",
                "topic": "pytorch",
                "author": "Meta AI",
            },
            "document_id": "pytorch_intro",
        },
        {
            "content": """
            TensorFlow is an end-to-end open-source platform for machine learning developed by Google.
            It offers a comprehensive ecosystem of tools, libraries, and community resources.
            TensorFlow uses static computational graphs by default, optimized for production deployment.
            Features include distributed training, model serving with TensorFlow Serving, and TensorBoard for visualization.
            """,
            "metadata": {
                "category": "technical",
                "topic": "tensorflow",
                "author": "Google",
            },
            "document_id": "tensorflow_intro",
        },
        {
            "content": """
            MLOps is a set of practices that combines Machine Learning, DevOps, and Data Engineering.
            The goal is to deploy and maintain ML systems in production reliably and efficiently.
            Key components include continuous integration/deployment, model versioning, monitoring, and automated retraining.
            MLOps ensures reproducibility, scalability, and governance of ML workflows.
            """,
            "metadata": {
                "category": "technical",
                "topic": "mlops",
                "author": "MLOps Community",
            },
            "document_id": "mlops_intro",
        },
        {
            "content": """
            Retrieval Augmented Generation (RAG) combines information retrieval with text generation.
            It enhances language models by providing relevant context from a knowledge base.
            The RAG process: 1) Embed the query, 2) Retrieve similar documents, 3) Augment prompt with context, 4) Generate response.
            Benefits include up-to-date information, reduced hallucinations, and domain-specific knowledge integration.
            """,
            "metadata": {
                "category": "technical",
                "topic": "rag",
                "author": "LangChain Team",
            },
            "document_id": "rag_intro",
        },
        {
            "content": """
            Docker is a platform for developing, shipping, and running applications in containers.
            Containers package software with all dependencies, ensuring consistency across environments.
            For ML/DL, Docker provides isolated environments with specific CUDA versions and frameworks.
            Benefits include reproducibility, portability, and simplified deployment of ML models.
            """,
            "metadata": {
                "category": "technical",
                "topic": "docker",
                "author": "Docker Inc",
            },
            "document_id": "docker_intro",
        },
    ]

    for doc in documents:
        try:
            response = requests.post(
                f"{base_url}/index",
                json=doc,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()
            console.print(
                f"✓ Indexed: {doc['document_id']} "
                f"({result['num_chunks']} chunks)",
                style="green",
            )
        except Exception as e:
            console.print(f"✗ Failed to index {doc['document_id']}: {e}", style="red")


def query_rag(base_url: str, query: str, top_k: int = 3):
    """Realiza query al sistema RAG."""
    console.print(f"\n[bold blue]Query:[/bold blue] {query}\n")

    try:
        response = requests.post(
            f"{base_url}/query",
            json={"query": query, "top_k": top_k},
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()

        # Crear tabla de resultados
        table = Table(title="RAG Results", show_header=True, header_style="bold magenta")
        table.add_column("Rank", style="cyan", width=6)
        table.add_column("Score", style="green", width=10)
        table.add_column("Topic", style="yellow", width=15)
        table.add_column("Content", style="white", width=60)

        for i, res in enumerate(result["results"], 1):
            score = res.get("relevance_score", 0)
            topic = res.get("metadata", {}).get("topic", "unknown")
            content = res.get("content", "")[:200] + "..."

            table.add_row(
                str(i),
                f"{score:.4f}",
                topic,
                content,
            )

        console.print(table)

        return result

    except Exception as e:
        console.print(f"✗ Query failed: {e}", style="red")
        return None


def main():
    parser = argparse.ArgumentParser(description="Test RAG system")
    parser.add_argument(
        "--base-url",
        type=str,
        default="http://localhost:8002",
        help="RAG service base URL",
    )
    parser.add_argument(
        "--index",
        action="store_true",
        help="Index sample documents",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Query to search",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of results to return",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode",
    )

    args = parser.parse_args()

    # Header
    console.print(
        Panel.fit(
            "[bold cyan]RAG System Testing Tool[/bold cyan]\n"
            f"Service: {args.base_url}",
            border_style="cyan",
        )
    )

    # Index documents if requested
    if args.index:
        index_sample_documents(args.base_url)

    # Single query mode
    if args.query:
        query_rag(args.base_url, args.query, args.top_k)

    # Interactive mode
    if args.interactive:
        console.print("\n[bold green]Interactive mode - Enter queries (Ctrl+C to exit)[/bold green]\n")

        sample_queries = [
            "What is PyTorch?",
            "How does RAG work?",
            "Differences between PyTorch and TensorFlow",
            "What are the benefits of Docker for ML?",
            "Explain MLOps practices",
        ]

        console.print("[dim]Sample queries:[/dim]")
        for i, q in enumerate(sample_queries, 1):
            console.print(f"  {i}. {q}", style="dim")
        console.print()

        try:
            while True:
                query = console.input("[bold yellow]Query:[/bold yellow] ")
                if query.strip():
                    query_rag(args.base_url, query.strip(), args.top_k)
                    console.print()
        except KeyboardInterrupt:
            console.print("\n\n[bold red]Exiting...[/bold red]")


if __name__ == "__main__":
    main()
