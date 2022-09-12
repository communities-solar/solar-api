#!/usr/bin/env python3
import os
import aws_cdk as cdk

import global_configurations
from cdk_storage.cdk_stack_rds import CdkStackStorageRDS


app = cdk.App()

storage_stack = CdkStackStorageRDS(
    app,
    "{}-{}-stack-storage-rds-cdk".format(global_configurations.DEPLOYMENT_ENVIRONMENT, global_configurations.MAIN_RESOURCES_NAME),
    global_configurations.NAME_PREFIX,
    global_configurations.MAIN_RESOURCES_NAME,
    global_configurations.DEPLOYMENT_ENVIRONMENT,
    global_configurations.DEPLOYMENT_VERSION,
    env={
        "account": os.environ["CDK_DEFAULT_ACCOUNT"], 
        "region": os.environ["CDK_DEFAULT_REGION"]
    },
    description="Stack for Storage (RDS) for {} solution".format(global_configurations.MAIN_RESOURCES_NAME),
)

global_configurations.add_tags_to_stack(storage_stack)

app.synth()
