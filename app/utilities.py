from flask import make_response
import random
import string
import json


def check_request(request_state, session_state):

    response = bad_state(
        request_state,
        session_state)
    if response is not None:
        return response


def get_state_token():
    """
    Create a random string for use int state tokens for CRSF protection
    """
    token = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    return token


def bad_state(request_token, login_token):
    """
    Purpose: Check if the request has the proper state token

    Returns: A response object.  If the state is valid, the response
             is returned with 'None' as the value.
    """
    if request_token != login_token:
            response = make_response(json.dumps('Invalid state parameter.'),
                                     401)
            response.headers['Content-Type'] = 'application/json'

    else:
        response = None

    return response
    