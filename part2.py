#### Part 2: APIs
"""
#TODO: WIP
1. Create a script that will fetch data from [this API](https://datausa.io/api/data?drilldowns=Nation&measures=Population).
   You can read the documentation [here](https://datausa.io/about/api/)
2. Save the result of this API call as a JSON file in S3.
"""
import boto3
import json
import requests

# Fetch data from the API
response = requests.get('https://datausa.io/api/data?drilldowns=Nation&measures=Population')
data = response.json()

# Save the data to S3
s3 = boto3.client('s3')
s3.put_object(
   Bucket='my-bucket', 
   Key='population.json', 
   Body=json.dumps(data)
)