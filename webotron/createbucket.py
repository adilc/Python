import boto3
session = boto3.Session()

s3 = session.resource('s3')

new_bucket = s3.create_bucket(Bucket='acpython', CreateBucketConfiguration = {'LocationConstraint': 'us-east-2'})

