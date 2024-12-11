import os
import json
from abc import ABC, abstractmethod

# TODO implementar validação
# Cada validação pode ser instanciada no setter
class UserDataHandler(ABC):
    def __init__(self):
        self._file_path = "ponto_data.json"
        self._menu_type = None
        ## Campo útil a possível valições;
        self._data_structure = {
            "Matricula" : None,
            "Senha": None,
        }
        self._code = self._data_structure["Matricula"]
        self._password = self._data_structure["Senha"]

    @property
    def file_path(self):
        return self._file_path

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
        print("Matricula validado")
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

    # Cada setter retorna o valor validado e o estado de validação
    def set_data(self):
        self.code = self.data_structure["Matricula"]


    def read_json(self):
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
            forward = input("1- Inserir dados\n2- Voltar ao início\n")

            if forward == '2':
                break

            self.input_data(self.data_structure)

            os.system('clear')
            print("Estes foram os dados digitados.\n")

            for i, j in list(self.data_structure.items()):
                print(f'{i}: {j}\n')

            # Preparar validação;
            self.set_data()

            confirmation = input("Confirmar(DIGITE UM NÚMERO)?\n1- SIM\n2-NÃO\n")

            match confirmation:
                case '1':
                    try:
                        os.system('clear')
                        self.finish_data_handler()
                    except:
                        continue
                    break
                case '2':
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
        self._code = self._data_structure["Nome"]
        self._password = self._data_structure["Email"]

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        print("Nome validado")
        self._name = value

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        print("Email validado")
        self._email = value

    def set_data(self):
        self.name = self.data_structure["Nome"]
        self.code = self.data_structure["Matricula"]
        self.email = self.data_structure["Email"]

    def write_json(self, new_data, retrieved_data=[]):
        try:
            with open(self.file_path, "w") as db:
                if isinstance(retrieved_data, list):
                    retrieved_data.append(new_data)
                json.dump(retrieved_data, db)
            print("Gravação concluída!")
        except:
            print("Algo de errado ocorreu com a gravação de dados.")


    def finish_data_handler(self):
        try:
            db_data = self.read_json()
            if not db_data:
                self.write_json(self.data_structure)
            else:
                for i in db_data:
                    if i["Matricula"] == self.data_structure["Matricula"]:
                        print("Matricula existente!")
                        raise Exception("Matricula existente!")
                self.write_json(self.data_structure, db_data)
        except:
            print("Algo deu errado com o cadastro.")
    
class SignInInterface(UserDataHandler):
    def __init__(self):
        super().__init__()
        self._menu_type = 'login'

    def finish_data_handler(self):
        db_data = self.read_json()
        for data_entry in db_data:
            if data_entry["Matricula"] == self.data_structure["Matricula"]:
                if data_entry["Senha"] == self.data_structure["Senha"]:
                    print("Login realizado!")
                    return
                else:
                    os.system('clear')
                    print("Senha incorreta!")
                    raise Exception("Senha incorreta!")
        os.system('clear')
        print("Cadastro não encontrado!")
        raise Exception("Cadastro não encontrado!")


        

class MainMenu:
    def display_options(self):
        os.system('clear')
        while(True):
            enter_option = input("Escolha a sua opção:\n1- Iniciar sessão\n2- Cadastrar-se\n")
            match enter_option:
                case '1':
                    os.system('clear')
                    login = SignInInterface()
                    login.menu()
                    continue
                case '2':
                    os.system('clear')
                    cadastro = SignUpInterface()
                    cadastro.menu()
                    continue
                case _:
                    os.system("clear")
                    print("Escolha as opções disponíveis.")
                
