import os
from abc import ABC, abstractmethod

import PyPDF2
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.common.config import singularity_config


class VectorStoreBase(ABC):
    def __init__(self, embedding=None, chunk_size=2000, chunk_overlap=100):
        self.embedding = embedding or OpenAIEmbeddings(api_key=singularity_config.settings.OPEN_AI_KEY)

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len, is_separator_regex=False
        )

    @abstractmethod
    def get_collection_vstore(self):
        """Return the VectorStore instance"""

    @abstractmethod
    def add_documents(self, collection_name: str, documents):
        """Add the documents to the VectorStore"""

    @abstractmethod
    def similarity_search(self, collection_name: str, query, k=5):
        """Return the search results"""

    def load_pdf_file(self, file, collection):
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        docs = self.text_splitter.create_documents([text])
        self.add_documents(documents=docs, collection_name=collection)

    def load_pdf_files_in_directory(self, directory):
        # Iterate through all files in the specified directory
        for filename in os.listdir(directory):
            if filename.endswith('.pdf'):
                filepath = os.path.join(directory, filename)
                # Extract text from the PDF file
                with open(filepath, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                # Split the text into chunks and create LangChain documents
                docs = self.text_splitter.create_documents([text])
                # Add the documents to the AstraDBVectorStore
                inserted_ids = self.add_documents(docs)
                print(f'Inserted document {filename} with IDs: {inserted_ids}')
