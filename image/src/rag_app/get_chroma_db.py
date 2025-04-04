import shutil
import sys
import os
from langchain_community.vectorstores import Chroma

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

# Handle imports differently if run as script vs imported as module
if __name__ == "__main__":
    # When run directly, use relative import
    from get_embedding_function import get_embedding_function
else:
    # When imported, use package import
    from rag_app.get_embedding_function import get_embedding_function

# Check if running in Docker/Lambda environment
IS_USING_IMAGE_RUNTIME = bool(os.environ.get("IS_USING_IMAGE_RUNTIME", False))

# Use different paths based on runtime environment
if IS_USING_IMAGE_RUNTIME:
    # In Docker/Lambda, the path is within LAMBDA_TASK_ROOT
    CHROMA_PATH = os.path.join(os.environ.get("LAMBDA_TASK_ROOT", ""), "src", "data", "chroma")
else:
    # Local development - use project structure
    CHROMA_PATH = os.path.join(project_root, "src", "data", "chroma")

print(f"Using Chroma DB at: {CHROMA_PATH}")

CHROMA_DB_INSTANCE = None  # Reference to singleton instance of ChromaDB


def get_chroma_db():
    global CHROMA_DB_INSTANCE
    if not CHROMA_DB_INSTANCE:

        # Hack needed for AWS Lambda's base Python image (to work with an updated version of SQLite).
        # In Lambda runtime, we need to copy ChromaDB to /tmp so it can have write permissions.
        if IS_USING_IMAGE_RUNTIME:
            __import__("pysqlite3")
            sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
            copy_chroma_to_tmp()

        # Prepare the DB.
        CHROMA_DB_INSTANCE = Chroma(
            persist_directory=get_runtime_chroma_path(),
            embedding_function=get_embedding_function(),
        )
        print(f"✅ Init ChromaDB {CHROMA_DB_INSTANCE} from {get_runtime_chroma_path()}")

    return CHROMA_DB_INSTANCE


def copy_chroma_to_tmp():
    dst_chroma_path = get_runtime_chroma_path()

    if not os.path.exists(dst_chroma_path):
        os.makedirs(dst_chroma_path)

    tmp_contents = os.listdir(dst_chroma_path)
    if len(tmp_contents) == 0:
        print(f"Copying ChromaDB from {CHROMA_PATH} to {dst_chroma_path}")
        os.makedirs(dst_chroma_path, exist_ok=True)
        shutil.copytree(CHROMA_PATH, dst_chroma_path, dirs_exist_ok=True)
    else:
        print(f"✅ ChromaDB already exists in {dst_chroma_path}")


def get_runtime_chroma_path():
    if IS_USING_IMAGE_RUNTIME:
        return os.path.join("/tmp", os.path.basename(CHROMA_PATH))
    else:
        return CHROMA_PATH


if __name__ == "__main__":
    # For testing
    print("Testing ChromaDB connection...")
    db = get_chroma_db()
    print(f"ChromaDB instance: {db}")
