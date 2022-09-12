#!/usr/bin/env python3
import os
import aws_cdk as cdk

import global_configurations
from cdk_storage.cdk_stack_dynamodb import CdkStackStorageDynamoDB


app = cdk.App()

storage_stack = CdkStackStorageDynamoDB(
    app,
    "{}-{}-stack-storage-dynamodb-cdk".format(global_configurations.DEPLOYMENT_ENVIRONMENT, global_configurations.MAIN_RESOURCES_NAME),
    global_configurations.NAME_PREFIX,
    global_configurations.MAIN_RESOURCES_NAME,
    global_configurations.DEPLOYMENT_ENVIRONMENT,
    global_configurations.DEPLOYMENT_VERSION,
    env={
        "account": os.environ["CDK_DEFAULT_ACCOUNT"], 
        "region": os.environ["CDK_DEFAULT_REGION"]
    },
    description="Stack for Storage (DynamoDB) for {} solution".format(global_configurations.MAIN_RESOURCES_NAME),
)

global_configurations.add_tags_to_stack(storage_stack)

app.synth()
