# HELPERS FOR RDS QUERIES

# Built-in imports
import json

# Own imports
import api_return_format

# External dependencies imports (from lambda layer)
import mysql.connector


def read_lead_from_id(event, mysql_connector, lead_id):
    """
    Function to read a lead row from lead_id information.
    :param lead_id: identifier for the lead (str)
    :return: lead_id_json structure with result (JSON) or None.
    """
    try:
        # Create cursor for DB functionality
        cursor = mysql_connector.cursor()

        # Execute main query for leads
        cursor.execute("SELECT * FROM solar_db.leads_table WHERE lead_id='{}'".format(lead_id))
        
        # Get one result (as there are never lead_id duplicates)
        query_result = cursor.fetchone()
        print("query_result is :", query_result)
        
        # Validate query response to be not None (that lead_id exists)
        if query_result is not None:
            col_names = cursor.column_names
            json_response = {}
            for i in range(len(col_names)):
                json_response[col_names[i]] = query_result[i]
            status_code_response = 200
        else:
            json_response = {
                "message": "There was not a match for the query.",
                "details": "Server unable to get request due to wrong query (lead_id)."}
            status_code_response = 400
        print("json_response is: ", json_response)

        return api_return_format.get_return_format(status_code_response, json.dumps(json_response, indent=2, default=str))
    except mysql.connector.Error as e:
        error_message = "Error reading data from MySQL table: ", e
        print(error_message)
        return api_return_format.get_return_format(400, json.dumps(error_message, indent=2, default=str))


def create_lead(event):
    # TODO: for future development when leads_are going to be created through API calls
    pass
