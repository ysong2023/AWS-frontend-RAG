import os
import sys
from dotenv import load_dotenv

# Setup paths for both direct execution and import usage
current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_file_dir)

# Add paths to sys.path if needed
if current_file_dir not in sys.path:
    sys.path.insert(0, current_file_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load environment variables from .env file
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path)

from query_model import QueryModel
from rag_app.query_rag import query_rag

def handler(event, context):
    query_item = QueryModel(**event)
    invoke_rag(query_item)


def invoke_rag(query_item: QueryModel):
    rag_response = query_rag(query_item.query_text)
    query_item.answer_text = rag_response.response_text
    query_item.sources = rag_response.sources
    query_item.is_complete = True
    query_item.put_item()
    print(f"✅ Item is updated: {query_item}")
    return query_item


def main():
    print("Running example RAG call.")
    query_item = QueryModel(
        query_text="How long does an e-commerce system take to build?"
    )
    response = invoke_rag(query_item)
    print(f"Received: {response}")


if __name__ == "__main__":
    # For local testing.
    main()
