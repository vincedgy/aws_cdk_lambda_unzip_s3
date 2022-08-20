from aws_cdk import (
    Stack,
    assertions
)

from cdk_unzip_lambda.cdk_unzip_lambda_stack import CdkUnzipLambdaStack
import pytest

def test_lambda_has_env_vars():
    """Test whether the function has declared the two mandatory parameters"""
    stack = Stack()
    CdkUnzipLambdaStack(stack, "HitCounter")

    template = assertions.Template.from_stack(stack)
    envCapture = assertions.Capture()

    template.has_resource_properties("AWS::Lambda::Function", {
        "Handler": "unzip_file_from_s3.handler",
        "Environment": envCapture,
    })

    assert envCapture.as_object() == {
        "Variables": {
            "DESTINATION_BUCKET": {"Ref": "XXX"},
        },
    }
