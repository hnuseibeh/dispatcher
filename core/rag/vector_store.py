# vector_store.py
# Handles storage/retrieval of embedded lessons using ChromaDB or fallback

class VectorStore:
    def __init__(self, path="./vector_store/"):
        self.path = path
        # TODO: initialize ChromaDB or SQLite + FAISS fallback

    def add_embedding(self, doc_id, embedding, metadata):
        # TODO: store embedding with associated metadata
        pass

    def query(self, embedding, top_k=3):
        # TODO: return top_k most similar embeddings
        return []

    def load_all_embeddings(self):
        # TODO: load all embeddings from lesson and report dirs
        pass