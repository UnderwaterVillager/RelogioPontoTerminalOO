import os
from dataclasses import dataclass

from clock_interfaces import  Clock

class User:
    def __init__(self, code):
        self._code = code if code else None

    @property
    def code(self):
        return self._code

    def profile():
        pass


class Worker(User):
    def __init__(self, code):
        super().__init__(code)
    
    def call_clock_doc():
        pass

    def run(self):
        while True:
            print("Escolha a operação:")
            operation = input("1- Bater ponto\n2- Ver folhas de ponto\n3- Contar faltas\nOutros- Voltar\n")
            match operation:
                case '1':
                    os.system('clear')
                    clock = Clock(self.code)
                    clock.run()
                    continue
                case '2':
                    pass
                case '3':
                    pass
                case _:
                    os.system('clear')
                    break

