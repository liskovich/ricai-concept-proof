import weaviate
import os
import openai

from dotenv import load_dotenv
from typing import List

from llama_index import (
    OpenAIEmbedding,
    VectorStoreIndex,
    StorageContext,
    ServiceContext,
    set_global_service_context,
)
from llama_index.node_parser import SimpleNodeParser
from llama_index.vector_stores import WeaviateVectorStore
from llama_index.schema import Document
from llama_index.llms import OpenAI, ChatMessage
from llama_index.tools import QueryEngineTool
from llama_index.query_engine import SubQuestionQueryEngine

load_dotenv()

open_ai_key = os.environ.get("OPEN_AI_KEY")
weaviate_url = os.environ.get("WEAVIATE_URL")
weaviate_api_key = os.environ.get("WEAVIATE_API_KEY")

openai.api_key = open_ai_key


def init_weaviate():
    client = weaviate.Client(
        url=weaviate_url,
        auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_api_key),
        additional_headers={"X-OpenAI-Api-Key": open_ai_key},
    )

    schema = {
        "classes": [
            {
                "class": "BusinessDocs",
                "description": "SRS document element.",
                "vectorizer": "text2vec-openai",
                "moduleConfig": {"generative-openai": {"model": "gpt-3.5-turbo"}},
                "properties": [
                    {
                        "name": "Content",
                        "dataType": ["text"],
                        "description": "Content from the specific SRS document element.",
                    },
                    {
                        "name": "Filepath",
                        "dataType": ["text"],
                        "description": "The specific SRS document's filepath.",
                    },
                ],
            },
            {
                "class": "CodeFiles",
                "description": "SRS document element.",
                "vectorizer": "text2vec-openai",
                "moduleConfig": {"generative-openai": {"model": "gpt-3.5-turbo"}},
                "properties": [
                    {
                        "name": "Content",
                        "dataType": ["text"],
                        "description": "Content from the specific code file structure.",
                    },
                    {
                        "name": "Filepath",
                        "dataType": ["text"],
                        "description": "The specific code file's filepath.",
                    },
                ],
            },
        ]
    }

    client.schema.create(schema)
    return client


# In a production version, this would be the result of parsing the SRS document
srs_document = [
    """## Introduction
The software described in this document consists of two Python functions, `calculate_square_area` and `calculate_discounted_price`, which perform specific calculations and include conditional statements to validate input parameters. These functions are intended for general-purpose use and can be integrated into various applications.""",
    """## Purpose
The purpose of this software is to provide users with the capability to calculate the area of a square and the discounted price of an item based on specified input parameters.""",
    """### `calculate_square_area` Function
#### Description
The `calculate_square_area` function calculates the area of a square based on the length of its side.
#### Input Parameters
- `side_length` (float or int): The length of the side of the square.
#### Output
- If `side_length` is greater than 0, the function returns the calculated area (float).
- If `side_length` is not greater than 0, the function returns an error message as a string: 'Invalid input: Side length must be greater than 0.'""",
    """### `calculate_discounted_price` Function
#### Description
The `calculate_discounted_price` function calculates the discounted price of an item based on the original price and a discount percentage.
#### Input Parameters
- `original_price` (float or int): The original price of the item.
- `discount_percentage` (float or int): The discount percentage to be applied to the original price.
#### Output
- If both `original_price` and `discount_percentage` are valid (original_price > 0 and 0 <= discount_percentage <= 100), the function returns the calculated discounted price (float).
- If either `original_price` is not greater than 0 or `discount_percentage` is not within the valid range, the function returns an error message as a string: 'Invalid input: Original price must be greater than 0, and discount percentage must be between 0 and 100.'""",
    """## Non-Functional Requirements
- **Usability**: The functions should be easy to use and understand.
- **Robustness**: The functions should handle invalid input gracefully and provide clear error messages.
- **Performance**: The functions should execute efficiently for typical input values.""",
    """## Dependencies
The software has no external dependencies and can be used in any Python environment that supports the required language features.""",
]


