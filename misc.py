import hashlib

def encrypthash(argument):
    encoded = argument.encode()
    result = hashlib.sha256(encoded)
    encrypted_argument = result.hexdigest()
    return encrypted_argument