from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as _iam,
    CfnOutput,
    Stack,

)
from constructs import Construct


class CdkUnzipLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create role for your Lambda function
        lambda_role = _iam.Role(scope=self, id='cdk-lambda-role',
                                assumed_by=_iam.ServicePrincipal('lambda.amazonaws.com'),
                                role_name='cdk-lambda-UnzipFileFromS3Bucket-role',
                                managed_policies=[
                                    _iam.ManagedPolicy.from_aws_managed_policy_name(
                                        'service-role/AWSLambdaVPCAccessExecutionRole'),
                                    _iam.ManagedPolicy.from_aws_managed_policy_name(
                                        'service-role/AWSLambdaBasicExecutionRole')
                                ])

        # create layer
        # layer = _lambda.LayerVersion(self, 'UnzipFileFromS3Bucket_layer',
        #                              code=_lambda.AssetCode("layer/"),
        #                              description='Common helper utility',
        #                              compatible_runtimes=[_lambda.Runtime.PYTHON_3_6, _lambda.Runtime.PYTHON_3_7,
        #                                                   _lambda.Runtime.PYTHON_3_8, _lambda.Runtime.PYTHON_3_9, ],
        #                              removal_policy=RemovalPolicy.DESTROY
        #                              )
        # create lambda function
        cdk_lambda = _lambda.Function(
            self,
            'UnzipFileFromS3Bucket',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda"),
            description='Lambda function to unzip a file from an S3 bucket. Lambda is triggered by S3 event.',
            handler="unzip_file_from_s3.handler",
            role=lambda_role,
            # layers=[layer],
            environment={
                'DESTINATION_BUCKET': f'{Stack.of(self).account}-destination-bucket'
            }
        )

        # Output of created resource
        CfnOutput(scope=self, id='cdk-output-lambda',
                  value=cdk_lambda.function_name)
        # CfnOutput(scope=self, id='cdk-output-lambda-layer',
        #           value=layer.layer_version_arn)
