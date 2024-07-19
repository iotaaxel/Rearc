# AWS Practice

#### Part 1: AWS S3 & Sourcing Datasets
1. Republish [this open dataset](https://download.bls.gov/pub/time.series/pr/) in Amazon S3 and share with us a link.
    - You may run into 403 Forbidden errors as you test accessing this data. 
2. Script this process so the files in the S3 bucket are kept in sync with the source when data on the website is updated, added, or deleted.
    - Don't rely on hard coded names - the script should be able to handle added or removed files.
    - Ensure the script doesn't upload the same file more than once.

#### Part 2: APIs
1. Create a script that will fetch data from [this API](https://datausa.io/api/data?drilldowns=Nation&measures=Population).
   You can read the documentation [here](https://datausa.io/about/api/)

### Part 3: Relax

#### Part 4: Infrastructure as Code & Data Pipeline with AWS CDK
0. Using [AWS CloudFormation](https://aws.amazon.com/cloudformation/), [AWS CDK](https://aws.amazon.com/cdk/) or [Terraform](https://www.terraform.io/), create a data pipeline that will automate the steps above.
1. The deployment should include a Lambda function that executes
   Part 1 and Part 2 (you can combine both in 1 lambda function). The lambda function will be scheduled to run daily.
2. The deployment should include an SQS queue that will be populated every time the JSON file is written to S3. (Hint: [S3 - Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html))
3. For every message on the queue - execute a Lambda function that outputs the reports from Part 3

## Troubleshooting 

### Q. How do I get around the 403 error when I try to fetch BLS data?
<details>
<summary>Hint 1</summary>
  The BLS data access policies can be found here: https://www.bls.gov/bls/pss.htm
</details>
<details>
<summary>Hint 2</summary>
  The policy page says:

```BLS also reserves the right to block robots that do not contain information that can be used to contact the owner. Blocking may occur in real time.```

How could you add information to your programmatic access requests to let BLS contact you?
</details>
<details>
<summary>Hint 3</summary>
  Adding a <code>User-Agent</code> header to your request with contact information will comply with the BLS data policies and allow you to keep accessing their data programmatically.
</details>
