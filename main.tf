provider "aws" {
    region = "your-region"
}

# Data fetch script (not managed by Terraform)
# The script fetches API data and converts Import

# S3 Bucket
resource "aws_s3_bucket" "data_bucket" {
    bucket = "data-bucket-name"
}

# S3 Bucket Notification for SQS Queue
resource "aws_s3_bucket_notification" "sqs_notification" {
    bucket = aws_s3_bucket.data_bucket.id

    queue {
        queue_arn = aws_sqs_queue.data_queue.arn
        events = ["s3:ObjectCreated:*"]
        filter_suffix = ".json" # Filter only JSON files
    }
}

# SQS Queue
resource "aws_sqs_queue" "data_queue" {
    name = "data-queue-name"
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
    name = "lambda-role-name"
    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
                Effect = "Allow",
                Principal = {
                    Service = "lambda.amazonaws.com"
                },
                Action = "sts:AssumeRole"
            }
        ]
    })
}

# Lambda Function
resource "aws_lambda_function" "analysis_function" {
    function_name = "analysis-function-name"
    handler = "index.handler" # handler function name
    runtime = "python3.8" # Adjust as necessary (e.g., python3.8, nodejs12.x, etc.)
    role = aws_iam_role.lambda_role.arn
    timeout = 10
    memory_size = 128

    environment {
        variables = {
            QUEUE_URL = aws_sqs_queue.data_queue.id
            S3_BUCKET_NAME = aws_s3_bucket.data_bucket.bucket
        }
    }

    filename = "lambda_function.zip" # Lambda function code store in zip file
    source_code_hash = filebase64sha256("lambda_function.zip")
}

# Event Source Mapping (triggers Lambda function from SQS)
resource "aws_lambda_event_source_mapping" "sqs_trigger" {
    event_source_arn = aws_sqs_queue.data_queue.arn
    function_name = aws_lambda_function.analysis_function.arn
    batch_size = 1
    starting_position = "TRIM_HORIZON"
}

# CloudWatch Event Rule (for daily schedule)
resource "aws_cloudwatch_event_rule" "daily_schedule" {
    name = "daily-schedule-name"
    schedule_expression = "cron(0 0 * * ? *)" # Run daily at midnight
}

# CloudWatch Event Target (triggerx Lambda function based on rule)
resource "aws_cloudwatch_event_target" "lambda_target" {
    rule = aws_cloudwatch_event_rule.daily_schedule.name
    target_id = "analysis-function-target" # Replace with your lambda target name
    arn = aws_lambda_function.analysis_function.arn
}