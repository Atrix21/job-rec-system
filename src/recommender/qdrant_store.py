import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import numpy as np

class QdrantVectorStore:
    def __init__(self, collection_name="jobs_hybrid", resume_collection_name="resumes_hybrid", vector_size=384):
        load_dotenv()
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.client = QdrantClient(url=qdrant_url)
        self.collection_name = collection_name
        self.resume_collection_name = resume_collection_name
        self.vector_size = vector_size
        self._ensure_collection(self.collection_name)
        self._ensure_collection(self.resume_collection_name)

    def _ensure_collection(self, collection_name):
        try:
            self.client.get_collection(collection_name)
        except Exception:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                )
            )

    def upsert_job(self, job_id: int, embedding: np.ndarray, metadata: dict):
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=job_id,
                    vector=embedding.tolist(),
                    payload=metadata
                )
            ]
        )

    def search(self, embedding: np.ndarray, top_k: int = 5):
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding.tolist(),
            limit=top_k
        )
        return [
            {
                "job_id": r.id,
                "score": r.score,
                "payload": r.payload
            }
            for r in results
        ]

    def upsert_resume(self, resume_id: int, embedding: np.ndarray, metadata: dict):
        self.client.upsert(
            collection_name=self.resume_collection_name,
            points=[
                models.PointStruct(
                    id=resume_id,
                    vector=embedding.tolist(),
                    payload=metadata
                )
            ]
        )

    def search_resume(self, embedding: np.ndarray, top_k: int = 5):
        results = self.client.search(
            collection_name=self.resume_collection_name,
            query_vector=embedding.tolist(),
            limit=top_k
        )
        return [
            {
                "resume_id": r.id,
                "score": r.score,
                "payload": r.payload
            }
            for r in results
        ] 