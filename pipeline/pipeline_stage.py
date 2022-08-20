from constructs import Construct
from aws_cdk import (
    Stage
)
from cdk_unzip_lambda.cdk_unzip_lambda_stack import CdkUnzipLambdaStack

class WorkshopPipelineStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = CdkUnzipLambdaStack(self, 'UnzipLambdaStack')
