# Built-in imports
import logging
import os
import json
import boto3

# Own imports
import api_return_format
import rds_helpers
import dynamodb_helpers

# External dependencies imports (from lambda layer)
from aws_lambda_powertools.utilities import parameters
import mysql.connector


# Configure logging
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

# Get environment variables for DynamoDB, RDS and Secrets
TABLE_NAME = os.environ.get("TABLE_NAME")
RDS_HOST = os.environ.get("RDS_HOST")
RDS_DATABASE = os.environ.get("RDS_DATABASE")
RDS_SECRET_NAME = os.environ.get("RDS_SECRET_NAME")
API_SECRET_NAME = os.environ.get("API_SECRET_NAME")

# Configure AWS resources
dynamodb_resource = boto3.resource("dynamodb")
dynamodb_table_resource = dynamodb_resource.Table(TABLE_NAME)
rds_secret = json.loads(parameters.get_secret(RDS_SECRET_NAME))
api_secret = json.loads(parameters.get_secret(API_SECRET_NAME))


# Load RDS connector
mydb_connector = mysql.connector.connect(
    host=RDS_HOST,
    user=rds_secret["username"],
    password=rds_secret["password"],
    database=RDS_DATABASE,
)


def lambda_handler(event, context):
    """
    Lambda function handler for the overall functionality orchestration.
    """

    LOG.info("lambda_handler: event is {}".format(event))
    
    # Validations of the API call and query-parameters
    if event["queryStringParameters"] is not None:
        # Validation of query params
        username_validation = "username" in event["queryStringParameters"]
        password_validation = "password" in event["queryStringParameters"]
        lead_id_validation = "lead_id" in event["queryStringParameters"]
        supplier_id_validation = "supplier_id" in event["queryStringParameters"]
        agent_id_validation = "agent_id" in event["queryStringParameters"]

        if (username_validation and password_validation and lead_id_validation and supplier_id_validation and agent_id_validation):
            agent_id = event["queryStringParameters"]["agent_id"]
            supplier_id = event["queryStringParameters"]["supplier_id"]
            lead_id = event["queryStringParameters"]["lead_id"]
            api_username = event["queryStringParameters"]["username"]
            api_password = event["queryStringParameters"]["password"]

            # Authentication for Solar API (retrieved from secret)
            if api_secret["username"] == api_username and api_secret["password"] == api_password:
                api_final_result =  rds_helpers.read_lead_from_id(event, mydb_connector, lead_id)
                print("api_final_result status code is : {}".format(api_final_result["statusCode"]) )

                if api_final_result["statusCode"] == 200:
                    # Add logs of successful request details to dynamodb table
                    dynamodb_response = dynamodb_helpers.create_update_lead_information(
                        dynamodb_table_resource,
                        agent_id,
                        lead_id,
                        supplier_id,
                        "successful",
                        None,
                    )
                    print("dynamodb_response for request info is : {}".format(dynamodb_response))

                    return api_final_result

    # Add logs of failure request details to dynamodb table
    dynamodb_response = dynamodb_helpers.create_update_lead_information(
        dynamodb_table_resource,
        None,
        None,
        None,
        "failure",
        "The request to the endpoint did not contain all the necessary correct query parameters."
    )
    print("dynamodb_response for request info is : {}".format(dynamodb_response))

    # If a validation fails, return usage explanation message (how to call API)
    return_usage_dict = {
        "instructions": "Please call this endpoint as the <type_usage> indicates...",
        "read_usage": "?username=<username>&password=<password>&supplier_id=<supplier_id>&lead_id=<lead_id>&agent_id=<agent_id>",
    }
    return api_return_format.get_return_format(200, json.dumps(return_usage_dict, indent=2, default=str))
