import boto3

sqs = boto3.resource('sqs')

queue = sqs.create_queue(QueueName="ac-sqs-boto")

print(queue.url)