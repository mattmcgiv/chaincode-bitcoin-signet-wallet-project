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
