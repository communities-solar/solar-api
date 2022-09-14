#!/usr/bin/env python3
import aws_cdk as cdk

import os
import sys

# Get deployment environment from env variable or default to development
environment = os.getenv("ENVIRONMENT", "dev").lower()

DEPLOYMENT_VERSION = "v1"
DEPLOYMENT_ENVIRONMENT = environment
NAME_PREFIX = "{}-".format(DEPLOYMENT_ENVIRONMENT)
MAIN_RESOURCES_NAME = "solar-api"
AUTHOR = "Lloyd Spencer and Carlos Espinosa"


def add_tags_to_stack(stack):
    """
    Simple function to add custom tags to stack in a centralized (equal) approach.
    """

    cdk.Tags.of(stack).add("Environment", DEPLOYMENT_ENVIRONMENT)
    cdk.Tags.of(stack).add("Author", AUTHOR)
    cdk.Tags.of(stack).add("Identifier", MAIN_RESOURCES_NAME)


def validate_correct_deployment_environment(environment):
    """
    Simple function that validates the deployment environment.
    """
    if environment == "dev" or environment == "prod":
        print("Environment for deployment is: {}".format(environment))
        return True
    else:
        print("THE ENVIRONMENT FOR THE DEPLOYMENT IS NOT VALID (ONLY ALLOWED \"DEV\" or \"PROD\")")
        return False
