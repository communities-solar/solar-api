#!/usr/bin/env python3
import aws_cdk as cdk

def add_tags_to_stack(stack):
    """
    Simple function to add custom tags to stack in a centralized (equal) approach.
    """

    cdk.Tags.of(stack).add("Environment", "Development")
    cdk.Tags.of(stack).add("Development", "Lloyd Spencer")
    cdk.Tags.of(stack).add("Identifier", "Solar API")
