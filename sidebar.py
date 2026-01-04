import customtkinter as ctk
from PIL import Image
from utils import resource_path
class sidebar(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master=master,fg_color="#27242d")
        self.icon = ctk.CTkLabel(
            self,
            image=ctk.CTkImage(
                dark_image=Image.open(resource_path("icon.png")),
                size=(128,128)),
            text=""
        )
        self.pack_propagate(False)
        self.icon.pack(side="top", anchor="n", pady=20)
        
        #create buttons
        homeButton = ctk.CTkButton(self, text="Home", command=master.homePage_init, fg_color="#1f1c25", hover_color="#23202b", font=ctk.CTkFont(size=24),height=45)
        downloadsButton = ctk.CTkButton(self, text="Downloads", command=master.downloadsPage_init, fg_color="#1f1c25", hover_color="#23202b", font=ctk.CTkFont(size=24),height=45)
        tweaksButton = ctk.CTkButton(self, text="Tweaks", command=master.tweaksPage_init, fg_color="#1f1c25", hover_color="#23202b", font=ctk.CTkFont(size=24),height=45)
        toolsButton = ctk.CTkButton(self, text="Tools", command=master.toolsPage_init, fg_color="#1f1c25", hover_color="#23202b", font=ctk.CTkFont(size=24),height=45)
        aboutButton = ctk.CTkButton(self, text="About", command=master.aboutPage_init, fg_color="#1f1c25", hover_color="#23202b", font=ctk.CTkFont(size=24),height=45)
        
        
        homeButton.pack(side="top", anchor="n", padx=5, pady=3, fill='x')
        downloadsButton.pack(side="top", anchor="n", padx=5, pady=3, fill='x')
        tweaksButton.pack(side="top", anchor="n", padx=5, pady=3, fill='x')
        toolsButton.pack(side="top", anchor="n", padx=5, pady=3, fill='x')
        aboutButton.pack(side="top", anchor="n", padx=5, pady=3, fill='x')
