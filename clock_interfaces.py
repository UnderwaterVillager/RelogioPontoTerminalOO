from datetime import datetime
import os, json

class ClockRegisterDocHandler:
    doc_day_structure = {"Entrada": [], "Saida": []}

    def __init__(self, code, date):
        self._selected_date = date
        self._file_path = f'db/{code}/folhas/'
        self._code = code

    @property
    def file_path(self):
        return self._file_path

    @property
    def code(self):
        return self._code

    @property
    def selected_date(self):
        return self._selected_date
    
    def get_json_day(self, month, day, mode):
        try:
            if(os.stat(f'db/folhas_diarias/{month}/{day}.json').st_size == 0):
                return None
        except FileNotFoundError:
            print("Arquivo do dia não encontrado.")
            return None
        try:
            with open(f'db/folhas_diarias/{month}/{day}.json') as doc:
                day_dict = json.load(doc)
                print("Carregado ao dia.")
                return day_dict
        except:
            print("Erro ao carregar folha do dia.")

    def write_json_day(self, new_data, current_data):
        mode = new_data["Modo"]
        try:
            if isinstance(current_data, dict):
                writing_list = current_data[mode]
                if isinstance(writing_list, list):
                    writing_list.append(new_data)
            else:
                print("Dados do ponto em formato incorreto.")
                return None
            if not os.path.exists(f'db/folhas_diarias/{new_data["Mes"]}/'):
                os.mkdir(f'db/folhas_diarias/{new_data["Mes"]}/')
            with open(f'db/folhas_diarias/{new_data["Mes"]}/{new_data["Dia"]}.json', 'w') as doc:
                json.dump(current_data, doc)
                print("Arquivo do dia salvo.")
        except:
            print('Erro ao escrever na folha do dia.')


    def get_json_personal(self):
        try:
            if (os.stat(f'{self.file_path}{self.selected_date}.json').st_size == 0):
                return None
        except FileNotFoundError:
            print("Arquivo do pontista não encontrado.")
            return None
        try:
            with open(f'{self.file_path}{self.selected_date}.json', 'r') as doc:
                clock_list = json.load(doc)
                print("Carregado ao pontista.")
                return clock_list
        except:
            print("Erro ao carregar folha de ponto.")

    def write_json_personal(self, new_data, current_data):
        try:
            if isinstance(current_data, list):
                current_data.append(new_data)
            else:
                print("Dados do ponto em formato incorreto.")
                raise Exception("Dados do ponto em formato incorreto.")
            with open(f'{self.file_path}{self.selected_date}.json', 'w') as doc:
                json.dump(current_data, doc)
                print("Arquivo do pontista salvo.")
        except:
            print('Erro ao escrever na folha de ponto.')
            
    def view_clock_doc(self):
        current_data = self.get_json_personal()
        if current_data:
            print(f"Folha de {self.code} no mes")
            print("*------------------------------*")
            print('Dia/Mes | Hora : Minuto | Modo')
            print("*------------------------------*")
            for i  in current_data:
                print(f'{i["Dia"]}/{i["Mes"]} | {i["Hora"]}:{i["Minuto"]} | {i["Modo"]}')
            print('')
            return
        print("Dados não encontrados.")


    def save_clock_personal(self, new_data):
        current_data = self.get_json_personal()
        if current_data and isinstance(current_data, list):
            for i in current_data:
                if (i['Dia'] == new_data['Dia']) and (i['Mes'] == new_data['Mes']) and (i['Ano'] == new_data['Ano']) and (i['Modo'] == new_data['Modo']):
                    print("Não é possível bater o mesmo tipo de ponto duas vezes no dia.")
                    raise Exception("Ponto batido no mesmo dia.")
            self.write_json_personal(new_data, current_data)
        else:
            self.write_json_personal(new_data, [])

    def save_clock_day(self, new_data):
        current_data = self.get_json_day(new_data["Mes"], new_data["Dia"], new_data["Modo"])
        if current_data and isinstance(current_data, dict):
            self.write_json_day(new_data, current_data)
        else:
            self.write_json_day(new_data, self.doc_day_structure)

    def save_clock(self, new_data):
        try:   
            self.save_clock_personal(new_data)
            self.save_clock_day(new_data)
        except:
            print("Erro ao salvar ponto.")

class Clock:
    def __init__(self, code):
        self._code = code
        self._current_time_fields = {
            'Dia': '',
            'Mes': '',
            'Ano': '',
            'Hora': '',
            'Minuto': '',
            'Modo': '',
        }

    @property
    def worker_code(self):
        return self._code

    @property
    def current_time_fields(self):
        return self._current_time_fields
    
    @current_time_fields.setter
    def current_time_fields(self, value):
        self._current_time_fields = value        

    def get_current_time(self):
        current_time = datetime.now()
        return current_time


    def hit_clock(self, data_path):
        clock_doc_cli = ClockRegisterDocHandler(self.worker_code, data_path)
        clock_doc_cli.save_clock(self.current_time_fields)

    def run(self):
        while True:
            current_time = self.get_current_time()
            self.current_time_fields = {
                "Matricula": self._code,
                "Dia": current_time.day,
                "Mes": current_time.month,
                'Ano': current_time.year,
                'Hora': current_time.hour,
                'Minuto': current_time.minute,
                'Modo': ''
            }
            print(f'Horario a bater ponto: {current_time.strftime("%d/%m/%Y | %H:%M")}')
            confirm_clock = input("Bater ponto?\n1- Sim\nOutros- Voltar\n")
            match confirm_clock:
                case '1':
                    is_clock_on = input("Horario de entrada ou saida?\n1- Entrada\n2- Saída\nOutros- Voltar\n")
                    match is_clock_on:
                        case '1':
                            self.current_time_fields['Modo'] = 'Entrada'
                        case '2':
                            self.current_time_fields['Modo'] = 'Saida'
                        case _:
                            os.system('clear')
                            continue
                    os.system('clear')
                    self.hit_clock(current_time.strftime("%m-%Y"))
                    break
                case _:
                    os.system('clear')
                    break

class ClockDocView:
    def __init__(self, code):
        self._file_path = f'db/{code}/folhas/'
        self._code = code

    @property
    def code(self):
        return self._code

    def run(self):
        selected_month = input("Selecione um mes:\n")
        selected_year = input("Selecione um ano:\n")
        clock_doc_cli = ClockRegisterDocHandler(self.code, f"{selected_month.zfill(2)}-{selected_year.zfill(2)}")
        clock_doc_cli.view_clock_doc()
        
