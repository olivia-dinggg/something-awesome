import random
import string

def generate_random_string(length):
    # Define the character set from which to generate the random string
    characters = string.ascii_letters + string.digits  # Letters (uppercase and lowercase) and digits
    # You can customize the character set by adding or removing characters as needed

    # Generate a random string of the specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


mode = input("Enter the mode you would like (R/HTTP):")
if mode == "R":
    length = int(input("Enter the length of the random string: "))
    random_string = generate_random_string(length)
