from aws_cdk import (
    aws_lambda as _lambda,
    Stack,
)
from constructs import Construct


class CdkUnzipLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        _lambda.Function(
            self,
            'UnzipFileFromS3Bucket',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler="unzip_fil_from_s3.handler"
        )
