import fire
import requests

BASE_URL = 'http://127.0.0.1'
HEADERS = {"Content-Type":"application/json"}

class WebClient(object):
    def create_endpoint(self, endpoint_name):
        """
        Method to create endpoint
        param name: name of the endpoint
        returns: json with endpoint code
        """
        # Create json body
        json_body = {'id': endpoint_name}
        # Create full request URL
        create_endpoint_url = BASE_URL + ':8000/endpoint'
        # Getting response
        response = requests.post(create_endpoint_url, json=json_body, headers=HEADERS)
        if response.status_code == 200:
            jsonResponse = response.json()
            print(('{message}, code is: {code}').format(message = jsonResponse['message'], code = jsonResponse['code']))
        else:
            print('Something went wrong, try again later.')
    
    def echo_message(self, endpoint_name, code, message):
        """
        Method to log message from endpoint
        param name: name of the endpoint
        param code: code returned after endpoint creation
        param message: message to record at log file
        returns: json with request status
        """
        # Create json body
        json_body = {'id': endpoint_name, 'code': code, 'message': message}
        # Create full request URL
        echo_message_url = BASE_URL + ':8001/echo'
        # Getting response
        response = requests.post(echo_message_url, json=json_body, headers=HEADERS)
        if response.status_code == 200:
            jsonResponse = response.json()
            print(('{message}').format(message = jsonResponse['message']))
        else:
            jsonResponse = response.json()
            print(('Something went wrong, try again later, reason: {reason}').format(reason = jsonResponse['reason']))

if __name__ == '__main__':
  fire.Fire(WebClient)