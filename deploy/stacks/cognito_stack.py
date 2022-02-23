import aws_cdk as core
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_ssm as ssm
from aws_cdk import custom_resources as cr
from constructs import Construct

from stacks.config import cfg


class CognitoStack(core.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a user pool and get Cognito to send a verification email to the
        # user to confirm their account
        self.user_pool = cognito.UserPool(
            self,
            f"{construct_id}-user-pool",
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(username=True, email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(mutable=True, required=True),
            ),
            user_verification=cognito.UserVerificationConfig(
                email_subject="Verify your account",
                email_style=cognito.VerificationEmailStyle.LINK,
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        # Add a client and generate client ID and secret
        self.client = self.user_pool.add_client(
            f"{construct_id}-client",
            generate_secret=True,
            user_pool_client_name=f"{cfg.NAMESPACE}-{cfg.ENV}",
            auth_flows=cognito.AuthFlow(user_password=True, user_srp=True),
        )
        self.export_client_secret_to_ssm(construct_id)

        # Add a custom domain for the hosted UI
        if cfg.AWS_COGNITO_SUBDOMAIN and cfg.AWS_DOMAIN_NAME:
            root_domain = cfg.AWS_DOMAIN_NAME
            cognito_domain = f"{cfg.AWS_COGNITO_SUBDOMAIN}.{root_domain}"

            zone = route53.HostedZone.from_lookup(
                self, f"{construct_id}-hosted-zone", domain_name=root_domain
            )

            cert = acm.DnsValidatedCertificate(
                self,
                f"{construct_id}-certificate",
                hosted_zone=zone,
                region="us-east-1",  # required for Cognito to be in us-east-1
                domain_name=cognito_domain,
                cleanup_route53_records=True,
            )

            self.user_pool.add_domain(
                f"{construct_id}-domain",
                custom_domain=cognito.CustomDomainOptions(
                    domain_name=cognito_domain, certificate=cert
                ),
            )

        # Use systems manager parameter store to export the variables needed
        # for import in the lambda environment
        ssm.StringParameter(
            self,
            f"{construct_id}-ssm-user-pool-id",
            parameter_name=f"/{cfg.NAMESPACE}/cognito-user-pool-id",
            string_value=self.user_pool.user_pool_id,
            description="Cognito user pool ID",
        )

        ssm.StringParameter(
            self,
            f"{construct_id}-ssm-user-pool-url",
            parameter_name=f"/{cfg.NAMESPACE}/cognito-user-pool-url",
            string_value=self.user_pool.user_pool_provider_url,
            description="Cognito user pool URL",
        )

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
        # generated client secret and store it in SSM. See:
        # https://github.com/aws/aws-cdk/issues/7225#issuecomment-610299259
        describe_client = cr.AwsCustomResource(
            self,
            f"{construct_id}-describe-pool-agent",
            resource_type="Custom::DescribeCognitoUserPoolClient",
            on_create=cr.AwsSdkCall(
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

        # TODO secure string?
        ssm.StringParameter(
            self,
            f"{construct_id}-ssm-client-secret",
            parameter_name=f"/{cfg.NAMESPACE}/cognito-client-secret",
            string_value=client_secret,
            description="Cognito client secret",
        )
