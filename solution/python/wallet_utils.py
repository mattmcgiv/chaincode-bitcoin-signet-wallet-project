import hashlib
from Crypto.Hash import SHA256, RIPEMD160
def parse_derivation_path(derivation_path):
    # Split the path by '/'
    path_parts = derivation_path.split("/")

    # Initialize the result list
    result = []

    # Process each part of the path
    for part in path_parts:
        if part == "*":
            # Ignore '*' in the path
            continue

        if part.endswith("h"):
            # Remove 'h' and mark as hardened
            index = int(part[:-1])
            hardened = True
        else:
            # Convert to int and mark as not hardened
            index = int(part)
            hardened = False

        # Add the tuple to the result list
        result.append((index, hardened))

    return result

def hash160(data):
    sha256 = hashlib.sha256(data).digest()

    # TODO: this is from a library that I may be able to remove (RIPEMD160)
    ripemd160 = RIPEMD160.new()
    ripemd160.update(sha256)

    return ripemd160.digest()