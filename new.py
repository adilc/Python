import boto3

ec2 = boto3.resource('ec2')

for i in ec2.instances.all():
    print("Id: " + i.id + "State: " + i.state['Name'])
    print("\tTags:")
    for idx, tag in enumerate(i.tags, start=1):
        print("\t- [{0}] Key: {1}\tValue: {2}".format(idx, tag['Key'], tag['Value'])
        )
