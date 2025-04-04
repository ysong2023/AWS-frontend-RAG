# AWS RAG Project - Deployment to AWS Lambda

## Date: April 4, 2024

## Overview

This document outlines the process of deploying our RAG (Retrieval-Augmented Generation) application to AWS Lambda using CDK. The deployment includes setting up DynamoDB for query storage, Lambda functions for API and worker processing, and integrating with OpenAI for embeddings and completions.

## Deployment Architecture

The deployed infrastructure consists of:

1. **DynamoDB Table**: Stores queries, responses, and metadata
2. **API Lambda Function**: Handles incoming requests and stores queries
3. **Worker Lambda Function**: Processes queries asynchronously, retrieves context from ChromaDB, and generates answers
4. **Function URL**: Provides public access to the API function

## Key Challenges & Solutions

### 1. Path Handling Issues

- **Problem**: Import path inconsistencies across different environments
- **Solution**: Created a `path_helper.py` file to manage imports consistently and added code to properly set up Python paths in all relevant files

### 2. Dockerfile Configuration

- **Problem**: The Docker build was failing with file not found errors
- **Solution**: Updated the Dockerfile to:
  - Correctly reference files within the src directory
  - Set appropriate paths for ChromaDB
  - Use proper CMD handler paths

### 3. Lambda Permission Issues

- **Problem**: Lambda functions couldn't read/write to DynamoDB
- **Solution**: Added IAM policies to both functions to grant DynamoDB access (AmazonDynamoDBFullAccess)

### 4. Missing OpenAI API Key

- **Problem**: Worker function couldn't process queries due to missing OpenAI credentials
- **Solution**: Added the OpenAI API key as an environment variable in the worker Lambda function

### 5. Asynchronous Processing Understanding

- **Problem**: Queries appeared incomplete immediately after submission
- **Solution**: Identified this was expected behavior due to asynchronous processing, requiring a short wait between submission and retrieval

## Implementation Details

### CDK Infrastructure Changes

- Removed Bedrock permissions that were no longer needed
- Updated handler paths to reference files in the src directory
- Deployed with explicit region and account configuration

### Lambda Function Environment Variables

- **API Function**:
  - TABLE_NAME: Name of the DynamoDB table
  - WORKER_LAMBDA_NAME: Name of the worker function

- **Worker Function**:
  - TABLE_NAME: Name of the DynamoDB table
  - OPENAI_API_KEY: API key for authentication with OpenAI
  - IS_USING_IMAGE_RUNTIME: Set to True to handle Lambda environment

## Testing Results

The deployment was successfully tested with:

1. API connectivity via the Function URL
2. Query submission functionality
3. Asynchronous processing by the worker function
4. Data retrieval with accurate answers
5. ChromaDB integration for context-based retrieval

## Next Steps

1. **Optimize ChromaDB handling**: Consider using a more persistent solution for vector storage
2. **Improve error handling**: Add more robust error handling and message formatting
3. **Enhance security**: Implement more specific IAM permissions following the principle of least privilege
4. **Monitoring**: Set up CloudWatch alarms and dashboards for operational visibility
5. **CI/CD Pipeline**: Automate the deployment process with proper testing 