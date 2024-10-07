import boto3
def get_dynamodb_client(region_name='ap-south-1'):
    return boto3.client(
        'dynamodb',
        aws_access_key_id="access key",
        aws_secret_access_key="access key",
        region_name=region_name
    )

def get_dynamodb_resource(region_name='ap-south-1'):
    return boto3.resource(
        'dynamodb',
        aws_access_key_id="access key",
        aws_secret_access_key="access key",
        region_name=region_name
    )

def test_dynamodb_connection():
    try:
        # Create a DynamoDB client using the default credentials
        dynamodb_client = get_dynamodb_client()

        # List DynamoDB tables
        response = dynamodb_client.list_tables()

        # Print the table names
        print("Successfully connected to DynamoDB. Tables:")
        for table_name in response['TableNames']:
            print(table_name)

        return True

    except Exception as e:
        print(f"Error connecting to DynamoDB: {e}")
        return False