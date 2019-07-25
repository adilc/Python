import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('ac-test')

Username = input("Enter Username  ")

table.put_item(
    Item={
        'Username': Username,
        'Name': 'Jane',
        'Lastname': 'Doe',
        'Age': 25
    }
)



