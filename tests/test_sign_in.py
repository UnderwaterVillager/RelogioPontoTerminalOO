import unittest
from unittest.mock import patch
from interfaces import SignUpInterface


class TestSignUp(unittest.TestCase):
    # Mudança de "ponteiro"
        
    @patch('builtins.input', side_effect=['Vinicius', '222006490', 'oi@gmail.com', 'cafe', '1'])
    def test_sign_up_save(self, mock_input):
        sign_up_interface = SignUpInterface()
        sign_up_interface.menu()
