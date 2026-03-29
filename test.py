from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.camera import Camera

class Cam(Camera):
    def __init__(self, **kwargs):
        # super().__init__(**kwargs)
        self.play = True
    
# class lab(Label):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.text = "HALLO"

class MyApp(App):

    def build(self):
        return Cam()
    

if __name__ == '__main__':
    MyApp().run()