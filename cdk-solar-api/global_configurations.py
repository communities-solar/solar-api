#!/usr/bin/env python3
import aws_cdk as cdk

import os

# Get deployment environment from env variable or default to development
environment = os.getenv("ENVIRONMENT", "dev")

DEPLOYMENT_VERSION = "v1"
DEPLOYMENT_ENVIRONMENT = environment
NAME_PREFIX = "{}-".format(DEPLOYMENT_ENVIRONMENT)
MAIN_RESOURCES_NAME = "solar-api"
AUTHOR = "Lloyd Spencer"


def add_tags_to_stack(stack):
    """
    Simple function to add custom tags to stack in a centralized (equal) approach.
    """

    cdk.Tags.of(stack).add("Environment", DEPLOYMENT_ENVIRONMENT)
    cdk.Tags.of(stack).add("Author", AUTHOR)
    cdk.Tags.of(stack).add("Identifier", MAIN_RESOURCES_NAME)
