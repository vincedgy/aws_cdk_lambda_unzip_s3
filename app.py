#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_unzip_lambda.cdk_unzip_lambda_stack import CdkUnzipLambdaStack

#from pipeline.pipeline_stack import WorkshopPipelineStack

#app = cdk.App()
#WorkshopPipelineStack(app, "CdkUnzipLambdaPipelineStack")

app = cdk.App()
CdkUnzipLambdaStack(app, "CdkUnzipLambdaStack")

app.synth()
