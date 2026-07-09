import boto3

def get_bedrock_client(access_key, secret_key, region="us-east-1"):
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

def get_dynamodb_client(access_key, secret_key, region="us-east-1"):
    return boto3.resource(
        'dynamodb',
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
