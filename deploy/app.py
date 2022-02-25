import aws_cdk as cdk

from stacks.api_stack import ApiStack
from stacks.cognito_stack import CognitoStack
from stacks.config import cfg

app = cdk.App()
cdk_env = cdk.Environment(region=cfg.AWS_REGION, account=cfg.AWS_ACCOUNT)

cognito = CognitoStack(app, "cognito", env=cdk_env)
api_gw = ApiStack(app, "api", env=cdk_env)
api_gw.add_dependency(cognito)

app.synth()
