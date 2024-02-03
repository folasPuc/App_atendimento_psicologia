from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from myfirebase import MyFirebase
import requests

import unicodedata
# coding: utf-8

class LoginPage(Screen):
    pass
class Menu(Screen):
    pass
class MenuAdmin(Screen):
    pass
class TodosPacientes(Screen):
    pass
class LabelButton(ButtonBehavior,Label ):
    pass
class ImageButton(ButtonBehavior,Image ):
    pass
    
GUI= Builder.load_file('main.kv')


class MainApp(App):
    def build(self):
        self.myfirebase = MyFirebase()
        return GUI
    
    def on_start(self):
        self.carregar_infos_usuario()   
    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela  
    def carregar_infos_usuario(self):
        try:
            with open("refreshtoken.txt", "r") as arquivo:
                refresh_token = arquivo.read()
            local_id, id_token = self.myfirebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token
            requisicao = requests.get(f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/{self.local_id}.json")
            requisicao_dic = requisicao.json()
            email = requisicao_dic["email"]
            telefone = requisicao_dic["telefone"]
            email_user = self.root.ids.menu.ids.email_usuario.text = "[b]Email:[/b] {}".format(email)
            tel_user = self.root.ids.menu.ids.telefone_usuario.text = "[b]Telefone:[/b] {}".format(telefone)
            if email == "admin@gmail.com":
                email_user = self.root.ids.menuadmin.ids.email_usuario.text = "[b]Email:[/b] {}".format(email)
                tel_user = self.root.ids.menuadmin.ids.telefone_usuario.text = "[b]Telefone:[/b] {}".format(telefone)
                self.mudar_tela("menuadmin")
            else:
                email_user = self.root.ids.menu.ids.email_usuario.text = "[b]Email:[/b] {}".format(email)
                tel_user = self.root.ids.menu.ids.telefone_usuario.text = "[b]Telefone:[/b] {}".format(telefone)
                self.mudar_tela("menu")
        except:
            pass
    def carregar_pacientes(self):
        link = f'https://app-psicologia-66b64-default-rtdb.firebaseio.com/.json?orderBy="email"'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        for local_id_usuario in requisicao_dic:
            email_usuario = requisicao_dic[local_id_usuario].get('email')
            telefone_usuario = requisicao_dic[local_id_usuario].get('telefone')
            print(email_usuario, telefone_usuario)

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

MainApp().run()
#comentario