#!/usr/bin/env python3

import aws_cdk as cdk

from pipeline.pipeline_stack import WorkshopPipelineStack

app = cdk.App()
WorkshopPipelineStack(app, "WorkshopPipelineStack")

# app = cdk.App()
# CdkUnzipLambdaStack(app, "cdk-unzip-lambda")

app.synth()
