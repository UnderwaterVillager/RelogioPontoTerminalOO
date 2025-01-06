import os

from clock_interfaces import  Clock, ClockDocView, ClockDayView
from supervisor_interfaces import WorkerAssignInterface, WorkerViewInterface

class User:
    def __init__(self, code):
        self._code = code if code else None

    @property
    def code(self):
        return self._code


class Worker(User):
    def __init__(self, code):
        super().__init__(code)

    def run(self):
        while True:
            print("Escolha a operação:")
            operation = input("1- Bater ponto\n2- Ver folhas de ponto\nOutros- Voltar\n")
            match operation:
                case '1':
                    os.system('clear')
                    clock = Clock(self.code)
                    clock.run()
                    continue
                case '2':
                    os.system('clear')
                    clock_doc_viewer = ClockDocView(self.code)
                    clock_doc_viewer.run()
                    continue
                case _:
                    os.system('clear')
                    break

class Supervisor(User):
    def __init__(self, code):
        super().__init__(code)

    def assign_worker(self):
        worker_input = WorkerAssignInterface(self.code)
        worker_input.run()

    def view_workers(self):
        worker_view = WorkerViewInterface(self.code)
        worker_view.run()

    def view_doc_day(self):
        day_view = ClockDayView(self.code)
        day_view.run()



    def run(self):
        while True:
            print("Escolha a operação:")
            operation = input("1- Adicionar pontista\n2- Ver pontista\n3- Ver folha do dia\nOutros- Voltar\n")
            match operation:
                case '1':
                    os.system('clear')
                    self.assign_worker()
                    continue
                case '2':
                    os.system('clear')
                    self.view_workers()
                    continue
                case '3':
                    os.system('clear')
                    self.view_doc_day()
                    continue
                case _:
                    os.system('clear')
                    break