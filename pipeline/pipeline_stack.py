from aws_cdk import (
    aws_codecommit as codecommit,
    pipelines as pipelines,
    Stack,
)
from constructs import Construct

from pipeline.pipeline_stage import UnzipLambdaToS3PipelineStage


class UnzipLambdaToS3PipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creates a CodeCommit repository called 'UnzipFileToS3Repo'
        repo = codecommit.Repository.from_repository_name(self, 'UnzipFileToS3Repo',
                                                          repository_name="UnzipFileToS3Repo")
        # repo = codecommit.Repository(
        #    self, 'UnzipFileToS3',
        ##    repository_name="UnzipFileToS3Repo"
        # )

        # Pipeline code will go here
        pipeline = pipelines.CodePipeline(self, "UnzipFileToS3Pipeline",
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
                                          )

                                          )

        deploy = UnzipLambdaToS3PipelineStage(self, "Deploy")
        pipeline.add_stage(deploy)
