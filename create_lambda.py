#!/usr/bin/env python3

import json
import os
from zipfile import ZipFile

import boto3


def create_lambda():
    with open('config.json') as f:
        config = json.load(f)

    lambda_config = config['lambda'][0]

    function_zip = 'lambda.zip'

    os.remove('./%s' % function_zip)

    with ZipFile(function_zip, 'w') as zz:
        function_directory_path = lambda_config['FunctionDirectoryPath']
        for ff in os.listdir(function_directory_path):
            zz.write(function_directory_path + '/%s' % ff, arcname=ff)

    iam_client = boto3.client(
        'iam',
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'],
        region_name=config['region_name']
    )

    """
    role_policy_document = {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "",
          "Effect": "Allow",
          "Principal": {
            "Service": "lambda.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
    iam_client.create_role(
      RoleName='LambdaBasicExecution',
      AssumeRolePolicyDocument=json.dumps(role_policy_document),
    )
    """

    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'],
        region_name=config['region_name']
    )

    with open(function_zip, 'rb') as f:
        zipped_code = f.read()

    role = iam_client.get_role(RoleName='LambdaBasicExecution')
    lambda_client.create_function(
        FunctionName=lambda_config['FunctionName'],
        Runtime=lambda_config['Runtime'],
        Role=role['Role']['Arn'],
        Handler=lambda_config['Handler'],
        Code=dict(ZipFile=zipped_code),
        Timeout=300
    )




if __name__ == "__main__":
    create_lambda()
