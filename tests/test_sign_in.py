import unittest
from unittest.mock import patch
from initial_interfaces import SignUpInterface, SignInInterface
from models import Worker


class TestSignUp(unittest.TestCase):  
    @patch('builtins.input', side_effect=['Vinicius', '222006490', 'oi@gmail.com', 'cafe', '1'])
    def test_sign_up_save(self, mock_input):
        sign_up_interface = SignUpInterface()
        sign_up_interface.menu()

class TestSignIn(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', '1'])
    def test_sign_in_worker(self):
        sign_in_interface = SignInInterface()
