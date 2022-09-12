# HELPERS FOR DYNAMODB FUNCTIONALITIES
# Built-in imports
import datetime
import uuid

def create_update_lead_information(table_table_resource, agent_id, lead_id, supplier_id, result, extra_information):
    """
    Function to create lead information summary
    :param table_table_resource: AWS DynamoDB boto3 table resource (Table).
    :param agent_id: agent id (string).
    :param lead_id: lead id (string).
    :param supplier_id: supplier id (string).
    :param result: result of RDS query (string).
    :param extra_information: reason for failure (string).
    """
    # Obtain current datetime for timestamp record
    now = datetime.datetime.now()
    datetime_formatted = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Create unique identifier
    unique_id = str(uuid.uuid4())[0:4]

    json_item_structure = {
        "record_id": "{}_{}".format(datetime_formatted, unique_id),
        "agent_id": agent_id,
        "lead_id": lead_id,
        "supplier_id": supplier_id,
        "result": result,
        "extra_information": extra_information,
        "timestamp": datetime_formatted,
    }
    response = table_table_resource.put_item(Item=json_item_structure)

    return response
