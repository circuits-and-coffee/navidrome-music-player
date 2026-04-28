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
        # NOTE that this might not always be an XML (in the case of us getting a specific song!)
        if response.apparent_encoding == 'utf-8':
            decoded_response = response.content.decode("utf-8")
            response_as_json = json.loads(json.dumps(xmltodict.parse(decoded_response)))
            flattened_response = hasher.flatten_response({}, response_as_json)        
            return flattened_response
        else:
            return response # Will probably need to be changed in the future
    
    def flatten_response(flattened_response_tree, specific_response):    
        for node_name, value in specific_response.items():
            if isinstance(value, dict):
                hasher.flatten_response(flattened_response_tree, specific_response[node_name])
            else:
                flattened_response_tree[node_name] = value
        return flattened_response_tree
