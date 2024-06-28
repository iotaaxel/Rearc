
#### Part 1: AWS S3 & Sourcing Datasets
"""
1. Republish [this open dataset](https://download.bls.gov/pub/time.series/pr/) in Amazon S3 and share with us a link.
    - You may run into 403 Forbidden errors as you test accessing this data. There is a way to comply with the BLS data access policies and re-gain access to fetch this data programatically - we have included some hints as to how to do this at the bottom of this README in the Q/A section.
2. Script this process so the files in the S3 bucket are kept in sync with the source when data on the website is updated, added, or deleted.
    - Don't rely on hard coded names - the script should be able to handle added or removed files.
    - Ensure the script doesn't upload the same file more than once.
"""

import requests
import boto3
import time


def fetch_and_republish(url, bucket_name, object_key):
    """
    Fetches a file from a URL and republishes it to an S3 bucket.
    """
    # Fetch the file
    response = requests.get(url)
    # Save the file to S3
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=response.content)
    return response.status_code

if __name__ == '__main__':
    # URL of the file to fetch
    url = 'https://download.bls.gov/pub/time.series/pr/pr.data.0.Current'
    # Name of the S3 bucket
    bucket_name = 'my-bucket'
    # Key of the object in the S3 bucket
    object_key = 'pr.data.0.Current'
    # Fetch and republish the file
    status_code = fetch_and_republish(url, bucket_name, object_key)
    print(f'Status code: {status_code}')

    # Wait for 5 seconds
    time.sleep(5)
    # Fetch and republish the file again
    status_code = fetch_and_republish(url, bucket_name, object_key)
    print(f'Status code: {status_code}')