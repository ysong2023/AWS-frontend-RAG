# AWS RAG Project - Initialization Guide

## Date: April 4, 2024

## Overview

This document provides step-by-step instructions for initializing and deploying the RAG (Retrieval-Augmented Generation) project. It covers both local testing using Docker and cloud deployment using AWS CDK.

## Prerequisites

1. Docker Desktop installed and running
2. AWS CLI configured with valid credentials
3. Node.js and npm installed (for CDK deployment)
4. OpenAI API key available

## Local Testing with Docker

### Step 1: Navigate to the project directory
```powershell
cd C:\Path\to\project\deploy-rag-to-aws\image
```

### Step 2: Create/update .env file with credentials
```powershell
# Example .env file content
OPENAI_API_KEY=sk-your-api-key
TABLE_NAME=local-table
```

### Step 3: Build the Docker image
```powershell
docker build --platform linux/amd64 -t aws_rag_app .
```

### Step 4: Run the API server (for interactive testing)
```powershell
docker run --rm -p 8000:8000 `
    --entrypoint python `
    --env-file .env `
    aws_rag_app src/app_api_handler.py
```

### Step 5: Run the worker process (for testing background processing)
```powershell
docker run --rm -it `
    --entrypoint python `
    --env-file .env `
    aws_rag_app src/app_work_handler.py
```

### Step 6: Access the API documentation
Open a browser and navigate to: `http://localhost:8000/docs`

## AWS Deployment with CDK

### Step 1: Navigate to the CDK project directory
```powershell
cd C:\Path\to\project\deploy-rag-to-aws\rag-cdk-infra
```

### Step 2: Install CDK dependencies
```powershell
npm install
```

### Step 3: Build the TypeScript project
```powershell
npm run build
```

### Step 4: Bootstrap CDK in your AWS account (first-time only)
```powershell
cdk bootstrap
```

### Step 5: Deploy the infrastructure
```powershell
cdk deploy
```

### Step 6: After deployment, capture the Function URL
The URL will be displayed in the outputs section after deployment completes. It will look like:
```
Outputs:
RagCdkInfraStack.FunctionUrl = https://xxxxxxxxxxxx.lambda-url.us-east-1.on.aws/
```

## Common Issues and Solutions

### Docker Image Build Failures
- Ensure Docker Desktop is running
- Check that the Dockerfile references correct paths
- Verify all required files are present in the src directory

### CDK Deployment Issues
- Make sure AWS credentials are properly configured with `aws configure`
- Check for Node.js in PATH with `node -v` (if not found, use `$env:Path += ";C:\Program Files\nodejs\"`)
- Verify AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are set

### Lambda Configuration Issues
- Verify Lambda functions have DynamoDB permissions
- Ensure OpenAI API key is set in environment variables
- Check that CloudWatch logs do not show errors

## Environment Variable Requirements

### Local Docker Environment
- OPENAI_API_KEY: Your OpenAI API key
- IS_USING_IMAGE_RUNTIME: Set to "True"

### AWS Lambda Environment (set by CDK)
- TABLE_NAME: DynamoDB table name
- WORKER_LAMBDA_NAME: Worker Lambda function name
- OPENAI_API_KEY: Your OpenAI API key (must be added manually)
- IS_USING_IMAGE_RUNTIME: Set to "True"

## Testing the Deployment

1. Access the API documentation: `https://your-function-url/docs`
2. Submit a query through the `/submit_query` endpoint
3. Wait 10-15 seconds for asynchronous processing
4. Use the query_id to check results via the `/get_query` endpoint

## Notes

- Asynchronous processing means query results won't be immediately available
- The worker function processes queries in the background 
- The first invocation may have cold start latency (10+ seconds)
- For a full rebuild and redeploy, run `cdk destroy` before `cdk deploy` 