from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as _iam,
    aws_s3 as s3,
    aws_s3_notifications as s3_notify,
    RemovalPolicy,
    CfnOutput,
    Stack, Duration,

)
from constructs import Construct


class CdkUnzipLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        SOURCE_BUCKET_NAME = f'{Stack.of(self).account}-source-bucket'
        DESTINATION_BUCKET_NAME = f'{Stack.of(self).account}-destination-bucket'

        source_bucket = s3.Bucket.from_bucket_name(self, "SourceBucket", bucket_name=SOURCE_BUCKET_NAME)
        if source_bucket is None:
            source_bucket = s3.Bucket(self, "SourceBucket", bucket_name=SOURCE_BUCKET_NAME,
                                      removal_policy=RemovalPolicy.RETAIN)

        destination_bucket = s3.Bucket.from_bucket_name(self, "DestinationBucket", bucket_name=DESTINATION_BUCKET_NAME)
        if destination_bucket is None:
            destination_bucket = s3.Bucket(self, "DestinationBucket", bucket_name=DESTINATION_BUCKET_NAME,
                                           removal_policy=RemovalPolicy.RETAIN)

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
        custome_layer = _lambda.LayerVersion(self, 'UnzipFileFromS3Bucket_layer',
                                             code=_lambda.AssetCode("layer/"),
                                             description='Common helper utility',
                                             compatible_runtimes=[_lambda.Runtime.PYTHON_3_6,
                                                                  _lambda.Runtime.PYTHON_3_7,
                                                                  _lambda.Runtime.PYTHON_3_8,
                                                                  _lambda.Runtime.PYTHON_3_9, ],
                                             removal_policy=RemovalPolicy.DESTROY
                                             )
        powertools_layer = _lambda.LayerVersion.from_layer_version_arn(
            self,
            id="lambda-powertools",
            layer_version_arn=f"arn:aws:lambda:{self.region}:017000801446:layer:AWSLambdaPowertoolsPython:29"
        )

        # create lambda function
        lambda_unzip_s3 = _lambda.Function(
            self,
            'UnzipFileFromS3Bucket',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda"),
            memory_size=256,
            description='Lambda function to unzip a file from an S3 bucket. Lambda is triggered by S3 event.',
            handler="unzip_file_from_s3.handler",
            role=lambda_role,
            timeout=Duration.seconds(300),
            insights_version=_lambda.LambdaInsightsVersion.from_insight_version_arn(
                "arn:aws:lambda:us-west-1:580247275435:layer:LambdaInsightsExtension:14"),
            tracing=_lambda.Tracing.ACTIVE,
            layers=[powertools_layer, custome_layer],
            environment={
                'DESTINATION_BUCKET': DESTINATION_BUCKET_NAME,
                'POWERTOOLS_SERVICE_NAME': 'UnzipFileFromS3Bucket',
                'LOG_LEVEL': 'DEBUG'
            }
        )

        # Adding grants on s3 for the lambda
        source_bucket.grant_read(lambda_unzip_s3)
        destination_bucket.grant_write(lambda_unzip_s3)

        # Create trigger for Lambda function using suffix
        notification = s3_notify.LambdaDestination(lambda_unzip_s3)
        notification.bind(self, source_bucket)
        # Add Create Event only for .zip files
        source_bucket.add_object_created_notification(
            notification, s3.NotificationKeyFilter(suffix='.zip'))

        # Output of created resource
        CfnOutput(scope=self, id='cdk-output-lambda',
                  value=lambda_unzip_s3.function_name)
        CfnOutput(scope=self, id='source_bucket',
                  value=source_bucket.bucket_name)
        CfnOutput(scope=self, id='destination_bucket',
                  value=destination_bucket.bucket_name)
