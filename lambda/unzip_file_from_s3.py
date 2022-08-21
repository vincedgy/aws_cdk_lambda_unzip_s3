#!/usr/bin/env python3
import os
import logging
#from aws_lambda_powertools import Logger as logger
import boto3
from stream_unzip import stream_unzip

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Globals
try:
    destination_bucket = os.environ["DESTINATION_BUCKET"]
except:
    destination_bucket = "124571346663-destination-bucket"

s3 = boto3.resource('s3')

def unzip_and_upload_files(file_to_unzip: str, source_bucket: str, destination_bucket: str):
    """Main function for :
    1 - stream read the file_to_unzip based on S3 event (the lambda is triggered),
    2 - extract each file (saved on ephemeral storage) from within the zipfile using stream_unzip lib
    3 - finaly savec the extracted file in the destination bucket

    TODO : Stream put the unzip file and not store it on the ephemeral lambda local storage
    """

    try:
        # Instantiate the readable Body of the file tp unzip
        logger.info(f"## Opening file {file_to_unzip} from s3://{source_bucket}")
        s3_obj = s3.Object(source_bucket, file_to_unzip)
        body = s3_obj.get()['Body']

        # Read the content of the zipped file with stream_unzip
        for file_name, file_size, file_chunks in stream_unzip(body):
            # Unzipping file with a content only
            if file_size > 0:

                # filename is composed with subfolder where it is stored
                # files are also flatten in the destination bucket
                filename = str(file_name.decode('utf-8')).replace("/", "-")

                # writing localy the file
                # TODO : consider put the file by stream and not localy
                logger.info(f"## Writing {filename} localy")
                with open(filename, "ab") as written_file:
                    for chunk in file_chunks:
                        written_file.write(chunk)

                # put the file in the bucket
                s3.Object(destination_bucket, filename).upload_file(filename)
                logger.info(f"## Unzipped file {filename} is now written on bucket {destination_bucket}")

                # deleting the file localy for the sake of the local ephemeral storage
                os.remove(filename)
                logger.info(f"## {filename} is now deleted localy")

    except Exception as e:
        logger.exception(e)
        raise f'Error: Unable to unzip & upload the file {file_to_unzip} from {source_bucket}'


def handler(event, context):
    """Handler function for the lambda"""

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
    # TODO : maybe something to re check here
    return {
        'statusCode': status_code
    }


# Dynamicaly install steam_unzip at runtime
if __name__ == '__main__':

    handler(context={}, event={
        "Records": [
            {
                "eventVersion": "2.0",
                "eventSource": "aws:s3",
                "awsRegion": "us-east-1",
                "eventTime": "1970-01-01T00:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {
                    "principalId": "EXAMPLE"
                },
                "requestParameters": {
                    "sourceIPAddress": "127.0.0.1"
                },
                "responseElements": {
                    "x-amz-request-id": "EXAMPLE123456789",
                    "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "testConfigRule",
                    "bucket": {
                        "name": "124571346663-source-bucket",
                        "ownerIdentity": {
                            "principalId": "EXAMPLE"
                        },
                        "arn": "arn:aws:s3:::example-bucket"
                    },
                    "object": {
                        "key": "test.zip",
                        "size": 1024,
                        "eTag": "0123456789abcdef0123456789abcdef",
                        "sequencer": "0A1B2C3D4E5F678901"
                    }
                }
            }
        ]
    })
