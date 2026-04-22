import requests
from kivy.app import App
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from PIL import Image as Imagee
from io import BytesIO
from withoutbg import WithoutBG
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.button import Button
import cv2


# barcode = "07092047636"
# url = "https://go-upc.com/search?q="
# resp = requests.get(url+barcode)

# i = '''<h2>Ingredients</h2>
#       <span>Sugar, Nonfat Milk, Modified Whey, Cocoa (Processed With Alkali), Corn Syrup, Hydrogenated Coconut Oil, Less Than 2% Of: Salt, Dipotassium Phosphate, Mono- And Diglycerides, Sodium Caseinate, Disodium Phosphate, Natural Flavor</span>
#     </div>'''

# with open("output.txt", 'w') as f:
#     f.write(resp.text[resp.text.index(u):])

class IMG(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        self.sc = None

        self.evt = Clock.schedule_interval(self.update, 1.0 / 30.0)
        
    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            print("Cam turned off")
            return

        # Convert frame to texture for Kivy
        buf = cv2.flip(frame, 0).tobytes()
        # buf = frame.tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.texture = texture



    def on_stop(self):
        # self.capture.release()
        self.evt.cancel()

class S1(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def callback(self, instance):
        self.img.on_stop()
        self.manager.current = "Sct"

    def on_enter(self, *args):
        self.layout = GridLayout(rows=2)
        super().on_enter(*args)
        self.img = IMG()
        self.img.sc = self
        self.layout.add_widget(self.img)
        self.bt = Button()
        self.bt.bind(on_press=self.callback)
        self.layout.add_widget(self.bt)
        self.add_widget(self.layout)



class S2(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def callback(self, instance):
        self.manager.current = "Sco"

    def on_enter(self, *args):
        super().on_enter(*args)

        bt = Button()
        bt.bind(on_press=self.callback)
        self.add_widget(bt)



class ape(App):

    def build(self):
        # layout = GridLayout(rows = 2)
        # layout2 = FloatLayout()

        # img = Image()
        # ur = "https://mojo.generalmills.com/api/public/content/-DsLMRztTuqaC3ODAR3eKg_gmi_hi_res_jpeg.jpeg?v=361228c7&t=1cfcc0a09ea348e0b53b953eb7705409"
        # imgresp = requests.get(url=ur)

        # model = WithoutBG.opensource()
        # # img1 = Imagee.open(BytesIO(imgresp.content)).convert("RGB")
        # img1 = model.remove_background(imgresp.content)
        # img_data = img1.tobytes()
        # texture = Texture.create(size=img1.size, colorfmt='rgba')
        # texture.blit_buffer(img_data, colorfmt='rgba', bufferfmt='ubyte')
        # img.texture = texture
        # texture.flip_vertical()

        # img.size

        # layout2.add_widget(Label(text="WHATS CRACKING"))

        # layout.add_widget(img)
        # layout.add_widget(Label(text="WHATS CRACKING"))

        # img.size_hint_y = None
        # img.height = 800
        # return layout

        sm = ScreenManager()
        sm.add_widget(S1(name="Sco"))
        sm.add_widget(S2(name="Sct"))
        
        return sm

# ur = "https://go-upc.s3.amazonaws.com/images/94904233.jpeg"
# imgresp = requests.get(url=ur)
# img1 = Imagee.open(BytesIO(imgresp.content)).convert("RGB")
# print(img1.size)

if __name__ == '__main__':
    ape().run()