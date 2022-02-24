import aws_cdk as core
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from aws_cdk import aws_ssm as ssm
from constructs import Construct

from stacks.config import cfg


class LambdaApiStack(core.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Setup the environment variables for Lambda
        environment = {
            "FLASK_APP": cfg.NAMESPACE,
            "FLASK_ENV": cfg.ENV,
            "FLASK_SITE_URL": self.from_ssm(f"/{cfg.NAMESPACE}/api-gateway-url"),
            "AWS_REGION": cfg.AWS_REGION,
            "AWS_DEFAULT_REGION": cfg.AWS_REGION,
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
        )

        # Optional Route 53 setup domain and certifcates
        domain_opts = None
        if cfg.AWS_DOMAIN_NAME and cfg.AWS_API_SUBDOMAIN:
            root_domain = cfg.AWS_DOMAIN_NAME
            api_domain = f"{cfg.AWS_API_SUBDOMAIN}.{root_domain}"

            # Get the HostedZone of the root domain
            zone = route53.HostedZone.from_lookup(
                self, f"{construct_id}-hosted-zone", domain_name=root_domain
            )

            # Create a certificate for the api subdomain
            cert = acm.Certificate(
                self,
                f"{construct_id}-certificate",
                domain_name=api_domain,
                validation=acm.CertificateValidation.from_dns(zone),
            )

            # Configure the api domain options for the rest api
            domain_opts = apigw.DomainNameOptions(
                certificate=cert, domain_name=api_domain
            )

        # Create a Lambda based rest API with optional domain name
        api = apigw.LambdaRestApi(
            self,
            f"{construct_id}-api-route",
            handler=fn,
            deploy_options=apigw.StageOptions(stage_name=cfg.ENV),
            domain_name=domain_opts,
        )

        # Register the A record for the api if required
        if domain_opts is not None:
            route53.ARecord(
                self,
                f"{construct_id}-A-record",
                record_name=api_domain,
                zone=zone,
                target=route53.RecordTarget.from_alias(targets.ApiGateway(api)),
            )

        # Export the API Gateway address to SSM
        ssm.StringParameter(
            self,
            f"{construct_id}-ssm-client-id",
            parameter_name=f"/{cfg.NAMESPACE}/api-gateway-url",
            string_value=api.url,
            description="API Gateway URL",
        )

    def from_ssm(self, key: str) -> str:
        return ssm.StringParameter.value_for_string_parameter(self, key)
