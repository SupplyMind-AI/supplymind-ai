"""Create the SupplyMind dense Pinecone index when it does not exist."""

from __future__ import annotations

from pinecone import Pinecone, ServerlessSpec

from supplymind.shared.config.settings import get_settings


def main() -> None:
    settings = get_settings()
    if not settings.pinecone_api_key:
        raise RuntimeError("PINECONE_API_KEY is required.")

    client = Pinecone(api_key=settings.pinecone_api_key)
    existing = {item.name for item in client.list_indexes()}

    if settings.pinecone_index_name not in existing:
        client.create_index(
            name=settings.pinecone_index_name,
            dimension=settings.embedding_dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=settings.pinecone_cloud,
                region=settings.pinecone_region,
            ),
        )
        print(f"Created Pinecone index: {settings.pinecone_index_name}")
    else:
        print(f"Pinecone index already exists: {settings.pinecone_index_name}")

    description = client.describe_index(settings.pinecone_index_name)
    print(f"Index host: {description.host}")
    print("Copy this value into PINECONE_INDEX_HOST in .env")


if __name__ == "__main__":
    main()
