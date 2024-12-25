import os
from dataclasses import dataclass

class User:
    def __init__(self, name, code, email, password):
        self._name = name if name else None
        self._code = code if code else None
        self._email = email if email else None
        self._password = password if password else None

    def profile():
        pass


class Worker(User):
    def __init__(self, name, code, email, password):
        super().__init__(name, code, email, password)

    def create_file_path():
        pass
    
    def call_clock():
        pass

    def call_clock_doc():
        pass