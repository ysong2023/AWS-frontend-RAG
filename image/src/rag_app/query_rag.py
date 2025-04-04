from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv
import os
import sys

# Setup paths for both direct execution and import usage
current_file_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_file_dir)
project_root = os.path.dirname(src_dir)

# Add src directory to path if not already there
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Add project root to path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load environment variables from .env file
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path)

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Handle imports differently if run as script vs imported as module
if __name__ == "__main__":
    # When run directly, use relative import
    from get_chroma_db import get_chroma_db
else:
    # When imported, use package import
    from rag_app.get_chroma_db import get_chroma_db

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# OpenAI model instead of Bedrock
OPENAI_MODEL = "gpt-3.5-turbo"


@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    sources: List[str]


def query_rag(query_text: str) -> QueryResponse:
    db = get_chroma_db()

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=3)
    
    # Debug: Print the documents that were found
    print("\nDebug - Retrieved documents:")
    for i, (doc, score) in enumerate(results):
        print(f"Document {i+1} (score: {score:.4f}):")
        print(f"Content: {doc.page_content[:200]}...")
        print(f"Metadata: {doc.metadata}")
        print("-" * 50)
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = ChatOpenAI(model=OPENAI_MODEL)
    response = model.invoke(prompt)
    response_text = response.content

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    print(f"Response: {response_text}\nSources: {sources}")

    return QueryResponse(
        query_text=query_text, response_text=response_text, sources=sources
    )


if __name__ == "__main__":
    # Allow running directly with command line arguments
    import sys
    
    if len(sys.argv) > 1:
        query_text = sys.argv[1]
        print(f"\nQuerying with: {query_text}\n")
        query_rag(query_text)
    else:
        # Default query if no arguments provided
        print("\nNo query provided, using default query:\n")
        query_rag("What is the price of Landing Page for Small Businesses in dollars?")
