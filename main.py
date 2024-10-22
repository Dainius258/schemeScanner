from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.core.window import Window

KV = '''
MDScreen:
    md_bg_color: app.theme_cls.surfaceColor

    MDButton:
        style: "tonal"
        pos_hint: {"center_x": .2, "center_y": .1}
        on_release: app.exit_app()
        MDButtonText:
            text: "Exit"

    MDIconButton:
        icon: "camera-outline"
        style: "tonal"
        pos_hint: {"center_x": .5, "center_y": .1}
        theme_font_size: "Custom"
        font_size: "48sp"
        radius: [self.height / 2, ]
        size_hint: None, None
        size: "84dp", "84dp"
        on_release: app.capture_image()

    MDButton:
        style: "tonal"
        pos_hint: {"center_x": .8, "center_y": .1}
        on_release: app.upload_picture()
        MDButtonText:
            text: "Upload picture"

    Camera:
        id: camera
        resolution: (640, 480)
        play: True
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint: 0.8, 0.6
'''

class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_string(KV)

    def exit_app(self):
        MDApp.get_running_app().stop()
        Window.close()

    def capture_image(self):
        camera = self.root.ids.camera
        camera.export_to_png("captured_image.png")
        print("Image captured and saved as captured_image.png")

    def upload_picture(self):
        print("Upload picture functionality not implemented yet")

Example().run()