import aws_cdk as cdk

from stacks.cognito_stack import CognitoStack
from stacks.config import cfg
from stacks.lambda_api_stack import LambdaApiStack

app = cdk.App()
cdk_env = cdk.Environment(region=cfg.AWS_REGION, account=cfg.AWS_ACCOUNT)

cognito = CognitoStack(app, "cognito", env=cdk_env)
lambda_api = LambdaApiStack(app, "lambda-api", env=cdk_env)
lambda_api.add_dependency(cognito)

app.synth()
