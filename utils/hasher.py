import string
import random
import json
import xmltodict


class hasher:
    def salt_generator(self, length=int):
        # Generate a random salt of specified length
        characters = string.ascii_letters + string.digits 
        random_string = ''.join(random.choices(characters, k=length))
        return random_string

    def response_parser(self, response):
        # Take an XML response from Subsonic API and convert to JSON
        decoded_response = response.content.decode("utf-8")
        response_as_json = json.loads(json.dumps(xmltodict.parse(decoded_response)))
        response = {
            "server_version": response_as_json['subsonic-response']['@serverVersion'],
            "result": response_as_json['subsonic-response']['@status']
        }
        if response_as_json['subsonic-response']['@status'] == 'failed':
            response['response_code'] = response_as_json['subsonic-response']['error']['@code']
            response['response_message'] = response_as_json['subsonic-response']['error']['@message']
        
        return response