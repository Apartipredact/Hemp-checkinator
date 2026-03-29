import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture


class BarcodeScanner(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)

        # Run update 30 times per second
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            print("false")
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

        
        for barcode in barcodes:
            x, y, w, h = barcode.rect
            data = barcode.data.decode("utf-8")

            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Draw text
            cv2.putText(frame, data, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)

            print("Detected:", data)


    def on_stop(self):
        self.capture.release()


class ScannerApp(App):
    def build(self):
        return BarcodeScanner()


if __name__ == "__main__":
    ScannerApp().run()