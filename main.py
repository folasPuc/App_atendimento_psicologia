from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from myfirebase import MyFirebase
from kivymd.uix.pickers import MDDatePicker
from clientes import Clientes
from sessoes import Sessoes
from kivymd.app import ThemeManager
from kivymd.app import MDApp
import subprocess
import requests
import os
import certifi
import unicodedata
import webbrowser
from horarios import Horarios


os.environ["SSL_CERT_FILE"] = certifi.where()
# coding: utf-8

class LoginPage(Screen):
    pass
class Menu(Screen):
    pass
class MenuAdmin(Screen):
    pass
class RegisterPage(Screen):
    pass
class TodosPacientes(Screen):
    pass
class ProcurarPaciente(Screen):
    pass
class AlterarFicha(Screen):
    pass
class BoxFicha(Screen):
    pass
class TodasSessoes(Screen):
    pass
class CancelarSessao(Screen):
    pass
class MarcarConsulta(Screen):
    pass
class EditarHorarios(Screen):
    pass
class LabelButton(ButtonBehavior,Label ):
    pass
class ImageButton(ButtonBehavior,Image ):
    pass


   

GUI= Builder.load_file('main.kv')
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = "BlueGray"
        self.myfirebase = MyFirebase()
        self.theme_cls = ThemeManager()
        return GUI
    def open_link(self,**args):
        link = "https://meet.google.com/jjb-wmoo-jkq"
        webbrowser.open(link)
    def run_calendar(self):
        date_dialog = MDDatePicker(year=2024, month=1, day=17)
        date_dialog.bind(on_save=self.on_save2, on_cancel=self.on_cancel2)
        date_dialog.open()
        local_id = self.local_id
    
        with open("local_id.txt", "w") as arquivo:
            arquivo.write(local_id)
    def on_save2(self, instance, value, date_range):
        selected_date = str(value)
        print(f"Voce marcou a sessao para dia {selected_date}")
        self.get_available_times(selected_date)
        

    def on_cancel2(self, instance, value):
        pass
    
    def get_available_times(self, selected_day):
        lista_remover_horarios = self.root.ids.marcar_consulta.ids.lista_horarios
        for item in list(lista_remover_horarios.children):
            lista_remover_horarios.remove_widget(item)
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
                    print("data encontrada no banco: ")
                    print(f"Horarios marcados: {Hora}")
                    horarios_disponiveis = [horario for horario in Horario_split if horario not in Hora]
                    print(f"horarios disponiveis no if (diferente dos da medica) {horarios_disponiveis}")
                    horarios_disponiveis_str = str(horarios_disponiveis)
                    horarios_disponiveis_lista = horarios_disponiveis_str.split(',')
                    for hora in horarios_disponiveis_lista:
                        horarios = Horarios(horarios = hora)
                        marcar_consulta = self.root.ids["marcar_consulta"]
                        lista_pacientes = marcar_consulta.ids["lista_horarios"]
                        lista_pacientes.add_widget(horarios)
                    self.root.ids.marcar_consulta.ids.data_select.text = selected_day
                    self.mudar_tela("marcar_consulta")
                    return horarios_disponiveis_str
                else:
                    print("entrando no else")
                    print(f"horarios disponiveis no else (igual os da medica): {Horario_split}")
        horarios_disponiveis = list(Horario_split)
        print(f"Horario final (nao achou o dia no banco: {horarios_disponiveis})")
        horarios_disponiveis_str = str(horarios_disponiveis)
        horarios_disponiveis_lista = horarios_disponiveis_str.split(',')
        for hora in horarios_disponiveis_lista:
            horarios = Horarios(horarios = hora)
            marcar_consulta = self.root.ids["marcar_consulta"]
            lista_pacientes = marcar_consulta.ids["lista_horarios"]
            lista_pacientes.add_widget(horarios)
        self.root.ids.marcar_consulta.ids.data_select.text = selected_day
        self.mudar_tela("marcar_consulta")
        return horarios_disponiveis_str
    
    def get_available_times2(self, selected_day):
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
                    print("data encontrada no banco: ")
                    print(f"Horarios marcados: {Hora}")
                    horarios_disponiveis = [horario for horario in Horario_split if horario not in Hora]
                    print(f"horarios disponiveis no if (diferente dos da medica) {horarios_disponiveis}")
                    horarios_disponiveis_str = str(horarios_disponiveis)
                    horarios_disponiveis_lista = horarios_disponiveis_str.split(',')
                    return horarios_disponiveis_str
                else:
                    print("entrando no else")
                    print(f"horarios disponiveis no else (igual os da medica): {Horario_split}")
        horarios_disponiveis = list(Horario_split)
        print(f"Horario final (nao achou o dia no banco: {horarios_disponiveis})")
        horarios_disponiveis_str = str(horarios_disponiveis)
        horarios_disponiveis_lista = horarios_disponiveis_str.split(',')
        return horarios_disponiveis_str
    def run_calendar2(self):
        subprocess.Popen(['Python', "Calendario2.py"])
        local_id = self.local_id
        with open("local_id.txt", "w") as arquivo:
            arquivo.write(local_id)

    def on_start(self):
        self.carregar_infos_usuario()   
    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela
    def alterar_informacao(self, nova_informacao):
        with open("config.txt", "w") as arquivo:
            arquivo.write(nova_informacao)

    def voltar(self, id_tela):
        lista_remover_sessoes = self.root.ids.todas_sessoes.ids.lista_sessoes
        for item in list(lista_remover_sessoes.children):
            lista_remover_sessoes.remove_widget(item)

        link = f'https://app-psicologia-66b64-default-rtdb.firebaseio.com/Sessoes.json'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        print(requisicao_dic)
        for local_id_usuario in requisicao_dic:
            usuario_info = requisicao_dic[local_id_usuario]
            if isinstance(usuario_info, dict):
                Nome = usuario_info.get('Nome')
                Data = usuario_info.get('Data')
                Hora = usuario_info.get('Hora')
            else:
                print("tem nada")
            sessao = Sessoes(Nome = Nome, Data = Data, Hora = Hora)
            todas_sessoes = self.root.ids["todas_sessoes"]
            lista_sessoes = todas_sessoes.ids["lista_sessoes"]
            lista_sessoes.add_widget(sessao)

        self.mudar_tela(id_tela)
    def carregar_infos_usuario(self):
        try:
            with open("refreshtoken.txt", "r") as arquivo:
                refresh_token = arquivo.read()
            local_id, id_token = self.myfirebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token
            requisicao = requests.get(f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/{self.local_id}.json")
            requisicao_dic = requisicao.json()
            nome = requisicao_dic["nome"]
            email = requisicao_dic["email"]
            telefone = requisicao_dic["telefone"]
            email_user = self.root.ids.menu.ids.email_usuario.text = nome
            tel_user = self.root.ids.menu.ids.telefone_usuario.text = telefone
            if email == "adminpsico1@gmail.com":
                email_user = self.root.ids.menuadmin.ids.email_usuario.text = nome
                tel_user = self.root.ids.menuadmin.ids.telefone_usuario.text = telefone
                self.alterar_informacao(nome)
                self.mudar_tela("menuadmin")
            else:
                email_user = self.root.ids.menu.ids.email_usuario.text = nome
                tel_user = self.root.ids.menu.ids.telefone_usuario.text = telefone
                self.alterar_informacao(nome)
                self.mudar_tela("menu")
        except:
            pass
    def carregar_pacientes(self):
        lista_remover_pacientes = self.root.ids.todospacientes.ids.lista_pacientes
        for item in list(lista_remover_pacientes.children):
            lista_remover_pacientes.remove_widget(item)

        link = f'https://app-psicologia-66b64-default-rtdb.firebaseio.com/.json?orderBy="email"'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        print(type(requisicao_dic))
        for local_id_usuario in requisicao_dic:
            usuario_info = requisicao_dic[local_id_usuario]
            if isinstance(usuario_info, dict):
                email_usuario = usuario_info.get('nome')
                telefone_usuario = usuario_info.get('telefone')
                ficha_usuario = usuario_info.get('ficha')
            if email_usuario and telefone_usuario and ficha_usuario is not None:
                cliente = Clientes(email = email_usuario, telefone = telefone_usuario, ficha = ficha_usuario)
                todospacientes = self.root.ids["todospacientes"]
                lista_pacientes = todospacientes.ids["lista_pacientes"]
                lista_pacientes.add_widget(cliente)
            else:
                pass
            info = {"Email": email_usuario, "Telefone": telefone_usuario, "Ficha": ficha_usuario}
            print(info)
        # Handle the case where usuario_info is not a dictionary

            # email_usuario = requisicao_dic[local_id_usuario]['email']
            # telefone_usuario = requisicao_dic[local_id_usuario].get('telefone')
            # ficha_usuario = requisicao_dic[local_id_usuario].get('ficha')
            # if email_usuario and telefone_usuario and ficha_usuario is not None:
            #     cliente = Clientes(email = email_usuario, telefone = telefone_usuario, ficha = ficha_usuario)
            #     todospacientes = self.root.ids["todospacientes"]
            #     lista_pacientes = todospacientes.ids["lista_pacientes"]
            #     lista_pacientes.add_widget(cliente)
            # else:
            #     pass
            # info = {"Email": email_usuario, "Telefone": telefone_usuario, "Ficha": ficha_usuario}
            # print(info)
        self.mudar_tela("todospacientes")
    def carregar_dias(self):
        link = f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/.json"
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        print(requisicao_dic)
        teste = requisicao_dic['Dias']
        print(teste)
        for dia in teste:
            horario = teste[dia]
            horario_teste = horario.get('Horarios')
            lista_horarios = horario_teste.split(',')
            info = {"Dia": dia, "Horarios": lista_horarios}
            print(info['Dia'])
            print(info['Horarios'])
        self.mudar_tela("todospacientes")
    def procurar_paciente(self, email):
        link = f'https://app-psicologia-66b64-default-rtdb.firebaseio.com/.json?orderBy="nome"&equalTo="{email}"'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        for local_id in requisicao_dic:
            usuario_info = requisicao_dic[local_id]
            if isinstance(usuario_info, dict):
                email_user = usuario_info.get('nome')
                telefone_user = usuario_info.get('telefone')
                ficha_user = usuario_info.get('ficha')
            self.root.ids.alterar_ficha.ids.email_usuario.text = email_user
            self.root.ids.alterar_ficha.ids.telefone_usuario.text = telefone_user
            self.mudar_tela("alterar_ficha")
    def carregar_ficha(self):
        email = self.root.ids.alterar_ficha.ids.email_usuario.text
        link = f'https://app-psicologia-66b64-default-rtdb.firebaseio.com/.json?orderBy="nome"&equalTo="{email}"'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        for local_id in requisicao_dic:
            email_user = requisicao_dic[local_id].get('nome')
            telefone_user = requisicao_dic[local_id].get('telefone')
            ficha_user = requisicao_dic[local_id].get('ficha')
            self.root.ids.box_ficha.ids.ficha_paciente.text = ficha_user
        self.mudar_tela("box_ficha")
    def atualizar_ficha(self):
        email = self.root.ids.alterar_ficha.ids.email_usuario.text
        print(email)
        link = f'https://app-psicologia-66b64-default-rtdb.firebaseio.com/.json?orderBy="nome"&equalTo="{email}"'
        ficha_atualizada = self.root.ids.box_ficha.ids.ficha_paciente.text
        print(ficha_atualizada)
        info_usuario = f'{{"ficha": "{ficha_atualizada}"}}'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        print(requisicao_dic)
        for local_id in requisicao_dic:
            print(local_id)
            link = f'https://app-psicologia-66b64-default-rtdb.firebaseio.com/{local_id}.json'
            req = requests.patch(link, data = info_usuario)
        if req.ok:
            self.root.ids.box_ficha.ids.status.text = "Ficha alterada com sucesso"
        else:
            self.root.ids.box_ficha.ids.status.text = "Erro ao editar ficha"
        print("chegou no final da funcao")
    def carregar_sessoes(self):
        lista_remover_sessoes = self.root.ids.todas_sessoes.ids.lista_sessoes
        for item in list(lista_remover_sessoes.children):
            lista_remover_sessoes.remove_widget(item)

        link = f'https://app-psicologia-66b64-default-rtdb.firebaseio.com/Sessoes.json'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        print(requisicao_dic)
        for local_id_usuario in requisicao_dic:
            usuario_info = requisicao_dic[local_id_usuario]
            print(usuario_info)
            if isinstance(usuario_info, dict):
                Nome = usuario_info.get('Nome')
                Data = usuario_info.get('Data')
                Hora = usuario_info.get('Hora')

                print(f"data eh {Nome, Data, Hora}")
            else:
                print("tem nada")
            sessao = Sessoes(Nome = Nome, Data = Data, Hora = Hora)
            todas_sessoes = self.root.ids["todas_sessoes"]
            lista_sessoes = todas_sessoes.ids["lista_sessoes"]
            lista_sessoes.add_widget(sessao)
        self.mudar_tela("todas_sessoes")
    def cancelar_sessao(self, email):
        link = f'https://app-psicologia-66b64-default-rtdb.firebaseio.com/Sessoes.json?orderBy="Nome"&equalTo="{email}"'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        print(requisicao_dic)
        for local_id in requisicao_dic:
            usuario_info = requisicao_dic[local_id]
            if isinstance(usuario_info, dict):
                local_id_user = local_id
        #         Data = usuario_info.get('Data')
        #         Hora = usuario_info.get('Hora')
        #     self.root.ids.alterar_ficha.ids.email_usuario.text = email_user
        #     self.root.ids.alterar_ficha.ids.telefone_usuario.text = telefone_user
        #     self.mudar_tela("alterar_ficha")
        link = f'https://app-psicologia-66b64-default-rtdb.firebaseio.com/Sessoes/{local_id_user}.json'
        requisicao = requests.delete(link)
        req_dic = requisicao.json()
        print(req_dic)
        if requisicao.ok:
            self.root.ids.cancelar_sessao.ids.status.text = "Sessão cancelada com sucesso!"
        else:
            self.root.ids.cancelar_sessao.ids.status.text = "Erro ao cancelar sessão"
    def validar_marcar(self, horario_input, selected_date):
        horarios_array = self.get_available_times2(selected_date)
        print(horarios_array)
        print(horario_input)
        if horario_input in horarios_array:
            print(f'O horário {horario_input} está na lista.')
            self.confirm_appoint(selected_date, horario_input)
        else:
            print(f'O horário {horario_input} não está na lista.')
            self.root.ids.marcar_consulta.ids.status.text = "Escolha um horário disponível"
    def confirm_appoint(self, dia, horario):
        horario_input = str(horario)
        local_id_func = self.local_id
        nome = self.root.ids.menu.ids.email_usuario.text
        lista_horario = horario_input.split(',')
        print(f"Horario cru: {horario}")
        print(f"Horario input: {horario_input}")
        print(f"Horario lista: {lista_horario}")
        print(f"local_id: {local_id_func}")
        print(f"nome: {nome}")
        print(f"dia: {dia}")

        link = f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/Sessoes.json"
        info_dia = f'{{"{local_id_func}": ""}}'
        req = requests.patch(link, data = info_dia)
        req_dic = req.json()

        link = f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/Sessoes/{local_id_func}.json"
        info_dia = f'{{"Nome": "{nome}", "Data": "{dia}", "Hora": "{lista_horario}"}}'
        req = requests.patch(link, data = info_dia)
        req_dic = req.json()
        print(req_dic)
        if req.ok:
            self.root.ids.marcar_consulta.ids.status.text = "Consulta marcada com sucesso"
        else:
            self.root.ids.marcar_consulta.ids.status.text = "Erro ao marcar consulta"

        print("marcado com sucesso!")
    def atualizar_horarios(self):
        string = self.root.ids.editar_horarios.ids.horarios_psico.text
        horarios = str(string)
        horarios_lista = horarios.split(',')
        print(f"horarios: {horarios_lista}")
        link = f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/Horarios.json"
        info_dia = f'{{"Horarios": "{horarios_lista}"}}'
        req = requests.patch(link, data = info_dia)
        if req.ok:
            self.root.ids.editar_horarios.ids.status.text = "Horários editados com sucesso"
        else:
            self.root.ids.editar_horarios.ids.status.text = "Erro ao editar horários"
    def carregar_horarios(self):
        link = f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/Horarios.json"
        req = requests.get(link)
        req_dic = req.json()
        horarios_banco = req_dic['Horarios']
        horarios = str(horarios_banco)
        print(horarios)
        horarios_sem_aspas = horarios.replace("'","")
        horario_final = horarios_sem_aspas.replace("[","").replace("]", "")
        self.root.ids.editar_horarios.ids.horarios_psico.text = horario_final
        self.mudar_tela("editar_horarios")
        pass
        
MainApp().run()
#comentario