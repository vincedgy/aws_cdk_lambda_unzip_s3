#!/usr/bin/env python3

import aws_cdk as cdk

app = cdk.App()

#from cdk_unzip_lambda.cdk_unzip_lambda_stack import CdkUnzipLambdaStack
#CdkUnzipLambdaStack(app, "CdkUnzipLambdaStack")

from pipeline.pipeline_stack import WorkshopPipelineStack
WorkshopPipelineStack(app, "WorkshopPipelineStack")

app.synth()
