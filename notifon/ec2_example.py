!#/usr/bin/python3
# coding: utf-8

import boto3
import os, stat

session = boto3.Session()
ec2 = session.resource('ec2')

key_name = 'ac-python'

key = ec2.create_key_pair(KeyName=key_name)
    
key_path = key_name + '.pem'
with open(key_path, 'w') as key_file:
    key_file.write(key.key_material)
    
os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)

ami_name = 'amzn2-ami-hvm-2.0.20190618-x86_64-gp2'
filters = [{'Name': 'name', 'Values': [ami_name]}]
imglist = list(ec2.images.filter(Owners=['amazon'], Filters = filters))
img = imglist[0]

instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName=key.key_name)
inst = instances[0]

sg = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])
sg.authorize_ingress(IpPermissions=[{'FromPort':22, 'ToPort':22, 'IpProtocol':'TCP', 'IpRanges': [{'CidrIp':'72.194.185.130/32'}]}])
