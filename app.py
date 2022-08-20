#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_unzip_lambda.cdk_unzip_lambda_stack import CdkUnzipLambdaStack


app = cdk.App()
CdkUnzipLambdaStack(app, "cdk-unzip-lambda")

app.synth()
