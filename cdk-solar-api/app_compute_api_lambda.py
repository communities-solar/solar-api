#!/usr/bin/env python3
import os
import aws_cdk as cdk

import global_configurations
from cdk_compute.cdk_stack_api_lambda import CdkStackComputeApiLambda


app = cdk.App()

compute_stack = CdkStackComputeApiLambda(
    app,
    "{}{}-stack-compute-api-lambda-cdk".format(global_configurations.DEPLOYMENT_ENVIRONMENT, global_configurations.MAIN_RESOURCES_NAME),
    global_configurations.NAME_PREFIX,
    global_configurations.MAIN_RESOURCES_NAME,
    global_configurations.DEPLOYMENT_ENVIRONMENT,
    global_configurations.DEPLOYMENT_VERSION,
    env={
        "account": os.environ["CDK_DEFAULT_ACCOUNT"], 
        "region": os.environ["CDK_DEFAULT_REGION"]
    },
    description="Stack for Compute (API, Lambda) for {} solution".format(global_configurations.MAIN_RESOURCES_NAME),
)

global_configurations.add_tags_to_stack(compute_stack)

app.synth()
