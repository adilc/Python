import boto3 

sqs = boto3.resource('sqs')

queue = sqs.get_queue_by_name(QueueName='AC_SQS')

response = queue.send_message(MessageBody = 'test message')
print(response.get('MessageId'))