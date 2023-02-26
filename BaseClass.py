
import random

def generate_random_number():
    prefix = "070"
    random_suffix = str(random.randint(0, 9999999)).zfill(7)
    return prefix + random_suffix


def generate_random_text(characters, length):
    """
    Generates random text from an array of characters of a given length.

    :param characters: list of characters to generate text from
    :param length: length of the generated text
    :return: random text of the specified length
    """
    # use random.choices to randomly select characters from the list
    # repeat the process for the specified length and join the results into a string
    return ''.join(random.choices(characters, k=length))