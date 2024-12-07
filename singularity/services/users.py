import os
import json
from typing import Dict, Any

from django.shortcuts import get_object_or_404
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from alinea_api.models import (
    AccessRequest,
    AccessRequestItem
)
from alinea_api.views.document import document_service

from singularity.llms.open_ai import get_opneai


class UserService:

    def __init__(self):
        self.llm = get_opneai()
        self.prompt = PromptTemplate(
            input_variables=["documents"],
            template="""
            You are an assistant that summarizes user information based on provided documents.
            
            Here are the approved documents:
            
            {documents}
            
            Please provide a concise and coherent summary of the user's information.
            """
        )

    def get_documents_summary(self, access_request_id: int) -> str:
        data_by_status: Dict[str, Any] = {'pending': [], 'approved': [], 'rejected': []}

        if not access_request_id:
            return ""
        access_request_obj = get_object_or_404(AccessRequest, id=access_request_id)
        data_by_status = {'pending': [], 'approved': [], 'rejected': []}
        access_requests = AccessRequestItem.objects.filter(access_request_id=access_request_id)

        for access_request in access_requests:
            data_by_status[access_request.status].append(access_request.data_type)
        user = access_request_obj.user
        user_doc = document_service.find_user_by_user_id(user.id)
        if not user_doc:
            return "no info found for user"
        data = {}
        for data_type in data_by_status['approved']:
            if data_type in user_doc:
                data[data_type] = user_doc[data_type]
            else:
                data[data_type] = None
        data_by_status["approved"] = data

        # Create a LangChain prompt and generate the summary
        try:
            summary = self._generate_summary(str(data_by_status))
        except Exception as e:
            # Handle exceptions such as API errors
            return f"An error occurred while generating the summary: {str(e)}"

        return summary

    def _prepare_documents_text(self, approved_data: Dict[str, Any]) -> str:
        """
        Converts the approved data dictionary into a structured text format suitable for the LLM.
        """
        documents = ""
        for data_type, data in approved_data.items():
            if data:
                documents += f"### {self._format_data_type(data_type)}\n"
                # Convert the data dictionary to a JSON string for better readability
                documents += f"{json.dumps(data, indent=2)}\n\n"
            else:
                documents += f"### {self._format_data_type(data_type)}\nNo data available.\n\n"
        return documents

    def _format_data_type(self, data_type: str) -> str:
        """
        Formats the data type string to a more readable form.
        """
        return data_type.replace('_', ' ').title()

    def _generate_summary(self, documents: str) -> str:
        """
        Uses LangChain and OpenAI to generate a summary from the provided documents.
        """
        # Create a chain with the prompt template and LLM
        chain = LLMChain(llm=self.llm, prompt=self.prompt)
        summary = chain.run(documents=documents)
        return summary
