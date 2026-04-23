#I preface all this with I AM NOT USING BEAUTIFULSOUP. We have beef from a prevous project

import cv2
from pyzbar.pyzbar import decode, ZBarSymbol

import requests
from PIL import Image as Imagee
from io import BytesIO
from withoutbg import WithoutBG

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition



class BarcodeScanner(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        self.texture = None
        self.screen = None

        # Run update 30 times per second
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


        # Decode barcodes
        barcodes = decode(frame,
         symbols=[
             ZBarSymbol.EAN13, 
             ZBarSymbol.EAN8, 
             ZBarSymbol.CODE128,
             ZBarSymbol.UPCA])

        #add this to a new function
        for barcode in barcodes:
            x, y, w, h = barcode.rect
            global CODE # Made global so it can be accessed in other screens
            CODE = barcode.data.decode("utf-8")

            # # Draw rectangle
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # # Draw text
            # cv2.putText(frame, data, (x, y - 10),
            #             cv2.FONT_HERSHEY_SIMPLEX,
            #             0.6, (0, 255, 0), 2)

            print("Detected:", CODE)
            self.on_stop()
            

#make a request to get ingredients of barcode and display whether hemp or no hemp

    def on_stop(self):
        self.evt.cancel()
        self.capture.release()
        self.screen.manager.current = "Info_Screen"

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.scanner = BarcodeScanner()
        self.scanner.screen = self
        self.add_widget(self.scanner)

class InfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.waiting = Label(text="Go meditate or something")
        self.diagnosis = Label()
        self.img = Image()
        self.hashemp = False
        self.options = {False: "No hemp here mate", True: "FAHHHH this shi got hemp"}

    def _imagify(self, content):
        
        #Grab image url for later display
        istart = content.text.index('img src="')+9
        iend = content.text[istart:].index("jpeg")+4+istart
        iurl = content.text[istart:iend]
        imgresp = requests.get(url=iurl)

        #Remove background and transform to kivy texture
        # img = Imagee.open(BytesIO(imgresp.content))
        model = WithoutBG.opensource()
        img = model.remove_background(imgresp)
        texture = Texture.create(size=img.size, colorfmt='rgba')
        texture.blit_buffer(imgresp.content, colorfmt='rgba', bufferfmt='ubyte')
        self.img.texture = texture


    def _get_info(self):
        ur = "https://go-upc.com/search?q="+CODE
        resp = requests.get(url=ur)

        # if 

        #grab ingredients
        u = '''<h2>Ingredients</h2>
      <span>'''
        start = resp.text.index(u) + 33
        end = resp.text[start:].index("</span>") + start
        ingredients = resp.text[start:end]

        self._imagify(ur)

        if "hemp" in ingredients:
            self.hashemp = True
            
    
    def on_pre_enter(self, *args):
        #Retrieve thte image and ingredient information before screen loads
        super().on_pre_enter(*args)
        self._get_info()
        self.diagnosis.text = self.options[self.hashemp]

    def on_enter(self):
        # self.add_widget(self.waiting)
        # self._get_info()
        # self.remove_widget(self.waiting)
        self.add_widget(self.img)
        self.add_widget(self.diagnosis)
    


class ScannerApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(CameraScreen(name="Cam_Screen"))
        sm.add_widget(InfoScreen(name="Info_Screen"))
        return sm
 

if __name__ == "__main__":
    ScannerApp().run()