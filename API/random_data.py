"""Generate random data"""

import random
import string


def generate_string(min_length, max_length):
    """Random string"""
    length = random.randint(min_length, max_length)
    return ''.join(random.choices(string.ascii_letters, k=length))


def generate_email():
    """Random email"""
    domains = ["example.com", "test.com", "mail.com"]
    return f"{generate_string(4, 10)}@{random.choice(domains)}"
