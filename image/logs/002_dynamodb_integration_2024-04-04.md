# AWS RAG Project - DynamoDB Integration

**Date:** April 4, 2024  
**Author:** Claude  
**Status:** Completed ✅

## Aim
This log documents the successful integration of DynamoDB with our RAG application and explains the overall system architecture and workflow.

## Overview
The application is a Retrieval-Augmented Generation (RAG) system that:
1. Stores documents in a vector database (ChromaDB)
2. Accepts user queries via a FastAPI endpoint
3. Retrieves relevant documents based on the query
4. Generates responses using OpenAI's language model
5. Stores query/response pairs in DynamoDB for persistence

## Progress Made
- Successfully configured DynamoDB integration with the correct partition key (`query_id`)
- Verified data is properly saved to the DynamoDB table
- Fixed path handling in all Python files for consistent execution
- Ensured proper environment variable loading across all components
- Corrected data directory structure to avoid duplication

## Key Components and Their Roles

### 1. Data Storage and Retrieval
- **ChromaDB**: Vector database that stores document embeddings for semantic search
- **DynamoDB**: NoSQL database that persists query/response pairs 
- **Directory Structure**:
  - `data/chroma/`: Contains the vector database
  - `data/source/`: Contains the source documents (PDFs) to be indexed

### 2. Core RAG Components
- **get_embedding_function.py**: Creates embeddings using OpenAI's embedding model
- **get_chroma_db.py**: Manages connections to ChromaDB, handles path resolution
- **query_rag.py**: Core RAG logic - retrieves documents and generates responses
- **query_model.py**: Defines the data model for queries and DynamoDB interaction

### 3. Application Interfaces
- **app_api_handler.py**: FastAPI server that exposes endpoints for querying
- **app_work_handler.py**: Worker component that processes queries asynchronously

## DynamoDB Integration
The application uses DynamoDB to store and retrieve queries:

1. **Table Structure**:
   - Table Name: `aws_rag`
   - Partition Key: `query_id` (String)
   - Other Fields: `create_time`, `query_text`, `answer_text`, `sources`, `is_complete`

2. **Data Flow**:
   - When a query is submitted, a unique `query_id` is generated
   - The RAG system processes the query and generates a response
   - The result is saved to DynamoDB with complete metadata
   - The query can be retrieved later using its ID

3. **Environment Configuration**:
   - AWS credentials and region are stored in the `.env` file
   - The environment variables are loaded at runtime
   - Boto3 is used to interact with AWS services

## Next Steps
1. Create additional documentation for deployment steps
2. Enhance error handling for AWS credential issues
3. Implement pagination for large result sets
4. Add monitoring and logging for production use

## Resources
- [AWS DynamoDB Documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction) 