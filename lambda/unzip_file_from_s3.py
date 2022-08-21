#!/usr/bin/env python3
import os
from io import BytesIO
from typing import Dict

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import S3Event
from aws_lambda_powertools.utilities.typing import LambdaContext

import boto3
from stream_unzip import stream_unzip

logger = Logger()

def unzip_and_upload_files(file_to_unzip: str, source_bucket_name: str, destination_bucket_name: str):
    """Main function for :
    1 - stream read the file_to_unzip based on S3 event (the lambda is triggered),
    2 - extract each file (saved on ephemeral storage) from within the zipfile using stream_unzip lib
    3 - finaly save the extracted file content in the destination bucket
    """

    # Instantiate the readable Body of the file tp unzip
    logger.info(f"## Opening file {file_to_unzip} from s3://{source_bucket_name}")

    s3 = boto3.resource('s3')
    s3_obj = s3.Object(source_bucket_name, file_to_unzip)
    body = s3_obj.get()['Body']

    # Read the content of the zipped file with stream_unzip
    for file_name, file_size, file_chunks in stream_unzip(body):
        # Unzipping file with a content only
        if file_size > 0:

            # filename is composed with subfolder where it is stored
            # files are also flatten in the destination bucket
            filename = str(file_name.decode('utf-8')).replace("/", "-")

            # Writing localy the file
            logger.debug(f"## Buffer {filename} content")
            buffer = BytesIO(bytes())
            for chunk in file_chunks:
                buffer.write(chunk)
            buffer.seek(0) # Important ! Reach the beginning of the buffer

            # Put the buffer as a file into the bucket
            destination_bucket = s3.Bucket(destination_bucket_name)
            destination_bucket.upload_fileobj(buffer, filename)

            logger.info(f"## Unzipped file '{filename}' is now saved in bucket {destination_bucket_name}")

@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: S3Event, context: LambdaContext) -> dict[str, int]:
    """Handler function for the lambda"""

    # Globals
    try:
        destination_bucket = os.environ["DESTINATION_BUCKET"]
    except:
        destination_bucket = "124571346663-destination-bucket"

    # Event parameters are stored
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    file_to_unzip = event['Records'][0]['s3']['object']['key']

    # This should the normal ending
    status_code = 200

    # Trying to unzip the file (check the function doc)
    try:
        unzip_and_upload_files(file_to_unzip, source_bucket, destination_bucket)
    except Exception as e:
        logger.exception(e)
        status_code = 500

    # Return a status code (for Step Function Handling for instance)
    return {
        'statusCode': status_code
    }
