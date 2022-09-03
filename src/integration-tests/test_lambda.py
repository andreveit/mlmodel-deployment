import json

import requests


class LocalLambdaTester:
    '''
    Triggers lambda functions on localhost and validates its response.
    '''

    URL = 'http://localhost:8080/2015-03-31/functions/function/invocations'

    def __init__(self, expected_response = None, event = None) -> None:
        expected_response_default = {
                'statusCode': 200
        }
        event_default = {
                'foo':'bar'
        }

        self.expected_response = expected_response or expected_response_default
        self.event = event or event_default


    def run_asserts(self):
        print('Triggering Lambda Function...')
        actual_response = requests.post(self.URL, json=self.event).json()
        print('\n\n',json.dumps(actual_response, indent=2))

        assert self.expected_response == actual_response, '[ERROR] Received unexpected response from Lambda.'



if __name__ == '__main__':

    # Validate Lambda response
    LocalLambdaTester().run_asserts()