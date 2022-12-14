# Welcome to your CDK Python project!

You should explore the contents of this project. It demonstrates a CDK app with an instance of a
stack (`cdk_unzip_lambda_stack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project. The initialization process also creates
a virtualenv within this project, stored under the .venv directory. To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

Install dependencies for lambda layer

> The layer is mandatory for the installation of all python dependencies. The target platform is lambda AmazonLinuxv2 (
> linux_x86_64)
> We also use the
> library [AWS Lambda powertools for python](https://awslabs.github.io/aws-lambda-powertools-python/latest) for logging
> and other usefull decorators or X-Ray interactions. Powertools has its own public repository used for the lambda layer.

```
$ rm -rf layer && pip install -r requirements-layer.txt --target layer/python --upgrade --only-binary ":all:" --platform linux_x86_64 --implementation cp
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

* `cdk ls`          list all stacks in the app
* `cdk synth`       emits the synthesized CloudFormation template
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk docs`        open CDK documentation

Enjoy!

## Verify S3 contents

```
$ aws s3 ls s3://764612093004-destination-bucket --recursive --human-readable  --summarize
```


## Intersting considerations

### Lambda layers based on Docker images

In order to avoir local pip install for the layer, another approach should be to use docker images and build the docker
image on AWS.
Need to check [this article](https://aws.amazon.com/blogs/devops/using-aws-codepipeline-for-deploying-container-images-to-aws-lambda-functions/)
