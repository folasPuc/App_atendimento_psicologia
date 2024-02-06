from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import ButtonBehavior
from kivy.graphics import Canvas, Rectangle


class LabelButton(ButtonBehavior, Label):
    pass
class ImageButton(ButtonBehavior, Image):
    pass
class Sessoes(GridLayout):
    def __init__(self, **kwargs):
        self.rows = 1
        super().__init__()
        nome = kwargs["Nome"]
        data = kwargs["Data"]
        hora = kwargs["Hora"]
        print(nome, data, hora)

        esquerda = FloatLayout()
        esquerda_label = Label(text=nome, size_hint = (1, 0.2), pos_hint={"right": 1, "top": 0.2})
        esquerda.add_widget(esquerda_label)
        meio = FloatLayout()
        meio_label = Label(text=data, size_hint = (1, 0.2), pos_hint={"right": 1, "top": 0.2})
        meio.add_widget(meio_label)
        direita = FloatLayout()
        direita_label = Label(text=hora, size_hint = (1, 0.2), pos_hint={"right": 1, "top": 0.2})
        direita.add_widget(direita_label)
        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)
