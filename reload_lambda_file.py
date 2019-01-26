import json
import os
from zipfile import ZipFile

import boto3

with open('config.json') as f:
    config = json.load(f)

lambda_config = config['lambda'][0]

function_zip = 'lambda.zip'

os.remove('./%s' % function_zip)

with ZipFile(function_zip, 'w') as zz:
    function_directory_path = lambda_config['FunctionDirectoryPath']
    for ff in os.listdir(function_directory_path):
        zz.write(function_directory_path + '/%s' % ff, arcname=ff)

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=config['aws_access_key_id'],
    aws_secret_access_key=config['aws_secret_access_key'],
    region_name=config['region_name']
)

with open('lambda.zip', 'rb') as f:
    zipped_code = f.read()

lambda_client.update_function_code(
    FunctionName=lambda_config['FunctionName'],
    ZipFile=zipped_code,
)
