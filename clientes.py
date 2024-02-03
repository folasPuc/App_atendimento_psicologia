from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Canvas, Rectangle

class Clientes(GridLayout):
    def __init__(self, **kwargs):
        super().__init__()

        nome = kwargs["email"]
        telefone = kwargs["telefone"]
        ficha = kwargs["ficha"]
        print(nome, telefone, ficha)

        esquerda = FloatLayout()
        esquerda_label = Label(text="testando", size_hint = (1, 0.2), pos_hint={"right": 1, "top": 0.2})
        esquerda.add_widget(esquerda_label)
        meio = FloatLayout()

        direita = FloatLayout()

        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)
