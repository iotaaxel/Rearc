
#### Part 1: AWS S3 & Sourcing Datasets
"""
1. Republish [this open dataset](https://download.bls.gov/pub/time.series/pr/) in Amazon S3 and share with us a link.
    - You may run into 403 Forbidden errors as you test accessing this data. There is a way to comply with the BLS data access policies and re-gain access to fetch this data programatically - we have included some hints as to how to do this at the bottom of this README in the Q/A section.
2. Script this process so the files in the S3 bucket are kept in sync with the source when data on the website is updated, added, or deleted.
    - Don't rely on hard coded names - the script should be able to handle added or removed files.
    - Ensure the script doesn't upload the same file more than once.
"""

import boto3
import requests
import hashlib
import json
import time
from botocore.exceptions import ClientError

# Configuration
BUCKET_NAME = 'my-bucket'
URL = 'https://download.bls.gov/pub/time.series/pr/'
DATA_DIR = 'data/' # local directory to store the downloaded files/data
ACCESS_KEY_ID = 'access-key-id' # From AWS IAM role or AWS account
SECRET_ACCESS = 'secret-access-key' # From AWS IAM role or AWS account
MAX_RETRIES = 3
RETRY_DELAY = 10 # in seconds
# WAIT_TIME = 5
# REGION = 'us-east-1'

# S3 client
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS)

def file_exists_in_s3(filename, etag):
    try:
        response = s3.head_object(Bucket=BUCKET_NAME, Key=filename)
        if response['ETag'] == etag:
            return True
        else:
            print(f'ETag mismatch for file {filename}')
            return False
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            print(f'Error checking file {filename} in S3: {e}')
            return False

def download_file(url):
    response = requests.get(url)

    if response.status_code == 403:
        print(f'403 Forbidden error for {url}')
        raise Exception(f'403 Forbidden error for {url} - Implement BLS data access policies')
    
    # Retry logic
    retries = 0
    while response.status_code != 200 and retries < MAX_RETRIES:
        print(f'Retrying {url} in {RETRY_DELAY} seconds')
        time.sleep(RETRY_DELAY) # wait before retrying
        response = requests.get(url)
        retries += 1

    if response.status_code != 200:
        print(f'Error downloading file {url}')
        raise Exception(f'Error downloading file {url}')
    
    etag = hashlib.md5(response.content).hexdigest()
    filename = url.split('/')[-1]

    with open(DATA_DIR + filename, 'wb') as f:
        f.write(response.content)
    
    return filename, etag
    

def upload_to_s3(filename, etag):
    if not file_exists_in_s3(filename, etag):
        try:
            s3.upload_file(DATA_DIR + filename, BUCKET_NAME, filename)
        except ClientError as e:
            print(f'Error uploading file {filename} to S3: {e}')
            return False
    

def sync_files():
    file_list = [] # list of files in the source URL

    for filename in file_list:
        try: 
            url = URL + filename
            filename, etag = download_file(url)
            upload_to_s3(filename, etag)
            print(f'Uploaded {filename} to S3')
        except Exception as e:
            print(f'Error processing file {filename}: {e}')
            continue
    
if __name__ == '__main__':
    sync_files()