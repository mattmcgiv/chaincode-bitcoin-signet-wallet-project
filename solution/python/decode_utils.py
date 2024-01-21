import struct


def base58_decode_and_remove_checksum(base58check_string: str) -> bytes:
    decoded_bytes = base58_decode(base58check_string)
    return remove_checksum(decoded_bytes)


# Decode a base58 string into an array of bytes
def base58_decode(base58_string: str) -> bytes:
    # Convert Base58 string to a big integer
    big_integer = convert_base_58_string_to_integer(base58_string)
    print(big_integer)

    # Convert the integer to bytes
    converted_bytes = big_integer.to_bytes(
        # see https://github.com/keis/base58/blob/master/base58/__init__.py#L126
        (big_integer.bit_length() + 7) // 8,
        byteorder="big",
    )

    return converted_bytes

    # TODO: BONUS POINTS: Verify the checksum!


def convert_base_58_string_to_integer(base_58_string):
    # base58 alphabet
    base58_alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    # a variable to build our result and return it
    integer_result = 0

    # a variable to store the power of the base
    power_of_base = 0

    # reverse the string to start with smaller powers of 58
    reversed_string = base_58_string[::-1]

    # loop through the reversed string
    for char in reversed_string:
        # get the integer value of the character
        integer_value = base58_alphabet.find(char)

        # multiply the integer value by the power of the base
        integer_result += integer_value * (58**power_of_base)

        # increase the power of the base by 1
        power_of_base += 1

    return integer_result


def remove_checksum(bytes):
    return bytes[0:-4]
    # return bytes[:-4]
