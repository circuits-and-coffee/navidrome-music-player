import string
import random

class hasher:
    def salt_generator(self, length=int):
        # Generate a random salt of specified length
        characters = string.ascii_letters + string.digits 
        random_string = ''.join(random.choices(characters, k=length))
        return random_string

    