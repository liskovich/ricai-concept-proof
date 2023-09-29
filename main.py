import weaviate
import os
import openai
import pytest

from dotenv import load_dotenv
from typing import List

from llama_index import (
    OpenAIEmbedding,
    VectorStoreIndex,
    StorageContext,
    ServiceContext,
    set_global_service_context,
    load_index_from_storage,
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

    # client.schema.create(schema)
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
        # correct calculation
        # discounted_price = original_price - (original_price * discount_percentage / 100)
        
        # calculation with error (multiplying by 2 was not required)
        discounted_price = original_price - (2 * original_price * discount_percentage / 100)
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
    return index


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
    return index


def generate_suggestions(code_feature):
    # "place the test report table here (for demo purposes copy from the cmd line directly!)
    test_suite_results = """

    """
    # place your previously generated unit test code here (for demo purposes copy from the cmd line directly!)
    genereated_unit_tests = """
    
    """

    # OpenAI chat call to generate feedback / suggest fixes to our code
    messages = [
        ChatMessage(
            role="system",
            content="You are a senior software tester with several years of expertise in enterprise software testing, you are given some code, the tests for it, test report and you need to provide suggestions on how to fix bugs in the code.",
        ),
        ChatMessage(
            role="user",
            content=f"Generate the feedback and suggestions on how to improve the following code \n{code_feature}\n given unit tests: \n{genereated_unit_tests}\n and the test run report: \n{test_suite_results}\n",
        ),
    ]

    code_fix_suggest = OpenAI().chat(messages)
    print(code_fix_suggest.message.content)


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

    # retrieve index
    try:
        srs_vector_store = WeaviateVectorStore(
            weaviate_client=w_client, index_name="BusinessDocs", text_key="content"
        )
        code_vector_store = WeaviateVectorStore(
            weaviate_client=w_client, index_name="CodeFiles", text_key="content"
        )
        srs_storage_context = StorageContext.from_defaults(
            vector_store=srs_vector_store
        )
        code_storage_context = StorageContext.from_defaults(
            vector_store=code_vector_store
        )

        srs_index = load_index_from_storage(storage_context=srs_storage_context)
        code_index = load_index_from_storage(storage_context=code_storage_context)
    except:
        srs_index = store_srs_doc(w_client, srs_docs=srs_document)
        code_index = store_code_files(w_client, codebase=codebase_files)

    # From here we can build a query engine, but for demo I will directly use weawiate python client
    # query weaviate to retrieve SRS document and code
    prompt = "calculate_discounted_price"

    srs_response = (
        w_client.query.get("BusinessDocs", properties=["content"])
        .with_bm25(query=prompt)
        .with_limit(1)
        .do()
    )
    srs_doc_feature = srs_response["data"]["Get"]["BusinessDocs"][0]["content"]

    print(srs_doc_feature)
    print("\n--------------------------------------\n")

    code_response = (
        w_client.query.get("CodeFiles", properties=["content"])
        .with_bm25(query=prompt)
        .with_limit(1)
        .do()
    )
    code_feature = code_response["data"]["Get"]["CodeFiles"][0]["content"]

    print(code_feature)
    print("\n--------------------------------------\n")

    # OpenAI chat call that takes requirements + code and generates test case descriptions
    messages = [
        ChatMessage(
            role="system",
            content="You are a senior software tester with several years of expertise in enterprise software testing",
        ),
        ChatMessage(
            role="user",
            content=f"Generate a table in markdown which contains test cases and their descriptions given the following code: \n{code_feature}\n and its functionality requirements: \n{srs_doc_feature}\n",
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
            content=f"Generate unit tests in pytest given the following test case descriptions: \n{test_cases.message.content}\n as well as the functionality requirements its requirements: \n{srs_doc_feature}\n",
        ),
    ]

    unit_tests = OpenAI().chat(messages)
    print(unit_tests.message.content)
    print("\n--------------------------------------\n")

    # TODO: uncomment after running the tests and recieving a test report
    # generate_suggestions(code_feature)


# TODO: uncomment to run the overall demo agent workflow
# main()


def run_tests():
    pytest.main(
        ["-s", "--md-report", "--md-report-verbose=1", "tests/test_sample_code.py"]
    )


# TODO: uncomment to run unit tests
# run_tests()
