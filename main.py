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
    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela     
    def carregar_infos_usuario(self):
        requisicao = requests.get(f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/{self.local_id}.json")
        requisicao_dic = requisicao.json()
        # email = requisicao_dic[]



MainApp().run()
#comentario