import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings


class VectorStoreService:
    """Manages ChromaDB for storing and retrieving document embeddings."""

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )

    def _get_collection(self, project_id: str):
        return self.client.get_or_create_collection(
            name=f"project_{project_id}",
            metadata={"hnsw:space": "cosine"},
        )

    def store(self, project_id: str, chunks: list[str], file_id: str, filename: str = ""):
        collection = self._get_collection(project_id)
        ids = [f"{file_id}_{i}" for i in range(len(chunks))]
        metadatas = [{"file_id": file_id, "chunk_index": i, "filename": filename} for i in range(len(chunks))]
        # ChromaDB handles embedding via its default model
        collection.add(documents=chunks, ids=ids, metadatas=metadatas)

    def query(self, project_id: str, query_text: str = "", n_results: int = 20) -> list[str]:
        collection = self._get_collection(project_id)
        if collection.count() == 0:
            return []

        if query_text:
            results = collection.query(query_texts=[query_text], n_results=n_results)
        else:
            # Return all documents if no specific query
            results = collection.get(limit=n_results)
            return results.get("documents", []) or []

        return results.get("documents", [[]])[0]

    def clear(self, project_id: str):
        collection_name = f"project_{project_id}"
        try:
            self.client.delete_collection(collection_name)
        except ValueError:
            pass  # Collection doesn't exist

    def list_projects(self) -> list[str]:
        collections = self.client.list_collections()
        return [c.name.removeprefix("project_") for c in collections if c.name.startswith("project_")]

    def list_files(self, project_id: str) -> list[dict]:
        collection = self._get_collection(project_id)
        if collection.count() == 0:
            return []
        results = collection.get(include=["metadatas"])
        file_ids = set()
        files = []
        for meta in (results.get("metadatas") or []):
            fid = meta.get("file_id", "")
            fname = meta.get("filename", fid)
            if fid and fid not in file_ids:
                file_ids.add(fid)
                files.append({"file_id": fid, "filename": fname})
        return files

    def delete_file(self, project_id: str, file_id: str) -> int:
        collection = self._get_collection(project_id)
        results = collection.get(where={"file_id": file_id})
        ids_to_delete = results.get("ids", [])
        if ids_to_delete:
            collection.delete(ids=ids_to_delete)
        return len(ids_to_delete)
