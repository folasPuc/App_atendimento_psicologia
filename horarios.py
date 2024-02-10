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
class Horarios(GridLayout):
    def __init__(self, **kwargs):
        self.rows = 1
        super().__init__()
        hora = kwargs["horarios"]
        print(f"print hora dentro do arquivo horarios.py: {hora}")


        esquerda = FloatLayout()
        esquerda_label = Label(text=hora, size_hint = (1, 0.2), pos_hint={"right": 1, "top": 0.2})
        esquerda.add_widget(esquerda_label)
        self.add_widget(esquerda)