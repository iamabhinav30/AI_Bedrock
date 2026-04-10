import boto3
import os
from dotenv import load_dotenv

load_dotenv()

client = boto3.client(
    'bedrock-runtime',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

model_id = 'apac.anthropic.claude-sonnet-4-20250514-v1:0'


