##############################################################################
# lambda/functions/example_function/handler.py
#
# Example Lambda function.
# Packaged as example_function.zip and uploaded to:
#   s3://de1-{env}-lambda-packages/functions/example_function.zip
# Referenced by the Lambda resource in de1-infrastructure.
##############################################################################

import json
import logging
import os
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")
PROJECT_NAME = os.environ.get("PROJECT_NAME", "de1")

s3_client = boto3.client("s3")


def lambda_handler(event, context):
    """
    Entry point for the Lambda function.
    Triggered by EventBridge, S3 events, or API Gateway depending on your use case.
    """
    logger.info(f"Lambda invoked | env={ENVIRONMENT} | event={json.dumps(event)}")

    try:
        result = process(event)
        logger.info(f"Processing complete: {result}")
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    except Exception as e:
        logger.error(f"Error during processing: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


def process(event):
    """
    Core business logic — replace this with your actual logic.
    """
    # Example: read a file from the data lake and return its size
    bucket = f"{PROJECT_NAME}-{ENVIRONMENT}-data-lake"
    key = event.get("key", "raw/")

    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=key)
    count = response.get("KeyCount", 0)

    return {
        "bucket": bucket,
        "prefix": key,
        "object_count": count,
        "environment": ENVIRONMENT,
    }
