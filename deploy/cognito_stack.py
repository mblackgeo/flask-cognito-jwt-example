from aws_cdk import Stack
from aws_cdk import aws_cognito as cognito
from constructs import Construct

from .config import Conf


class CognitoStack(Stack):
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
        )

        # Add a custom domain for the hosted UI
        if Conf.AWS_COGNITO_SUBDOMAIN:
            self.user_pool.add_domain(
                f"{construct_id}-user-pool-domain",
                cognito_domain=cognito.CognitoDomainOptions(
                    domain_prefix=Conf.AWS_COGNITO_SUBDOMAIN
                ),
            )

        # Use systems manager parameter store to export the variables needed
        # for import in the lambda environment
        # TODO
