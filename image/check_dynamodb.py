import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print loaded environment variables (redacting secret keys)
print(f"AWS_ACCESS_KEY_ID: {os.environ.get('AWS_ACCESS_KEY_ID', 'Not set')[:5]}...")
print(f"AWS_SECRET_ACCESS_KEY: {'*' * 8}")
print(f"AWS_DEFAULT_REGION: {os.environ.get('AWS_DEFAULT_REGION', 'Not set')}")
print(f"TABLE_NAME: {os.environ.get('TABLE_NAME', 'Not set')}")

# Get table name from environment or use default
TABLE_NAME = os.environ.get("TABLE_NAME", "aws_rag")
print(f"\nChecking DynamoDB table: {TABLE_NAME}")

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

# Scan the table to get all items
try:
    response = table.scan()
    items = response.get('Items', [])
    
    if not items:
        print(f"No items found in the table {TABLE_NAME}")
    else:
        print(f"Found {len(items)} items in the table {TABLE_NAME}:")
        for i, item in enumerate(items, 1):
            print(f"\nItem {i}:")
            for key, value in item.items():
                print(f"  {key}: {value}")
            print("-" * 50)
            
except Exception as e:
    print(f"Error accessing DynamoDB: {str(e)}")
    print("\nCheck that your AWS credentials are correctly set in the .env file:")
    print("AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION") 