# AWS RAG Project - Bedrock to OpenAI Migration

**Date:** 2024-04-04  
**Project:** AWS RAG Serverless Deployment  
**Author:** Claude & User  

## Project Aim
Deploy a Retrieval-Augmented Generation (RAG) application on AWS serverlessly, with API endpoints for querying the system.

## Overview
This project uses a FastAPI application to provide API endpoints for a RAG system. The original implementation used AWS Bedrock for embeddings and LLM responses, but due to access limitations, we've migrated to using OpenAI API instead.

## Progress

### 1. Migration from AWS Bedrock to OpenAI
- Successfully replaced Bedrock embeddings with OpenAI embeddings
- Updated the query system to use ChatGPT instead of Claude
- Fixed environment variable loading to ensure API keys are properly accessed

### 2. Fixed Database Path Issues
- Resolved inconsistency between relative and absolute paths
- Ensured the Chroma vector database was correctly populated and accessible
- Added debugging to verify document retrieval

### 3. Verified RAG System Functionality
- Confirmed the system can correctly retrieve pricing information from documents
- Tested the API functionality through direct module execution

## Key Code Changes

### 1. Migration to OpenAI Embeddings
```python
# Original Bedrock implementation
from langchain_aws import BedrockEmbeddings

def get_embedding_function():
    embeddings = BedrockEmbeddings()
    return embeddings
```

```python
# Updated OpenAI implementation
from langchain_openai import OpenAIEmbeddings

def get_embedding_function():
    # Use OpenAI embeddings instead of Bedrock
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return embeddings
```

### 2. Updated LLM Model
```python
# Original Bedrock LLM
from langchain_aws import ChatBedrock
model = ChatBedrock(model_id=BEDROCK_MODEL_ID)
```

```python
# Updated OpenAI LLM
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model=OPENAI_MODEL)
```

### 3. Environment Variable Loading
```python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
```

### 4. Fixed Chroma Database Path
```python
# Consistent path used across all files
CHROMA_PATH = "src/data/chroma"
```

## Modified Files
1. `src/rag_app/get_embedding_function.py` - Changed from Bedrock to OpenAI embeddings
2. `src/rag_app/query_rag.py` - Switched from ChatBedrock to ChatOpenAI
3. `src/rag_app/get_chroma_db.py` - Fixed path issues and added debugging
4. `populate_database.py` - Added dotenv loading and debugging
5. `src/app_api_handler.py` - Added dotenv loading for environment variables
6. `src/app_work_handler.py` - Added dotenv loading for environment variables

## Next Steps

### 1. Complete FastAPI Testing
- Run the API server locally: `python src/app_api_handler.py`
- Test the `/submit_query` endpoint with a POST request:
  ```bash
  curl -X POST "http://localhost:8000/submit_query" -H "Content-Type: application/json" -d '{"query_text":"What is the price of Landing Page for Small Businesses?"}'
  ```
- Verify the synchronous response containing the query_id
- Check that the answer was stored in the local database

### 2. AWS CDK Infrastructure Updates
- Modify the CDK stack (`deploy-rag-to-aws/rag-cdk-infra/lib/rag-cdk-infra-stack.ts`) to:
  - Add OpenAI API key to the Lambda function environment variables
  - Remove or replace the `AmazonBedrockFullAccess` policy with appropriate permissions
  - Consider using AWS Secrets Manager for the OpenAI API key
- Build and deploy the updated infrastructure:
  ```bash
  cd rag-cdk-infra
  npm install
  cdk deploy
  ```

### 3. Docker Container Updates
- Update the Dockerfile to include the OpenAI API requirements
- Ensure the .env file handling is properly set up for container use
- Make sure the Chroma DB persists correctly in the container environment
- Test building the Docker image locally:
  ```bash
  cd image
  docker build -t rag-api .
  ```

### 4. DynamoDB Integration
- Test DynamoDB integration locally using AWS CLI
- Ensure the QueryModel class is correctly interacting with DynamoDB
- Set up local DynamoDB for testing if needed

### 5. Final Deployment Steps
- Prepare the vector database for deployment
- Update environment variables for production
- Configure proper logging and monitoring
- Document the API endpoints and usage

### 6. Security and Performance
- Review and secure API key handling
- Test performance with larger document collections
- Implement caching if needed
- Add authentication to API endpoints if required

## Docker and AWS Recommendations

### Docker Updates
1. **Update requirements.txt:**
   - Ensure `langchain-openai` and `python-dotenv` are included
   - Remove any unnecessary Bedrock-specific packages

2. **Dockerfile Modifications:**
   - Update the current Dockerfile to copy the .env file (with secure handling)
   ```dockerfile
   # Add this line to copy the .env file
   COPY .env ${LAMBDA_TASK_ROOT}
   ```
   - Consider using multi-stage builds to improve security
   - Ensure all required source directories are properly copied

3. **Environment Variables:**
   - Modify the Dockerfile to set default environment variables if needed
   ```dockerfile
   # Set environment variables
   ENV IS_USING_IMAGE_RUNTIME=True
   ENV CHROMA_PATH=data/chroma
   ```

### AWS Lambda Setup
1. **Secret Management:**
   - Store the OpenAI API key in AWS Secrets Manager
   - Update the Lambda functions to retrieve the secret at runtime

2. **IAM Policy Changes:**
   - Replace the Bedrock policy with minimal required permissions
   - Add permissions to access Secrets Manager if used

3. **Lambda Configuration:**
   - Increase memory allocation if needed for embedding operations
   - Adjust timeouts based on performance testing

4. **CDK Modifications:**
   ```typescript
   // Add Secrets Manager access
   const openAiSecret = secretsmanager.Secret.fromSecretNameV2(
     this, 'OpenAiApiKey', 'openai/api-key'
   );
   
   // Grant Lambda access to the secret
   openAiSecret.grantRead(workerFunction);
   openAiSecret.grantRead(apiFunction);
   
   // Remove Bedrock policy and add appropriate policies
   // workerFunction.role?.addManagedPolicy(
   //   ManagedPolicy.fromAwsManagedPolicyName("AmazonBedrockFullAccess")
   // );
   ```

5. **DynamoDB Configuration:**
   - No changes needed as the existing setup works with the OpenAI integration

These recommendations provide a clear path to deploy the updated OpenAI-based RAG system to AWS Lambda while maintaining security best practices. 