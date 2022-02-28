import aws_cdk as cdk
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_ssm as ssm
from aws_cdk import custom_resources as cr
from constructs import Construct

from stacks.config import cfg


class LambdaEnvStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.namespace = cfg.NAMESPACE

        # Grab the Lambda function
        fn = _lambda.Function.from_function_arn(
            scope=self,
            id=f"{construct_id}-lambda-fn",
            function_arn=self.from_ssm("lambda-arn"),
        )

        # Get the environment variables from SSM
        # Only possible *after* both API gateway and Cognito have been deployed
        # Other option would be to have the container resolve these values at
        # runtime using the AWS SDK (boto3)
        environment = {
            "FLASK_APP": cfg.NAMESPACE,
            "FLASK_ENV": cfg.ENV,
            "FLASK_SITE_URL": self.from_ssm("apigw-url"),
            "AWS_COGNITO_DOMAIN": self.from_ssm("cognito-user-pool-url"),
            "AWS_COGNITO_USER_POOL_ID": self.from_ssm("cognito-user-pool-id"),
            "AWS_COGNITO_USER_POOL_CLIENT_ID": self.from_ssm("cognito-client-id"),
            "AWS_COGNITO_USER_POOL_CLIENT_SECRET": self.from_ssm(
                "cognito-client-secret"
            ),
        }

        # Use a custom resource to update the environment variables of the Lambda
        cr.AwsCustomResource(
            self,
            f"{construct_id}-custom-resource-update-env",
            resource_type="Custom::DescribeCognitoUserPoolClient",
            on_update=cr.AwsSdkCall(
                region=cfg.AWS_REGION,
                service="Lambda",
                action="updateFunctionConfiguration",
                parameters={
                    "FunctionName": fn.function_arn,
                    "Environment": {
                        "Variables": environment,
                    },
                },
                physical_resource_id=cr.PhysicalResourceId.of(fn.function_arn),
            ),
            policy=cr.AwsCustomResourcePolicy.from_sdk_calls(
                resources=[fn.function_arn]
            ),
        )

    def from_ssm(self, key: str) -> str:
        return ssm.StringParameter.value_for_string_parameter(
            scope=self, parameter_name=f"/{self.namespace}/{key}"
        )
