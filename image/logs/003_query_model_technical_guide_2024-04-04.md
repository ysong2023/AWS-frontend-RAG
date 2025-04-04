# How the RAG System in image/ Works

**Date:** April 4, 2024  
**Author:** Claude  
**Type:** Educational Overview

## 1. The Big Picture
This is a Retrieval-Augmented Generation (RAG) system packaged inside a Docker container, designed to be deployed to AWS Lambda. It has two main functions:
- Answer questions based on your documents
- Remember the questions and answers in a database

## 2. The Key Components

### Vector Database (ChromaDB)
Think of this as a "smart bookshelf" that can find document snippets related to any question. It works by:
- Converting text into mathematical vectors (embeddings) using OpenAI
- Organizing these vectors so similar content is grouped together
- Quickly retrieving the most relevant content when asked a question

### DynamoDB
This is like the system's "memory" - it remembers all questions, answers, and where the information came from. Each query gets:
- A unique ID (like a receipt number)
- Timestamps of when it was created
- The original question
- The AI-generated answer
- Source documents used to create the answer

### FastAPI Application
This is the "front desk" where users submit their questions:
- Provides a clean, modern API
- Handles both synchronous (immediate) and asynchronous (background) processing
- Converts to AWS Lambda functions when deployed

## 3. The Data Flow

When a user asks a question:

1. **Question Submission**: The question arrives at the FastAPI endpoint (`/submit_query`)
2. **Vector Search**: The system searches ChromaDB for relevant document snippets
3. **Context Assembly**: The most relevant snippets are combined into a context
4. **LLM Processing**: OpenAI's model generates an answer based on this context
5. **Storage**: The question, answer, and sources are saved to DynamoDB
6. **Response**: The answer is returned to the user

## 4. The File Structure

- **data/**: The information hub
  - **chroma/**: Vector database files
  - **source/**: Your original PDF documents

- **src/**: The brain of the operation
  - **rag_app/**: Core RAG functionality
    - **get_embedding_function.py**: Creates text embeddings
    - **get_chroma_db.py**: Manages the vector database
    - **query_rag.py**: Performs the actual RAG operations
  - **app_api_handler.py**: Handles API requests
  - **app_work_handler.py**: Processes queries as background tasks
  - **query_model.py**: Defines the data structure and DynamoDB interactions

- **Dockerfile**: Packages everything for AWS Lambda
- **.env**: Stores your API keys and configuration
- **populate_database.py**: Loads your documents into ChromaDB

## 5. Key Improvements We Made

1. **Path Handling**: Ensured consistent paths across all files
2. **Database Structure**: Fixed ChromaDB directory location
3. **DynamoDB Integration**: Set the correct partition key (`query_id`)
4. **Environment Variables**: Ensured proper loading in all components
5. **Error Handling**: Added better error reporting

Everything in the image/ folder now works together seamlessly, with proper paths, database connections, and environment variable handling. 