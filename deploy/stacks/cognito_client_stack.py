from os.path import join

import aws_cdk as cdk
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_ssm as ssm
from aws_cdk import custom_resources as cr
from constructs import Construct

from stacks.config import cfg


class CognitoClientStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.user_pool = cognito.UserPool.from_user_pool_id(
            scope=self,
            id=f"{construct_id}-cognito-user-pool",
            user_pool_id=ssm.StringParameter.value_for_string_parameter(
                self, f"/{cfg.NAMESPACE}/cognito-user-pool-id"
            ),
        )

        # Set callback URLs for the client
        apigw_url = join(
            ssm.StringParameter.value_for_string_parameter(
                self, f"/{cfg.NAMESPACE}/apigw-url"
            ),
            "postlogin",
        )
        callback_urls = ["http://localhost:5000/postlogin", apigw_url]

        # Add a client and generate client ID and secret
        self.client = self.user_pool.add_client(
            f"{construct_id}-client",
            generate_secret=True,
            user_pool_client_name=f"{cfg.NAMESPACE}-{cfg.ENV}",
            auth_flows=cognito.AuthFlow(user_password=True, user_srp=True),
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(authorization_code_grant=True),
                scopes=[cognito.OAuthScope.OPENID],
                callback_urls=callback_urls,
            ),
        )
        self.export_client_secret_to_ssm(construct_id)

        ssm.StringParameter(
            self,
            f"{construct_id}-ssm-client-id",
            parameter_name=f"/{cfg.NAMESPACE}/cognito-client-id",
            string_value=self.client.user_pool_client_id,
            description="Cognito client ID",
        )

    def export_client_secret_to_ssm(self, construct_id: str):
        # The generated client secret is not outputted by CloudFormation
        # Here we make a custom resource that will perform an SDK call to get
        # the generated client secret and store it in SSM. See:
        # https://github.com/aws/aws-cdk/issues/7225#issuecomment-610299259
        describe_client = cr.AwsCustomResource(
            self,
            f"{construct_id}-describe-pool-agent",
            resource_type="Custom::DescribeCognitoUserPoolClient",
            on_update=cr.AwsSdkCall(
                region=cfg.AWS_REGION,
                service="CognitoIdentityServiceProvider",
                action="describeUserPoolClient",
                parameters={
                    "UserPoolId": self.user_pool.user_pool_id,
                    "ClientId": self.client.user_pool_client_id,
                },
                physical_resource_id=cr.PhysicalResourceId.of(
                    self.client.user_pool_client_id
                ),
            ),
            # TODO restrict this resource policy
            policy=cr.AwsCustomResourcePolicy.from_sdk_calls(
                resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE
            ),
        )

        client_secret = describe_client.get_response_field(
            "UserPoolClient.ClientSecret"
        )

        ssm.StringParameter(
            self,
            f"{construct_id}-ssm-client-secret",
            parameter_name=f"/{cfg.NAMESPACE}/cognito-client-secret",
            string_value=client_secret,
            description="Cognito client secret",
        )
