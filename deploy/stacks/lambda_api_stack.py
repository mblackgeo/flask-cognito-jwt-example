import aws_cdk as core
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from constructs import Construct

from stacks.config import cfg


class LambdaApiStack(core.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Stage configuration
        opts = apigw.StageOptions(stage_name=cfg.ENV)

        # Optional Route 53 setup domain and certifcates
        if cfg.AWS_DOMAIN_NAME:
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

        # Register and build an Lambda docker image
        # This picks up on Dockerfile in the parent folder
        fn = _lambda.DockerImageFunction(
            self,
            f"{construct_id}-lambda-handler",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="..", file="Dockerfile.aws"
            ),
            timeout=core.Duration.seconds(15),
            environment={
                "FLASK_APP": "webapp",
                "FLASK_ENV": cfg.ENV,
                "FLASK_JWT_SECRET_KEY": "",
                "FLASK_SITE_URL": "",
                "AWS_REGION": cfg.AWS_REGION,
                "AWS_DEFAULT_REGION": cfg.AWS_REGION,
                "AWS_COGNITO_DOMAIN": "",
                "AWS_COGNITO_USER_POOL_ID": "",
                "AWS_COGNITO_USER_POOL_CLIENT_ID": "",
                "AWS_COGNITO_USER_POOL_CLIENT_SECRET": "",
            },
        )

        # Create a Lambda based rest API with optional domain name
        api = apigw.LambdaRestApi(
            self,
            f"{construct_id}-api-route",
            handler=fn,
            deploy_options=opts,
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
