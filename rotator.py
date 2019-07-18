"""
rotator.py
Rotate AWS credentials, when MFA and role-based (assume role) access are in use.
Python requirements:
- boto3
Run:
python3 rotator.py [MFA-token-from-device]
Github source: https://janikarhunen.fi/secure-access-from-aws-cli-with-cross-account-access-and-mfa
References:
https://docs.python.org/3/library/configparser.html
https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.get_session_token
"""

import configparser
import os.path
import sys

import boto3

try:
    mfa_token = sys.argv[1]
except:
    print('Missing MFA token')
    sys.exit()

''' Allowed values between 900 - 43200 sec (12 hrs). '''
TOKEN_DURATION = 43200
REGION = 'us-east-2'

# AC customizations
creds_file = '/Users/xxxx/.aws/credentials'
mfa_arn = 'arn:aws:iam::xxxxx:mfa/ac-cli'
cli_user = 'xxxcliuser'


def get_tokens(mfa_device_arn=None, mfa_token=None):
    """ Get new session tokens with AWS Security Token Service.
        The default profile is used to get new tokens.
    """
    session = boto3.Session(profile_name=cli_user)
    client = session.client('sts')

    response = client.get_session_token(
        DurationSeconds=TOKEN_DURATION,
        SerialNumber=mfa_device_arn,
        TokenCode=mfa_token
    )

    tokens = {
        'output': 'json',
        'region': REGION,
        'aws_access_key_id': response['Credentials']['AccessKeyId'],
        'aws_secret_access_key': response['Credentials']['SecretAccessKey'],
        'aws_session_token': response['Credentials']['SessionToken']
    }

    print(f"Token expiration: {response['Credentials']['Expiration']}")

    return tokens

def rotate(credentials_file, mfa_device_arn, mfa_token):
    """ Rotate sessions tokens for AWS CLI. """

    ''' Check that the required parameters have values. '''
    if not os.path.isfile(credentials_file):
        print('Credentials file is missing!')
        sys.exit()
    if not mfa_device_arn.startswith('arn:aws:iam:'):
        print('MFA Device ARN should have a correct value.')
        sys.exit()
    if len(mfa_token) != 6:
        print('MFA Token should contain 6 characters.')
        sys.exit()

    ''' Get the new session tokens from AWS. '''
    tokens = get_tokens(mfa_device_arn, mfa_token)

    ''' Set the new tokens to credentials config file. '''
    config = configparser.ConfigParser()
    config.read(credentials_file)

    config['mfa'] = tokens

    with open(credentials_file, 'w') as configfile:
        config.write(configfile)

    print('New session tokens have been set successfully.')

    sys.exit()

if __name__ == '__main__':
    # rotate()
    rotate(creds_file, mfa_arn, mfa_token)
