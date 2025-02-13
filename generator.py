import random
import string


class UserGenerator:
    @staticmethod
    def generate_email():
        return f'{"".join(random.choices(string.ascii_lowercase, k=8))}@example.com'

    @staticmethod
    def generate_password():
        return "".join(random.choices(string.ascii_letters + string.digits, k=12))

    @staticmethod
    def generate_name():
        return "".join(random.choices(string.ascii_letters, k=6))

    @classmethod
    def generate_user(cls):
        return {
            "email": cls.generate_email(),
            "password": cls.generate_password(),
            "name": cls.generate_name(),
        }

