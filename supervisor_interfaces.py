import os, json

class WorkerListInterface:
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
                if data:
                    print("Carregado!")
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
            print("Gravação concluída!")
        except:
            print("Algo de errado ocorreu com a gravação de dados.")
            raise Exception("Algo de errado ocorreu com a gravação de dados.")
        
    def write_json_assign_supervisor(self, workers, selected_worker, supervisor_code):
        try:
            for i in workers:
                if i["Matricula"] == selected_worker:
                    i["Supervisor"] = supervisor_code
                    break
            with open(self.file_path_worker, "w") as db:
                json.dump(workers, db)
            print("Gravação concluída!")
        except:
            print("Algo de errado ocorreu com a gravação de dados.")
            raise Exception("Algo de errado ocorreu com a gravação de dados.")

    
    def assigning(self, worker):
        try:
            os.system('clear')
            supervisor_data = self.read_json(self.file_path_supervisor)
            self.write_json_assign_worker(supervisor_data, worker)
            worker_data = self.read_json(self.file_path_worker)
            self.write_json_assign_supervisor(worker_data, worker, self.code)
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
                    print(f"Nome: {i["Nome"]} | Matricula: {i["Matricula"]} | Email: {i["Email"]}\n")
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

