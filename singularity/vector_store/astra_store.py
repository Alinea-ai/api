from langchain_astradb import AstraDBVectorStore

from src.common.config import singularity_config
from src.vector_store.vector_store_base import VectorStoreBase


class AstraStore(VectorStoreBase):
    def get_collection_vstore(self, collection_name='search'):
        return AstraDBVectorStore(
            embedding=self.embedding,
            collection_name=collection_name,
            token=singularity_config.settings.ASTRA_DB_APPLICATION_TOKEN,
            api_endpoint=singularity_config.settings.ASTRA_DB_API_ENDPOINT,
        )

    def similarity_search(self, collection_name, query, k=2):
        return self.get_collection_vstore().similarity_search(query, k)

    def add_documents(self, collection_name, documents):
        return self.get_collection_vstore().add_documents(documents)
