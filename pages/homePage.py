import customtkinter as ctk
from PIL import Image
from utils import resource_path
class homePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master.main_area, fg_color="transparent")
        self.homePage_image = ctk.CTkLabel(
            self,image=ctk.CTkImage(
                dark_image=Image.open(resource_path("options.png")),
                size=(900,315)),text="")
        self.homePage_label = ctk.CTkLabel(self, text="Welcome to OSlivion Options!\nHere you can get software downloads, tweak management and maybe more in the future.\n\nThanks for using OSlivion and if you run into any issues, please contact us on GitHub.\nMore info on the about page.",
            font=ctk.CTkFont(size=23))
        self.homePage_image.pack(side="top", pady=(20,14))
        self.homePage_label.pack(side="top")