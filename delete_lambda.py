#!/usr/bin/env python3

import json

import boto3

with open('config.json') as f:
    config = json.load(f)

function_name = config['lambda'][0]['FunctionName']

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=config['aws_access_key_id'],
    aws_secret_access_key=config['aws_secret_access_key'],
    region_name=config['region_name']
)

response = lambda_client.delete_function(
    FunctionName=function_name
)

print(response)