# In a production version, this would be the result of parsing the codebase
codebase_files = [
    """
def calculate_square_area(side_length):
    if side_length > 0:
        area = side_length * side_length
        return area
    else:
        return 'Invalid input: Side length must be greater than 0'""",
    """
def calculate_discounted_price(original_price, discount_percentage):
    if original_price > 0 and 0 <= discount_percentage <= 100:
        discounted_price = original_price - (original_price * discount_percentage / 100)
        return discounted_price
    else:
        return 'Invalid input: Original price must be greater than 0, and discount percentage must be between 0 and 100'""",
]


def store_srs_doc(w_client, srs_docs):
    documents: List[Document] = [
        Document(text=doc, extra_info={"filepath": "srs_doc_1"}) for doc in srs_docs
    ]
    parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)
    nodes = parser.get_nodes_from_documents(documents)

    # Build vector store and index
    vector_store = WeaviateVectorStore(
        weaviate_client=w_client, index_name="BusinessDocs", text_key="content"
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(nodes, storage_context=storage_context)

    # Build query engine
    query_engine = index.as_query_engine()
    return query_engine


def store_code_files(w_client, codebase):
    documents: List[Document] = [
        Document(text=c, extra_info={"filepath": "codefile.py"}) for c in codebase
    ]
    parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)
    nodes = parser.get_nodes_from_documents(documents)

    # Build vector store and index
    vector_store = WeaviateVectorStore(
        weaviate_client=w_client, index_name="CodeFiles", text_key="content"
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(nodes, storage_context=storage_context)

    # Build query engine
    query_engine = index.as_query_engine()
    return query_engine


def main():
    w_client = init_weaviate()
    print(
        f"Initialized weaviate client, ready to accept requests: {w_client.is_ready()}"
    )
    print("\n--------------------------------------\n")

    # setup service context
    service_context = ServiceContext.from_defaults(
        llm=OpenAI(model="gpt-3.5-turbo", temperature=0), embed_model=OpenAIEmbedding()
    )
    set_global_service_context(service_context)

    # separate query engine tools for each of the knowledge bases
    srs_tool = QueryEngineTool.from_defaults(
        query_engine=store_srs_doc(w_client, srs_docs=srs_document),
        name="SRS document tool",
        description="Useful for answering questions about the software requirement specification of the program.",
    )

    code_tool = QueryEngineTool.from_defaults(
        query_engine=store_code_files(w_client, codebase=codebase_files),
        name="Codebase tool",
        description="Useful for answering questions about the codebase of the program.",
    )

    # a main query engine which consolidates other sub-engines
    query_engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=[
            srs_tool,
            code_tool,
        ],
        verbose=False,
    )

    response = query_engine.query(
        "Give me the code and the software requirement specification for the function calculate_discounted_price"
    )
    print(response.response)
    print("\n--------------------------------------\n")

    # OpenAI chat call that takes requirements + code and generates test case descriptions
    messages = [
        ChatMessage(
            role="system",
            content="You are a senior software tester with several years of expertise in enterprise software testing",
        ),
        ChatMessage(
            role="user",
            content=f"Generate a table in markdown which contains test cases and their descriptions given the following info: {response.response}",
        ),
    ]

    test_cases = OpenAI().chat(messages)
    print(test_cases.message.content)
    print("\n--------------------------------------\n")

    # OpenAI chat call that takes generated test cases and generates unit tests
    messages = [
        ChatMessage(
            role="system",
            content="You are a senior software tester with several years of expertise in enterprise software testing",
        ),
        ChatMessage(
            role="user",
            content=f"Generate a unit tests in pytest given the following test case descriptions: {test_cases.message.content}",
        ),
    ]

    unit_tests = OpenAI().chat(messages)
    print(unit_tests.message.content)


main()
