import aws_cdk as core
from aws_cdk import aws_apigatewayv2_alpha as apigw
from aws_cdk import aws_apigatewayv2_integrations_alpha as apigw_integrations
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_ssm as ssm
from constructs import Construct

from stacks.config import cfg


class LambdaStack(core.Stack):
    def __init__(
        self, scope: Construct, construct_id: str, http_api: apigw.HttpApi, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        environment = {
            "FLASK_APP": cfg.NAMESPACE,
            "FLASK_ENV": cfg.ENV,
            "AWS_COGNITO_DOMAIN": self.from_ssm(
                f"/{cfg.NAMESPACE}/cognito-user-pool-url"
            ),
            "AWS_COGNITO_USER_POOL_ID": self.from_ssm(
                f"/{cfg.NAMESPACE}/cognito-user-pool-id"
            ),
            "AWS_COGNITO_USER_POOL_CLIENT_ID": self.from_ssm(
                f"/{cfg.NAMESPACE}/cognito-client-id"
            ),
            "AWS_COGNITO_USER_POOL_CLIENT_SECRET": self.from_ssm(
                f"/{cfg.NAMESPACE}/cognito-client-secret"
            ),
        }

        # Register and build an Lambda docker image
        # This picks up on Dockerfile in the parent folder
        fn = _lambda.DockerImageFunction(
            self,
            f"{construct_id}-lambda-handler",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="..", file="Dockerfile"
            ),
            timeout=core.Duration.seconds(15),
            environment=environment,
            memory_size=512,
        )

        # Add proxy integration for all routes
        http_api.add_routes(
            path="/",
            methods=[apigw.HttpMethod.ANY],
            integration=apigw_integrations.HttpLambdaIntegration(
                id=f"{construct_id}-lambda-any-integration", handler=fn
            ),
        )

        fn.add_environment(key="FLASK_SITE_URL", value=http_api.url)

    def from_ssm(self, key: str) -> str:
        return ssm.StringParameter.value_for_string_parameter(self, key)
