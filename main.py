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
            self.mudar_tela("menu")
        except:
            pass
        



MainApp().run()
#comentario