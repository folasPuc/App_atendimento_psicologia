from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.app import App
from datetime import date, timedelta
from functools import partial
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
import requests
import json

class LoginPage(Screen):
    pass
class Menu(Screen):
    pass
class MenuAdmin(Screen):
    pass
class TodosPacientes(Screen):
    pass
class ProcurarPaciente(Screen):
    pass
class AlterarFicha(Screen):
    pass
class BoxFicha(Screen):
    pass
class LabelButton(ButtonBehavior,Label ):
    pass
class ImageButton(ButtonBehavior,Image ):
    pass

class TimePicker(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(TimePicker, self).__init__(**kwargs)
        self.orientation = "horizontal"
        link = f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/Horarios.json"
        req = requests.get(link)
        requisicao_dic = req.json()
        Horario = requisicao_dic['Horarios']
        Horario_split = Horario.split(',')
        print(Horario_split)
        #self.times = ['9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM']
        self.times = Horario_split
        #print(self.times)
        self.selected_times = set()

        for time in self.times:
            time_button = Button(text=time)
            time_button.bind(on_press=self.select_time)
            self.add_widget(time_button)

        edit_button = Button(text="Editar Horários")
        edit_button.bind(on_press=self.edit_times)
        self.add_widget(edit_button)

    def select_time(self, instance):
        if instance.state == 'down':
            self.selected_times.add(instance.text)
    def edit_times(self, instance):
        popup_content = GridLayout(cols=2, spacing=5)
        times_input = TextInput(text=", ".join(self.times), multiline=False)
        save_button = Button(text="Salvar")
        save_button.bind(on_press=partial(self.save_times, times_input))
        popup_content.add_widget(Label(text="Horários (separados por vírgula):"))
        popup_content.add_widget(times_input)
        popup_content.add_widget(save_button)

        popup = Popup(title="Editar Horários Disponíveis",
                      content=popup_content, size_hint=(None, None), size=(400, 200))
        popup.open()

    def save_times(self, times_input, instance):
        new_times = [time.strip() for time in times_input.text.split(',')]
        self.times = new_times
        horarios = self.times
        horarios_str = [str(time) for time in horarios]
        horarios_combined = ', '.join(horarios_str)
        print(horarios_combined)
        link = f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/Horarios.json"
        info_dia = f'{{"Horarios": "{horarios_combined}"}}'
        req = requests.patch(link, data = info_dia)


        self.clear_widgets()
        self.selected_times.clear()

        for time in self.times:
            time_button = Button(text=time)
            time_button.bind(on_press=self.select_time)
            self.add_widget(time_button)

        edit_button = Button(text="Editar Horários")
        edit_button.bind(on_press=self.edit_times)
        self.add_widget(edit_button)


class DatePicker(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(DatePicker, self).__init__(**kwargs)
        self.date = date.today()
        self.orientation = "vertical"
        self.month_names = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
        self.header = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.body = GridLayout(cols=7)
        self.time_picker = TimePicker(size_hint=(1, 0.2))
        self.add_widget(self.header)
        self.add_widget(self.body)
        self.add_widget(self.time_picker)

        self.available_times = {}
        self.selected_day = None

        self.populate_body()
        self.populate_header()
        

    def populate_header(self, *args, **kwargs):
        self.header.clear_widgets()
        previous_month = Button(text="<")
        previous_month.bind(on_press=partial(self.move_previous_month))
        next_month = Button(text=">", on_press=partial(self.move_next_month))
        next_month.bind(on_press=partial(self.move_next_month))
        month_year_text = self.month_names[self.date.month - 1] + ' ' + str(self.date.year)
        current_month = Label(text=month_year_text, size_hint=(2, 1))

        self.header.add_widget(previous_month)
        self.header.add_widget(current_month)
        self.header.add_widget(next_month)

    def populate_body(self, *args, **kwargs):
        self.body.clear_widgets()
        date_cursor = date(self.date.year, self.date.month, 1)
        for filler in range(date_cursor.isoweekday() - 1):
            self.body.add_widget(Label(text=""))

        while date_cursor.month == self.date.month:
            date_button = Button(text=str(date_cursor.day))
            date_button.bind(on_press=partial(self.show_available_times, day=date_cursor.day, month = date_cursor.month, year = date_cursor.year))
            self.body.add_widget(date_button)
            date_cursor += timedelta(days=1)

    def show_available_times(self, instance, *args, **kwargs):
        day = kwargs['day']
        month = kwargs['month']
        year = kwargs['year']
        print(day, month, year)
        selected_date = f"{year}-{month:02d}-{day:02d}"
        print(selected_date)
        self.selected_day = day  # Store the selected day

        available_times_for_day, bol = self.get_available_times(selected_date)

        print(f"available_times_for_day e bol aqui: {available_times_for_day, bol}")

        if day not in self.available_times:
            self.available_times[day] = set()
            print(f" available_times[day]: {self.available_times[day]}")

        popup_content = GridLayout(cols=3, spacing=5)
        if bol == True:
            for time in available_times_for_day:
                time_button = Button(text=time)
                time_button.bind(on_press=partial(self.select_time_for_day, day=day, time=time))
                if time in self.available_times[day]:
                    time_button.state = 'down'
                popup_content.add_widget(time_button)

            confirm_button = Button(text="Confirmar Consulta")
            confirm_button.bind(on_press=self.confirm_appointment)
            popup_content.add_widget(confirm_button)

            popup = Popup(title=f"Horários disponíveis para {self.month_names[self.date.month - 1]} {day}, {self.date.year}",
                        content=popup_content, size_hint=(None, None), size=(400, 400))
            popup.open()
        elif bol == False:
            for time in self.time_picker.times:
                time_button = Button(text=time)
                time_button.bind(on_press=partial(self.select_time_for_day, day=day, time=time))
                if time in self.available_times[day]:
                    time_button.state = 'down'
                popup_content.add_widget(time_button)

            confirm_button = Button(text="Confirmar Consulta")
            confirm_button.bind(on_press=self.confirm_appointment)
            popup_content.add_widget(confirm_button)

            popup = Popup(title=f"Horários disponíveis para {self.month_names[self.date.month - 1]} {day}, {self.date.year}",
                        content=popup_content, size_hint=(None, None), size=(400, 400))
            popup.open()
    
    def get_available_times(self, selected_day):
        bol = False
        print("entrando na func get_available_times")
        print(f"data selecionada: {selected_day}")
        link = f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/Horarios.json"
        req = requests.get(link)
        requisicao_dic = req.json()
        Horario = requisicao_dic['Horarios']
        Horario_split = Horario.split(',')
        #[horario.strip() for horario in Horario.split(',')]
        link = f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/Sessoes.json"
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        print(requisicao_dic)
        print(f"Horarios da medica {Horario_split}")
        for local_id_usuario in requisicao_dic:
            usuario_info = requisicao_dic[local_id_usuario]
            print(usuario_info)
            if isinstance(usuario_info, dict):
                Data = usuario_info.get('Data')
                if selected_day == Data:
                    Hora = usuario_info.get('Hora')
                    bol = True
                    print("data encontrada no banco: ")
                    print(f"Horarios marcados: {Hora}")
                    horarios_disponiveis = [horario for horario in Horario_split if horario not in Hora]
                    print(f"horarios disponiveis no if (diferente dos da medica) {horarios_disponiveis}")
                    return horarios_disponiveis, bol
                else:
                    print("entrando no else")
                    print(f"horarios disponiveis no else (igual os da medica): {Horario_split}")
        horarios_disponiveis = list(Horario_split)
        bol = False
        return horarios_disponiveis, bol

    def select_time_for_day(self, instance, *args, **kwargs):
        day = kwargs['day']
        time = kwargs['time']

        if instance.state == 'down':
            self.available_times[day].add(time)
        else:
            self.available_times[day].remove(time)

    def move_next_month(self, *args, **kwargs):
        if self.date.month == 12:
            self.date = date(self.date.year + 1, 1, self.date.day)
        else:
            self.date = date(self.date.year, self.date.month + 1, self.date.day)
        self.populate_header()
        self.populate_body()

    def move_previous_month(self, *args, **kwargs):
        if self.date.month == 1:
            self.date = date(self.date.year - 1, 12, self.date.day)
        else:
            self.date = date(self.date.year, self.date.month - 1, self.date.day)
        self.populate_header()
        self.populate_body()

    def confirm_appointment(self, instance):
        #colocar horarios no banco de dados
        selected_date = f"{self.date.year}-{self.date.month:02d}-{self.selected_day:02d}"
        selected_times = list(self.available_times.get(self.selected_day, set()))
        print(f"Consulta confirmada para {selected_date} nos horários: {selected_times}")
        with open("config.txt", "r") as arquivo:
            email = arquivo.read()
        with open("local_id.txt", "r") as arquivo:
            local_id = arquivo.read()
        selected_times_str = selected_times
        print(selected_times_str)
        print(type(selected_times_str))
        if not selected_times_str:
            print("selected_times chegou como vazio")
            popup = Popup(title=f"Nao ha horarios disponiveis para esse dia! Escolha outro dia.",
            size_hint=(None, None), size=(200, 200))
            popup.open()
            return
        else:
            pass

        link = f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/Sessoes.json"
        info_dia = f'{{"{local_id}": ""}}'
        req = requests.patch(link, data = info_dia)
        req_dic = req.json()

        link = f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/Sessoes/{local_id}.json"
        info_dia = f'{{"Nome": "{email}", "Data": "{selected_date}", "Hora": "{selected_times_str}"}}'
        req = requests.patch(link, data = info_dia)
        req_dic = req.json()
        print(req_dic)
        print(selected_times_str)
        
        popup = Popup(title=f"Obrigado {email}! Sua sessao foi marcada para {selected_date} as {selected_times_str}",
                         size_hint=(None, None), size=(200, 200))
        popup.open()

class MyApp(App):
    def build(self):
        return DatePicker()

if __name__ == '__main__':
    MyApp().run()
