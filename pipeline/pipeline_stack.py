from constructs import Construct
from aws_cdk import (
    aws_codecommit as codecommit,
    pipelines as pipelines,
    Stack,
)
from pipeline.pipeline_stage import WorkshopPipelineStage


class WorkshopPipelineStack(Stack):
      
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creates a CodeCommit repository called 'WorkshopRepo'
        repo = codecommit.Repository(
            self, 'UnzipFileToS3Repo',
            repository_name="UnzipFileToS3Repo"
        )

        # Pipeline code will go here
        pipeline = pipelines.CodePipeline(
            self,
            "UnzipFileToS3Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                commands=[
                    "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                    # Instructs Codebuild to install required packages
                    # "pip install --upgrade pip",
                    "pip install -r requirements.txt",
                    "cdk synth",
                ]
            ),
        )

        deploy = WorkshopPipelineStage(self, "Deploy")
        deploy_stage = pipeline.add_stage(deploy)

        # deploy_stage.add_post(
        #   pipelines.ShellStep(
        #       "TestViewerEndpoint",
        #       env_from_cfn_outputs={
        #           "ENDPOINT_URL": deploy.hc_viewer_url
        #       },
        #       commands=["curl -Ssf $ENDPOINT_URL"],
        #   )
        # )
        # deploy_stage.add_post(
        #     pipelines.ShellStep(
        #         "TestAPIGatewayEndpoint",
        #         env_from_cfn_outputs={
        #             "ENDPOINT_URL":  deploy.hc_endpoint
        #         },
        #         commands=[
        #             "curl -Ssf $ENDPOINT_URL",
        #             "curl -Ssf $ENDPOINT_URL/hello",
        #             "curl -Ssf $ENDPOINT_URL/test",
        #         ],
        #     )
        # )
