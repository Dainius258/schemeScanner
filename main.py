from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.camera import Camera
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from ultralytics import YOLO
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.filemanager import MDFileManager
import os
from datetime import datetime

KV = '''
MDScreen:
    md_bg_color: app.theme_cls.surfaceColor
    
    MDBoxLayout:
        orientation: 'vertical'
        spacing: "10dp"
        padding: "10dp"
        
        RelativeLayout:
            id: preview_box
            size_hint_y: 0.7
            
            Camera:
                id: camera
                resolution: (640, 480)
                play: True
                size_hint: 1, 1
            
            Image:
                id: preview_image
                size_hint: 1, 1
                opacity: 0
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        MDLabel:
            id: status_label
            text: ""
            halign: "center"
            size_hint_y: 0.1
            theme_text_color: "Secondary"
            
        MDBoxLayout:
            size_hint_y: 0.2
            spacing: "10dp"
            padding: "10dp"
            
            # Added flexible space on the left
            Widget:
                size_hint_x: 1
            
            MDButton:
                style: "tonal"
                size_hint_x: None
                width: "100dp"
                on_release: app.exit_app()
                MDButtonText:
                    text: "Exit"
            
            MDIconButton:
                icon: "camera-outline"
                style: "tonal"
                theme_font_size: "Custom"
                font_size: "48sp"
                radius: [self.height / 2, ]
                size_hint: None, None
                size: "84dp", "84dp"
                pos_hint: {"center_y": .5}
                on_release: app.capture_image()
            
            MDButton:
                style: "tonal"
                size_hint_x: None
                width: "100dp"
                on_release: app.upload_picture()
                MDButtonText:
                    text: "Upload"
            
            # Added flexible space on the right
            Widget:
                size_hint_x: 1
'''

class ObjectDetectionApp(MDApp):
    status_message = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the YOLO model
        self.model = YOLO("models/22.10.onnx")
        self.file_manager = None
        self.current_image_path = None
    
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_path,
        )
        return Builder.load_string(KV)
    
    def show_status(self, message):
        """Display a status message and clear it after 3 seconds"""
        self.root.ids.status_label.text = message
        Clock.schedule_once(lambda dt: self.clear_status(), 3)
    
    def clear_status(self):
        """Clear the status message"""
        self.root.ids.status_label.text = ""
    
    def exit_app(self):
        MDApp.get_running_app().stop()
        Window.close()
    
    def capture_image(self):
        camera = self.root.ids.camera
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_image_path = f"captured_image_{timestamp}.png"
        camera.export_to_png(self.current_image_path)
        self.show_status("Image captured!")
        self.process_image(self.current_image_path)
    
    def upload_picture(self):
        self.file_manager.show('/')
    
    def select_path(self, path):
        self.exit_file_manager()
        self.current_image_path = path
        self.show_status("Image selected!")
        self.process_image(path)
    
    def exit_file_manager(self, *args):
        self.file_manager.close()
    
    def process_image(self, image_path):
        try:
            # Run inference
            results = self.model(image_path)
            
            # Save the result
            result_path = f"result_{os.path.basename(image_path)}"
            results[0].save(result_path)
            
            # Update the preview
            preview = self.root.ids.preview_image
            camera = self.root.ids.camera
            
            # Hide camera, show result
            camera.opacity = 0
            preview.source = result_path
            preview.opacity = 1
            
            # Show success message
            self.show_status(f"Detection completed! Saved as {result_path}")
            
            # Schedule return to camera view
            Clock.schedule_once(self.return_to_camera, 3)
            
        except Exception as e:
            self.show_status(f"Error processing image: {str(e)}")
    
    def return_to_camera(self, dt):
        camera = self.root.ids.camera
        preview = self.root.ids.preview_image
        
        # Hide result, show camera
        preview.opacity = 0
        camera.opacity = 1

if __name__ == "__main__":
    ObjectDetectionApp().run()