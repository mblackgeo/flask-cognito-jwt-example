import aws_cdk as cdk
from aws_cdk import aws_apigatewayv2_alpha as apigw
from aws_cdk import aws_apigatewayv2_integrations_alpha as apigw_integrations
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from aws_cdk import aws_ssm as ssm
from constructs import Construct

from stacks.config import cfg


class ApiStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Optional Route 53 setup domain and certifcates
        default_domain_mapping = None
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
            domain_name = apigw.DomainName(
                scope=self,
                id=f"{construct_id}-domain-name",
                certificate=cert,
                domain_name=api_domain,
            )

            # Register the A record for the api if required
            route53.ARecord(
                scope=self,
                id=f"{construct_id}-alias-record",
                zone=zone,
                record_name=api_domain,
                target=route53.RecordTarget.from_alias(
                    targets.ApiGatewayv2DomainProperties(
                        regional_domain_name=domain_name.regional_domain_name,
                        regional_hosted_zone_id=domain_name.regional_hosted_zone_id,
                    )
                ),
            )

            default_domain_mapping = apigw.DomainMappingOptions(domain_name=domain_name)

        # Register and build an Lambda docker image
        # This picks up on Dockerfile in the parent folder
        fn = _lambda.DockerImageFunction(
            self,
            f"{construct_id}-lambda-handler",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="..", file="Dockerfile"
            ),
            timeout=cdk.Duration.seconds(15),
            memory_size=128,
        )

        # Add proxy integration for all routes
        self.http_api = apigw.HttpApi(
            scope=self,
            id=f"{construct_id}-endpoint",
            default_domain_mapping=default_domain_mapping,
            default_integration=apigw_integrations.HttpLambdaIntegration(
                id=f"{construct_id}-lambda-default-integration", handler=fn
            ),
        )

        self.http_api.add_routes(
            path="/",
            methods=[apigw.HttpMethod.ANY],
            integration=apigw_integrations.HttpLambdaIntegration(
                id=f"{construct_id}-lambda-any-integration", handler=fn
            ),
        )

        # Export the URL and Lambda ARN to SSM for other stacks to import
        ssm.StringParameter(
            self,
            f"{construct_id}-ssm-lambda-arn",
            parameter_name=f"/{cfg.NAMESPACE}/lambda-arn",
            string_value=fn.function_arn,
            description="Lambda function ARN",
        )

        ssm.StringParameter(
            self,
            f"{construct_id}-ssm-http-url",
            parameter_name=f"/{cfg.NAMESPACE}/apigw-url",
            string_value=self.http_api.url,
            description="API Gateway URL",
        )
