import aws_cdk as cdk

from stacks.api_stack import ApiStack
from stacks.cognito_client_stack import CognitoClientStack
from stacks.cognito_stack import CognitoStack
from stacks.config import cfg
from stacks.lambda_env_stack import LambdaEnvStack

app = cdk.App()
cdk_env = cdk.Environment(region=cfg.AWS_REGION, account=cfg.AWS_ACCOUNT)

# Create the API Gateway and User Pools up front. Later we add the client
# and register the Lambda target on the API
api = ApiStack(scope=app, construct_id="api", env=cdk_env)
cognito = CognitoStack(scope=app, construct_id="cognito", env=cdk_env)

# Register a client to the Cognito user pool, after both API and User Pool
# are already setup. This is so we can resolve the URL of the API gateway
# after it has been created and correctly register the post login URL on
# the user pool client
client = CognitoClientStack(
    scope=app,
    construct_id="cognito-client",
    env=cdk_env,
)
client.add_dependency(api)
client.add_dependency(cognito)

# Finally we can populate the Lambda function with the required environment
# variables from all the above stacks
# An alternative option here would be to resolve the parameters from SSM at runtime
# rather than at deployment time
lambda_env = LambdaEnvStack(
    scope=app,
    construct_id="lambda-env",
    env=cdk_env,
)
lambda_env.add_dependency(client)

app.synth()
