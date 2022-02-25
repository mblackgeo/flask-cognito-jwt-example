import aws_cdk as cdk

from stacks.api_stack import ApiStack
from stacks.cognito_client_stack import CognitoClientStack
from stacks.cognito_stack import CognitoStack
from stacks.config import cfg
from stacks.lambda_stack import LambdaStack

app = cdk.App()
cdk_env = cdk.Environment(region=cfg.AWS_REGION, account=cfg.AWS_ACCOUNT)

# Create the Cognito User Pool and API Gateway proxy to Lambda
cognito = CognitoStack(app, "cognito", env=cdk_env)
api = ApiStack(app, "api", env=cdk_env)
api.add_dependency(cognito)

# Register a client to the Cognito user pool, after both are already setup
# This is so we can resolve the URL of the API gateway after it has been
# created
client = CognitoClientStack(app, "client", user_pool=cognito.user_pool, env=cdk_env)
client.add_dependency(cognito)
client.add_dependency(api)

# Register the lambda function to the API gateway
lambda_fn = LambdaStack(app, "lambda", http_api=api.http_api)

app.synth()
