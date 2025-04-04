import os
import sys
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

# Setup paths for both direct execution and import usage
current_file_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_file_dir)
project_root = os.path.dirname(src_dir)

# Add paths to sys.path if needed
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load environment variables
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path)

def get_embedding_function():
    # Check if OPENAI_API_KEY is in env
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY not found in environment variables")
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return embeddings

if __name__ == "__main__":
    # For testing
    print("Testing embedding function...")
    embedding_function = get_embedding_function()
    print(f"Embedding function type: {type(embedding_function)}")
