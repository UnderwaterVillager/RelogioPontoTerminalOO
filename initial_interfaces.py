import os
import json
from abc import ABC, abstractmethod

from user_models import Worker

# Interfaces de login e cadastro;
## TODO implementar validação
## Cada validação pode ser instanciada no setter
class UserDataHandler(ABC):
    def __init__(self):
        self._file_path = None
        self._menu_type = None
        ### Campo útil a possível valições;
        self._data_structure = {
            "Matricula" : None,
            "Senha": None,
        }
        self._code = self._data_structure["Matricula"]
        self._password = self._data_structure["Senha"]

    @property
    def file_path(self):
        return self._file_path
    
    @file_path.setter
    def file_path(self, value):
        self._file_path = value

    @property
    def menu_type(self):
        return self._menu_type
    
    @property
    def data_structure(self):
        return self._data_structure 
    
    @data_structure.setter
    def data_structure(self, data_dict):
        self._data_structure = data_dict 

    @property
    def code(self):
        return self._code
    
    @code.setter
    def code(self, value):
        if not value:
            return
        if value[0] not in ['1', '2']:
            os.system('clear')
            print("Nao ha cargo associado com a matricula inserida.")
            return
        if value[0] == '1':
            self.file_path = 'db/pontista_dados_cadastro.json'
        elif value[0] == '2':
            self.file_path ='db/supervisor_dados_cadastro.json'
        self._code = value
    
    @property
    def password(self):
        return self._password


    @abstractmethod
    def finish_data_handler(self):
        pass

    def input_data(self, obj_ds):
        for i in list(obj_ds.keys()):
            prompt_data = input(f'Digite {i}:\n')
            obj_ds[i] = prompt_data
        self.data_structure = obj_ds

    ### Cada setter retorna o valor validado e o estado de validação
    def set_data(self):
        self.code = self.data_structure["Matricula"]

    def null_data(self):
        self.code = None

    def read_self_json(self):
        try:
            if (os.stat(self.file_path).st_size == 0):
                return None
        except FileNotFoundError:
            return None
        try:
            with open(self.file_path, "r") as db:
                data = json.load(db)
                if data:
                    print("Carregado!")
            return data
        except:
            print("Algo deu errado na recuperação de dados")

## Validação não prioritária;
    def menu(self):
        while(True):
            print(f"Esta é a tela de {self.menu_type}")
            forward = input("1- Inserir dados\nOutros- Voltar ao início\n")

            if forward != '1':
                os.system('clear')
                break

            self.input_data(self.data_structure)

            os.system('clear')
            print("Estes foram os dados digitados.\n")

            for i, j in list(self.data_structure.items()):
                print(f'{i}: {j}\n')

            
            confirmation = input("Confirmar(DIGITE UM NÚMERO)?\n1- SIM\nOutros- NÃO\n")

            try:
                os.system('clear')
                self.set_data()
            except:
                os.system('clear')
                self.null_data()
                continue

            match confirmation:
                case '1':
                    try:
                        result = self.finish_data_handler()
                        return result
                    except:
                        continue
                case _:
                    os.system('clear')
                    continue


class SignUpInterface(UserDataHandler):
    def __init__(self):
        super().__init__()
        self._menu_type = 'cadastro'
        self._data_structure = {
            "Nome" : None,
            "Matricula" : None,
            "Email": None,
            "Senha": None,
        }
        self._name = self._data_structure["Nome"]
        self._email = self._data_structure["Email"]

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = value

    def set_data(self):
        self.name = self.data_structure["Nome"]
        self.code = self.data_structure["Matricula"]
        self.email = self.data_structure["Email"]

    def null_data(self):
        self.name = None
        self.code = None
        self.email = None


    def create_file_path(self):
        try:
            os.mkdir(f'db/{self.data_structure["Matricula"]}/')
            if self.code[0] == '1':
                os.mkdir(f'db/{self.data_structure["Matricula"]}/folhas/')
        except FileExistsError:
            print("Diretório da referida matricula ja existe.")
        except Exception as e:
            print(f'Ocorreu um erro: {e}')

    def write_json(self, new_data, retrieved_data):
        try:
            if self.file_path == 'db/pontista_dados_cadastro.json':
                new_data["Supervisor"] = ''
                if 'Pontistas' in new_data and isinstance(new_data, dict):
                    new_data.pop('Pontistas')
            else:
                new_data["Pontistas"] = []
                if 'Supervisor' in new_data and isinstance(new_data, dict):
                    new_data.pop('Supervisor')
            with open(self.file_path, "w") as db:
                if isinstance(retrieved_data, list):
                    retrieved_data.append(new_data)
                json.dump(retrieved_data, db)
            print("Gravação concluída!")
        except:
            print("Algo de errado ocorreu com a gravação de dados.")
            raise Exception("Algo de errado ocorreu com a gravação de dados.")


    def finish_data_handler(self):
        try:
            db_data = self.read_self_json()
            if not db_data:
                self.create_file_path()
                self.write_json(self.data_structure, [])
                print("Cadastro realizado")
            else:
                for i in db_data:
                    if i["Matricula"] == self.data_structure["Matricula"]:
                        print("Matricula existente!")
                        raise Exception("Matricula existente!")
                self.create_file_path()
                self.write_json(self.data_structure, db_data)
                print("Cadastro realizado!")
        except:
            print("Algo deu errado com o cadastro.")
    
class SignInInterface(UserDataHandler):
    def __init__(self):
        super().__init__()
        self._menu_type = 'login'

    def finish_data_handler(self):
        db_data = self.read_self_json()
        if not db_data:
            print("Cadastro não encontrado!")
        for data_entry in db_data:
            if data_entry["Matricula"] == self.data_structure["Matricula"]:
                if data_entry["Senha"] == self.data_structure["Senha"]:
                    print("Login realizado!")
                    return self.code
                else:
                    os.system('clear')
                    print("Senha incorreta!")
                    raise Exception("Senha incorreta!")
        os.system('clear')
        print("Cadastro não encontrado!")
        raise Exception("Cadastro não encontrado!")

# Fim de Interface de Login e Cadastro





# Interface Inicial
class MainMenu:
    def menu_signup(self):
        cadastro = SignUpInterface()
        cadastro.menu()

    def menu_login(self):
        login = SignInInterface()
        logged_code = login.menu()
        return logged_code
    

    def display_options(self):
        while(True):
            enter_option = input("Escolha a sua opção:\n1- Iniciar sessão\n2- Cadastrar-se\nOutros- Sair\n")
            match enter_option:
                case '1':
                    os.system('clear')
                    logged_code = self.menu_login()

                    if logged_code:
                        match logged_code[0]:
                            case '1':
                                user = Worker(logged_code)
                            case '2':
                                pass
                            case _:
                                break
                        if user:
                            user.run()
                    continue
                case '2':
                    os.system('clear')
                    self.menu_signup()
                    continue
                case _:
                    return
                
