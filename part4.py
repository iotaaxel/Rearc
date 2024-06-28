"""
#TODO: WIP, see main.tf

0. Using [AWS CloudFormation](https://aws.amazon.com/cloudformation/), [AWS CDK](https://aws.amazon.com/cdk/) or [Terraform](https://www.terraform.io/), create a data pipeline that will automate the steps above.
1. The deployment should include a Lambda function that executes
   Part 1 and Part 2 (you can combine both in 1 lambda function). The lambda function will be scheduled to run daily.
2. The deployment should include an SQS queue that will be populated every time the JSON file is written to S3. (Hint: [S3 - Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html))
3. For every message on the queue - execute a Lambda function that outputs the reports from Part 3 (just logging the results of the queries would be enough. No .ipynb is required).
"""
import boto3
import json
import requests

def lambda_handler(event, context):
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

    