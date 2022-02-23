import aws_cdk as cdk

from .cognito_stack import CognitoStack
from .config import Conf
from .lambda_api_stack import LambdaApiStack

app = cdk.App()
cdk_environment = cdk.Environment(region=Conf.AWS_REGION, account=Conf.AWS_ACCOUNT)

cognito = CognitoStack(app, "cognito")
lambda_api = LambdaApiStack(app, "lambda-api")
lambda_api.add_dependency(cognito)

app.synth()
