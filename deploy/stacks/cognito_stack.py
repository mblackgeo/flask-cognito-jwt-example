import aws_cdk as cdk
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_ssm as ssm
from constructs import Construct

from stacks.config import cfg


class CognitoStack(cdk.Stack):
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
            removal_policy=cdk.RemovalPolicy.DESTROY,  # TODO change for prod
        )

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

            domain = self.user_pool.add_domain(
                f"{construct_id}-domain",
                custom_domain=cognito.CustomDomainOptions(
                    domain_name=cognito_domain, certificate=cert
                ),
            )
        else:
            # Create domain prefix so there is a hosted UI
            domain = self.user_pool.add_domain(
                f"{construct_id}-prefix-domain",
                cognito_domain=cognito.CognitoDomainOptions(
                    domain_prefix=f"{cfg.NAMESPACE}-auth"
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
            string_value=domain.base_url(),
            description="Cognito user pool URL",
        )
