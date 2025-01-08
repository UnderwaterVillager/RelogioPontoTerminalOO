import os, json

from clock_interfaces import ClockDocView

class WorkerAssignInterface:
    def __init__(self, code):
        self._code = code
        self._file_path_worker = 'db/pontista_dados_cadastro.json'
        self._file_path_supervisor = 'db/supervisor_dados_cadastro.json'

    @property
    def code(self):
        return self._code

    @property
    def file_path_worker(self):
        return self._file_path_worker
    
    @property
    def file_path_supervisor(self):
        return self._file_path_supervisor


    def read_json(self, path):
        try:
            if (os.stat(path).st_size == 0):
                return None
        except FileNotFoundError:
            return None
        try:
            with open(path, "r") as db:
                data = json.load(db)
            return data
        except:
            print("Algo deu errado na recuperação de dados")

    def write_json_assign_worker(self, data, worker):
        try:
            for i in data:
                if self.code == i["Matricula"]:
                    if isinstance(i["Pontistas"], list):
                        i["Pontistas"].append(worker)
                        break
            with open(self.file_path_supervisor, "w") as db:
                json.dump(data, db)
        except:
            print("Algo de errado ocorreu com a gravação de dados.")
            raise Exception("Algo de errado ocorreu com a gravação de dados.")
        
    def write_json_assign_supervisor(self, workers, selected_worker, supervisor_code):
        returning_worker = None
        try:
            for i in workers:
                if i["Matricula"] == selected_worker:
                    i["Supervisor"] = supervisor_code
                    returning_worker = i
                    break
            with open(self.file_path_worker, "w") as db:
                json.dump(workers, db)
            return returning_worker
        except:
            print("Algo de errado ocorreu com a gravação de dados.")
            raise Exception("Algo de errado ocorreu com a gravação de dados.")

    
    def assigning(self, worker):
        try:
            os.system('clear')
            worker_list = self.read_json(self.file_path_worker)
            worker_data = self.write_json_assign_supervisor(worker_list, worker, self.code)
            supervisor_data = self.read_json(self.file_path_supervisor)
            self.write_json_assign_worker(supervisor_data, worker_data)
            print("Pontista associado!")
        except:
            print("Erro ao associar pontista e supervisor.") 

    def display_workers(self):
        counter = 0
        worker_list = self.read_json(self.file_path_worker)
        if not worker_list:
            print("Nao existe pontistas!")
            return None
        else:
            print("PONTISTAS DISPONIVEIS:\n---------------------------------")
            for i in worker_list:
                if i["Supervisor"] == '':
                    print(f"Nome: {i['Nome']} | Matricula: {i['Matricula']} | Email: {i['Email']}\n")
                    counter += 1    
            print(f"---------------------------------\n{counter} pontistas disponiveis.")
            if counter > 0:
                select_worker = input("Escolha um pontista para supervisionar:\n")
                if select_worker in [x['Matricula'] for x in worker_list]:
                    return select_worker
            return None
                
    def run(self):
        assigning_worker = self.display_workers()
        if assigning_worker:
            self.assigning(assigning_worker)
            return
        print("Pontista incorreto/indisponivel!")
        input("Digite qualquer coisa para continuar.")
        os.system("clear")
    

class WorkerViewInterface:
    def __init__(self, code):
        self._code = code
        self._file_path_worker = 'db/pontista_dados_cadastro.json'
        self._file_path_supervisor = 'db/supervisor_dados_cadastro.json'

    @property
    def code(self):
        return self._code

    @property
    def file_path_worker(self):
        return self._file_path_worker
    
    @property
    def file_path_supervisor(self):
        return self._file_path_supervisor
    
    def read_json(self, path):
        try:
            if (os.stat(path).st_size == 0):
                return None 
        except FileNotFoundError:
            return None
        try:
            with open(path, "r") as db:
                data = json.load(db)
            return data
        except:
            print("Algo deu errado na recuperação de dados")

    def write_json(self, data, path):
        try:
            with open(path, "w") as db:
                json.dump(data, db)
        except:
            print("Algo de errado ocorreu com a gravação de dados.")
            raise Exception("Algo de errado ocorreu com a gravação de dados.")

    def assigned_workers(self):
        supervisors = self.read_json(self.file_path_supervisor)
        assigned_workers = None
        counter = 0
        print("PONTISTAS ASSOCIADOS:\n---------------------------------")
        for i in supervisors:
            if i["Matricula"] == self.code:
                for j in i["Pontistas"]:
                    print(f"Nome: {j['Nome']} | Matricula: {j['Matricula']} | Email: {j['Email']}\n")
                    counter += 1
                assigned_workers = i["Pontistas"]
        print(f"---------------------------------\nPossui {counter} pontistas associados.")
        return assigned_workers
    
    def unassign_from_worker(self, worker_code, supervisor_code):
        data = self.read_json(self.file_path_worker)
        if data:
            for i in data:
                if i["Matricula"] == worker_code and i["Supervisor"] == supervisor_code:
                    i["Supervisor"] = ''
                    self.write_json(data, self.file_path_worker)
                    return
        print("Não há dados sobre o pontista selecionado.")
        raise Exception("Pontista não encontrado.")
                    
    def unassign_from_supervisor(self, worker_code, supervisor_code):
        data = self.read_json(self.file_path_supervisor)
        if data:
            for i in data:
                if i["Matricula"] == supervisor_code:
                    for j in i["Pontistas"]:
                        if j["Matricula"] == worker_code:
                            i["Pontistas"].remove(j)
                            self.write_json(data, self.file_path_supervisor)
                            return
        print("Não há dados sobre o pontista selecionado.")
        raise Exception("Pontista não encontrado.")

    
    def unassign_worker(self, worker_code):
        try:
            self.unassign_from_worker(worker_code, self.code)
            self.unassign_from_supervisor(worker_code, self.code)
            print("Pontista desassociado.")
        except:
            print("Erro ao desassociar pontista.")
    
    def run(self):
        while True:
            workers_list = self.assigned_workers()
            if workers_list:
                selected_worker = input("Digite um pontista, ou digite x para voltar:\n")
                if selected_worker in [worker["Matricula"] for worker in workers_list]:
                    while True:
                        option = input("O que gostaria de fazer com este pontista?\n1- Ver folha de Ponto\n2- Deletar Pontista\nOutros- Voltar\n")
                        match option:
                            case '1':
                                clock_doc_viewer = ClockDocView(selected_worker)
                                clock_doc_viewer.run()
                            case '2':
                                self.unassign_worker(selected_worker)
                                break
                            case _:
                                os.system("clear")
                                break
                elif selected_worker == 'x':
                    os.system("clear")
                    break
                else:
                    os.system("clear")
                    print("Digite um pontista disponível.")
            else:
                break