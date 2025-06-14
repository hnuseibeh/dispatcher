# core/rag/vector_store.py
import chromadb
from chromadb.utils import embedding_functions
import os
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, path="./vector_store_data/", collection_name="zaki_os_lessons", embedding_model_name="all-MiniLM-L6-v2"):
        os.makedirs(path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=path)

        self.sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model_name)

        try:
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                embedding_function=self.sentence_transformer_ef
            )
            logger.info(f"ChromaDB collection '{collection_name}' loaded/created successfully at path '{path}'.")
        except Exception as e:
            logger.error(f"Failed to get or create ChromaDB collection: {e}", exc_info=True)
            raise

    def add_documents(self, documents: list[str], metadatas: list[dict], ids: list[str]):
        if not (len(documents) == len(metadatas) == len(ids)):
            logger.error("Number of documents, metadatas, and ids must be the same.")
            raise ValueError("Number of documents, metadatas, and ids must be the same.")
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(documents)} documents to collection '{self.collection.name}'.")
        except Exception as e:
            logger.error(f"Failed to add documents to ChromaDB: {e}", exc_info=True)
            raise

    def query(self, query_texts: list[str], n_results: int = 3) -> dict:
        try:
            results = self.collection.query(
                query_texts=query_texts,
                n_results=n_results,
                include=['metadatas', 'documents', 'distances']
            )
            num_results_found = 0
            if results and results.get('ids') and results['ids'][0]: # Check if results and first query's ids are not empty
                num_results_found = len(results['ids'][0])
            logger.info(f"Query returned {num_results_found} results for '{query_texts[0] if query_texts else ''}'.")
            return results if results else {}
        except Exception as e:
            logger.error(f"Failed to query ChromaDB: {e}", exc_info=True)
            return {}

    def get_collection_count(self) -> int:
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Failed to get collection count: {e}", exc_info=True)
            return 0