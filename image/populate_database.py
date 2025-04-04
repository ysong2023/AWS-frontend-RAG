import argparse
import os
import shutil
import sys
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.vectorstores import Chroma

# Setup paths for both direct execution and import usage
current_file_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_file_dir, "src")

# Add src directory to the Python path
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
if current_file_dir not in sys.path:
    sys.path.insert(0, current_file_dir)

# Load environment variables from .env file
dotenv_path = os.path.join(current_file_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)

from src.rag_app.get_embedding_function import get_embedding_function

# Use os.path for path handling
CHROMA_PATH = os.path.join(current_file_dir, "src", "data", "chroma")
DATA_SOURCE_PATH = os.path.join(current_file_dir, "src", "data", "source")

def main():
    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    parser.add_argument("--info", action="store_true", help="Show information about the database.")
    args = parser.parse_args()
    
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    if args.info:
        print(f"Database Path: {CHROMA_PATH}")
        print(f"Source Path: {DATA_SOURCE_PATH}")
        if os.path.exists(CHROMA_PATH):
            print(f"Database exists at {CHROMA_PATH}")
            try:
                db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
                collection = db.get()
                print(f"Collection contains {len(collection['ids'])} documents")
            except Exception as e:
                print(f"Error accessing database: {e}")
        else:
            print(f"Database does not exist at {CHROMA_PATH}")
        return

    # Create (or update) the data store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def load_documents():
    document_loader = PyPDFDirectoryLoader(DATA_SOURCE_PATH)
    return document_loader.load()


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=120,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):
    # Load the existing database.
    print(f"Creating/loading Chroma database at: {CHROMA_PATH}")
    print(f"Type of embedding function: {type(get_embedding_function())}")
    
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )
    print(f"Successfully created/loaded Chroma database")

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)
    print(f"Calculated chunk IDs for {len(chunks_with_ids)} chunks")
    
    for chunk in chunks:
        print(f"Chunk Page Sample: {chunk.metadata['id']}\n{chunk.page_content}\n\n")

    # Add or Update the documents.
    try:
        existing_items = db.get(include=[])  # IDs are always included by default
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")
    except Exception as e:
        print(f"Error getting existing items: {e}")
        existing_ids = set()
        print("Continuing with empty existing_ids")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        try:
            db.add_documents(new_chunks, ids=new_chunk_ids)
            print("✅ Successfully added documents to database")
            
            # Verify documents were added
            try:
                updated_items = db.get(include=[])
                print(f"After adding, database contains {len(updated_items['ids'])} documents")
            except Exception as e:
                print(f"Error verifying added documents: {e}")
        except Exception as e:
            print(f"❌ Error adding documents to database: {e}")
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the chunk meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print(f"Database at {CHROMA_PATH} has been cleared")
    else:
        print(f"No database found at {CHROMA_PATH}")


if __name__ == "__main__":
    main()
