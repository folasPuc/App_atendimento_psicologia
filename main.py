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
from kivy.core.window import Window
from kivymd.app import ThemeManager
from kivymd.app import MDApp
import subprocess
import requests
import unicodedata


# coding: utf-8
Window.size = (350,580)

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
    def run_calendar(self):
        subprocess.Popen(['Python', "Calendario.py"])
        local_id = self.local_id
        with open("local_id.txt", "w") as arquivo:
            arquivo.write(local_id)
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
            email_user = self.root.ids.menu.ids.email_usuario.text = "[b]Email:[/b] {}".format(nome)
            tel_user = self.root.ids.menu.ids.telefone_usuario.text = "[b]Telefone:[/b] {}".format(telefone)
            if email == "adminpsico1@gmail.com":
                email_user = self.root.ids.menuadmin.ids.email_usuario.text = "[b]Email:[/b] {}".format(nome)
                tel_user = self.root.ids.menuadmin.ids.telefone_usuario.text = "[b]Telefone:[/b] {}".format(telefone)
                self.alterar_informacao(nome)
                self.mudar_tela("menuadmin")
            else:
                email_user = self.root.ids.menu.ids.email_usuario.text = "[b]Email:[/b] {}".format(nome)
                tel_user = self.root.ids.menu.ids.telefone_usuario.text = "[b]Telefone:[/b] {}".format(telefone)
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


MainApp().run()
#comentario