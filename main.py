from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image

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
        return GUI
    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela    



MainApp().run()
#comentario