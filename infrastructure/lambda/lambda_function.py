import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    client = boto3.client('glue')

    try:
        response = client.start_job_run(
            JobName='s3_csv_change_schema'
        )
        logger.info(f"Glue job started: {response['JobRunId']}")
        return {
            'statusCode': 200,
            'body': f"Glue job started: {response['JobRunId']}"
        }
    except client.exceptions.ConcurrentRunsExceededException as e:
        logger.error(f"Glue job already running: {e}")
        return {
            'statusCode': 429,
            'body': 'Glue job is already running'
        }
    except Exception as e:
        logger.error(f"Failed to start Glue job: {e}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }