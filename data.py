import requests
from flask import Flask,json, jsonify
import threading
from base64 import b64encode  # Import the b64encode function

app = Flask(__name__)

@app.route('/getData', methods=['GET'])
def get_xapi_statement():
    # Define your xAPI endpoint and authentication
    uuid = 'd9574430-789e-4789-8fb6-acfb5d293abe'
    endpoint = "https://lms.lrs.io/xapi/"
    auth = "Basic " + b64encode("kaunee:ifahat".encode()).decode()

    # Create the URL to retrieve the statement
    statement_url = f"{endpoint}statements?statementId={uuid}"

    # Send a GET request to retrieve the xAPI statement
    response = requests.get(statement_url, headers={"Authorization": auth})

    if response.status_code == 200:
        # Request was successful
        statement = response.json()
        return jsonify(statement)
    else:
        # Handle errors
        return jsonify({"error": "Failed to retrieve xAPI statement"}), response.status_code


@app.route('/getTerminated', methods=['GET'])
def get_terminated_xapi_statements():
    # Define your xAPI endpoint and authentication
    endpoint = "https://lmsvisualization.lrs.io/xapi/"
    auth = "Basic " + b64encode("binnom:jojeba".encode()).decode()

    # Define the query parameters to filter statements
    query_parameters = {
        "verb": "http://adlnet.gov/expapi/verbs/passed"
    }



    # Send a GET request to retrieve xAPI statements with the specified verb
    response = requests.get(endpoint + "statements", params=query_parameters, headers={"Authorization": auth})

    if response.status_code == 200:
        # Request was successful
        terminated_statements = response.json()
        return jsonify(terminated_statements)
    else:
        # Handle errors
        return jsonify({"error": "Failed to retrieve terminated xAPI statements"}), response.status_code
    

@app.route('/getAllStatements', methods=['GET'])
def get_all_xapi_statements():
    # Define your xAPI endpoint and authentication
    endpoint = "https://lms.lrs.io/xapi/"
    auth = "Basic " + b64encode("kaunee:ifahat".encode()).decode()

    # Initialize variables for pagination
    statements = []  # To store all statements
    more_statements = True
    page = 1

    while more_statements:
        # Define query parameters for pagination
        query_parameters = {
            "page": page,
            "limit": 100  # Adjust the limit as needed
        }

        # Send a GET request to retrieve xAPI statements for the current page
        response = requests.get(endpoint + "statements", params=query_parameters, headers={"Authorization": auth})

        if response.status_code == 200:
            # Request was successful
            page_statements = response.json()
            statements.extend(page_statements)
            page += 1

            # Check if there are more statements to fetch
            if len(page_statements) < query_parameters["limit"]:
                more_statements = False
        else:
            # Handle errors
            return jsonify({"error": "Failed to retrieve xAPI statements"}), response.status_code

    return jsonify(statements)

@app.route('/talentLms', methods=['GET'])
def gettalentlms():
    XAPI_KEY = 'SQ2ZkEN56h1iXACKCpqBenL51CGwce'
    # Define your xAPI endpoint and authentication
    endpoint = "http://yourdomain.talentlms.com/dev/tincan/"
    auth = "Basic " + b64encode(XAPI_KEY.encode()).decode()

    # Initialize variables for pagination
    statements = []  # To store all statements
    more_statements = True
    page = 1

    while more_statements:
        # Define query parameters for pagination
        query_parameters = {
            "page": page,
            "limit": 100   
        }

        # Send a GET request to retrieve xAPI statements for the current page
        response = requests.get(endpoint + "statements", params=query_parameters, headers={"Authorization": auth})

        if response.status_code == 200:
            # Request was successful
            try:
                page_statements = response.json()
                statements.extend(page_statements)
            except json.decoder.JSONDecodeError:
                # If the response is not valid JSON, break out of the loop
                break
            
            page += 1

            # Check if there are more statements to fetch
            if len(page_statements) < query_parameters["limit"]:
                more_statements = False
        else:
            # Handle errors
            return jsonify({"error": "Failed to retrieve xAPI statements"}), response.status_code

    return jsonify(statements)


if __name__ == '__main__':
    app.run(debug=True)
