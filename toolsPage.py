import customtkinter as ctk
from PIL import Image
from utils import resource_path
from tools import autotimerres
class toolsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master.main_area, fg_color="transparent")
        self.titleBar = ctk.CTkLabel(self, text="Tools", font=ctk.CTkFont(size=32,weight="bold"), bg_color="#1d1a23", height=50)
        self.titleBar.pack(side="top", fill="x")

        self.toolsFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.toolsFrame.pack(side="top", fill="both", expand=True)
        #auto timer res
        ATRFrame = ctk.CTkFrame(self.toolsFrame, width=500, height=220, corner_radius=20)
        ATRFrame.pack_propagate(False)  # important to keep height fixed so corners are visible
        ATRLabel = ctk.CTkLabel(ATRFrame, text="Auto Timer Resolution", pady=6, font=ctk.CTkFont(size=36,weight="bold"))
        ATRLabel.pack(side="top")
        ATRDescription = ctk.CTkLabel(ATRFrame, text="Automatically apply and benchmark multiple timer resolution values to find the one best for your hardware.\nFor accurate readings, close all other open applications.",wraplength=480,bg_color="transparent", font=ctk.CTkFont(size=19), justify="center")
        ATRDescription.pack(side="top", pady=(5,10))

        ATRBtnContainer = ctk.CTkFrame(ATRFrame, fg_color="transparent", bg_color="transparent")
        ATRApplyBtn = ctk.CTkButton(ATRBtnContainer, text="Apply", font=ctk.CTkFont(size=16), fg_color="#00aa00", hover_color="#006600", width=150, command=lambda: autotimerres.apply(self.master.master))
        ATRDefaultBtn = ctk.CTkButton(ATRBtnContainer, text="Default", font=ctk.CTkFont(size=16) , fg_color="#aa0000", hover_color="#660000", width=150, command=lambda: autotimerres.default(self.master.master))

        ATRApplyBtn.grid(row=0, column=0, padx=50, pady=10)
        ATRDefaultBtn.grid(row=0, column=1, padx=50, pady=10)

        ATRBtnContainer.grid_columnconfigure(0, weight=1)
        ATRBtnContainer.pack(side="top")

        ATRFrame.rowconfigure(0, weight=1)
        self.frames = [ATRFrame]
        r=0
        c=0
        for frame in self.frames:
            frame.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)
            c += 1
            if c > 1:
                c = 0
                r += 1
