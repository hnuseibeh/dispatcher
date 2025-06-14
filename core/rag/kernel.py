# core/rag/kernel.py
import os
import pathlib
import logging
from typing import List, Dict # Corrected import for Dict
from core.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS_PATH = PROJECT_ROOT / "docs"
VECTOR_STORE_PATH = str(PROJECT_ROOT / "core" / "rag" / "vector_store_data_prod")
DEFAULT_RAG_COLLECTION_NAME = "zaki_os_lessons_prod"

class RAGKernel:
    def __init__(self, vector_store_path: str = VECTOR_STORE_PATH, collection_name: str = DEFAULT_RAG_COLLECTION_NAME, embedding_model_name: str = "all-MiniLM-L6-v2"):
        logger.info(f"Initializing RAGKernel with vector store path: {vector_store_path}, collection: {collection_name}")
        try:
            self.vector_store = VectorStore(path=vector_store_path, collection_name=collection_name, embedding_model_name=embedding_model_name)
            # Check if collection is not None before calling count, and handle potential errors from VectorStore init
            if self.vector_store and self.vector_store.collection:
                 self.documents_loaded = self.vector_store.get_collection_count() > 0
            else:
                 self.documents_loaded = False
                 logger.warning("VectorStore or its collection might not have been initialized properly.")
        except Exception as e:
            logger.error(f"RAGKernel initialization failed: {e}", exc_info=True)
            self.vector_store = None
            self.documents_loaded = False

    def _load_markdown_documents(self, doc_paths: List[pathlib.Path]) -> List[Dict[str, str]]:
        loaded_docs = []
        for doc_path in doc_paths:
            try:
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                loaded_docs.append({"source": doc_path.name, "content": content, "path": str(doc_path)})
                logger.info(f"Successfully loaded document: {doc_path.name}")
            except Exception as e:
                logger.error(f"Failed to load document {doc_path}: {e}", exc_info=True)
        return loaded_docs

    def initialize_and_embed_lessons(self, force_reindex: bool = False):
        if self.vector_store is None:
            logger.error("Vector store not initialized. Cannot embed lessons.")
            return

        if not force_reindex and self.documents_loaded:
            logger.info("Documents already exist in the vector store and seem loaded. Skipping re-indexing. Use force_reindex=True to override.")
            return

        doc_files_to_load = [
            DOCS_PATH / "memory_kernel" / "index.md",
            DOCS_PATH / "onboarding" / "AGENT_ONBOARDING.md",
            DOCS_PATH / "status" / "AGENT_WORKFLOW_RULES_v1.3.2.md"
        ]

        existing_doc_paths = [p for p in doc_files_to_load if p.exists()]
        missing_docs = set(doc_files_to_load) - set(existing_doc_paths)
        if missing_docs:
            for p_miss in missing_docs: logger.warning(f"Document not found: {p_miss}")

        if not existing_doc_paths:
            logger.warning("No documents found to load for RAG system.")
            return

        raw_documents = self._load_markdown_documents(existing_doc_paths)

        if not raw_documents:
            logger.warning("No documents were successfully loaded. RAG system will be empty.")
            return

        docs_to_add = [doc['content'] for doc in raw_documents]
        metadatas_to_add = [{'source': doc['source'], 'path': doc['path']} for doc in raw_documents]
        ids_to_add = [doc['path'] for doc in raw_documents] # Using path as unique ID

        try:
            self.vector_store.add_documents(docs_to_add, metadatas_to_add, ids_to_add)
            self.documents_loaded = True
            logger.info(f"Successfully embedded and stored {len(docs_to_add)} documents.")
        except Exception as e:
            logger.error(f"Failed during embedding and storing documents: {e}", exc_info=True)
            self.documents_loaded = False

    def get_relevant_lessons(self, query_text: str, n_results: int = 3) -> List[Dict[str, any]]:
        if not self.documents_loaded or self.vector_store is None: # Check vector_store again
            logger.warning("RAG system not ready or no documents loaded. Cannot query for lessons.")
            return []

        try:
            query_results = self.vector_store.query(query_texts=[query_text], n_results=n_results)
            relevant_docs = []
            # Check if query_results and its nested lists/dictionaries are not None and not empty
            if query_results and \
               query_results.get('ids') and query_results['ids'] and query_results['ids'][0] and \
               query_results.get('documents') and query_results['documents'] and query_results['documents'][0] and \
               query_results.get('metadatas') and query_results['metadatas'] and query_results['metadatas'][0] and \
               query_results.get('distances') and query_results['distances'] and query_results['distances'][0]:

                for i in range(len(query_results['ids'][0])):
                    doc_info = {
                        'id': query_results['ids'][0][i],
                        'document_content': query_results['documents'][0][i],
                        'metadata': query_results['metadatas'][0][i],
                        'distance': query_results['distances'][0][i],
                    }
                    relevant_docs.append(doc_info)
            else:
                logger.info(f"Query for '{query_text}' returned no results or unexpected structure.")
            return relevant_docs
        except Exception as e:
            logger.error(f"Error querying for relevant lessons: {e}", exc_info=True)
            return []

if __name__ == '__main__':
    logger.info("RAG Kernel standalone test initiated.")
    # Use a different path for test data to avoid interfering with potential prod data
    test_vector_store_path = str(PROJECT_ROOT / "core" / "rag" / "vector_store_data_test")
    test_collection_name = "zaki_os_lessons_test"

    # Clean up old test data if any
    if os.path.exists(test_vector_store_path):
        import shutil
        try:
            shutil.rmtree(test_vector_store_path)
            logger.info(f"Removed old test vector store data at: {test_vector_store_path}")
        except Exception as e_rm:
            logger.error(f"Error removing old test vector store data: {e_rm}")

    rag_kernel = RAGKernel(vector_store_path=test_vector_store_path, collection_name=test_collection_name)

    if rag_kernel.vector_store and rag_kernel.vector_store.collection: # Ensure collection is also valid
        rag_kernel.initialize_and_embed_lessons(force_reindex=True) # Force reindex for testing
        count = rag_kernel.vector_store.get_collection_count()
        logger.info(f"Number of documents in RAG store ('{test_collection_name}'): {count}")

        if count > 0:
            sample_query = "How should an agent create a plan?"
            lessons = rag_kernel.get_relevant_lessons(sample_query, n_results=2)
            if lessons:
                logger.info(f"Query: '{sample_query}' -> Found {len(lessons)} relevant lessons:")
                for i, lesson in enumerate(lessons):
                    logger.info(f"  Lesson {i+1}: Source: {lesson.get('metadata', {}).get('source')}, Distance: {lesson.get('distance'):.4f if lesson.get('distance') is not None else 'N/A'}")
                    # logger.info(f" Content: {lesson.get('document_content', '')[:100]}...") # Optional: log snippet
            else:
                logger.warning(f"No relevant lessons found for query: '{sample_query}'")
    else:
        logger.error("RAG Kernel could not be initialized with a vector store or collection. Standalone test aborted.")
