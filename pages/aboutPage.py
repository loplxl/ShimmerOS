import customtkinter as ctk
from PIL import Image
from utils import resource_path
from webbrowser import open as openLink
class aboutPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master.main_area, fg_color="transparent")
        self.aboutPage_image = ctk.CTkLabel(self,image=ctk.CTkImage(
                dark_image=Image.open(resource_path("about.png")),
                size=(900,315)),text="")
        self.aboutPage_image.pack(side="top", pady=(20,0))

        self.LinksTitle = ctk.CTkLabel(self, text="Links", font=ctk.CTkFont(size=28))
        self.LinksTitle.pack(side="top", pady=(9,4))

        #Github Link
        self.OSOGHFrame = ctk.CTkFrame(self, fg_color="transparent")

        self.GHNameLabel = ctk.CTkLabel(self.OSOGHFrame, text="GitHub:", font=ctk.CTkFont(size=16))
        self.GHLinkLabel = ctk.CTkLabel(self.OSOGHFrame, text="github.com/loplxl/OSlivionOptions",
            font=ctk.CTkFont(size=16), cursor="hand2", text_color="#0000ff")

        self.GHNameLabel.pack(side="left", padx=(0,10))
        self.GHLinkLabel.pack(side="left")

        self.GHLinkLabel.bind("<Enter>", lambda e: e.widget.master.configure(text_color="#0000aa"))
        self.GHLinkLabel.bind("<Leave>", lambda e: e.widget.master.configure(text_color="#0000ff"))
        self.GHLinkLabel.bind("<Button-1>", lambda e: openLink("https://github.com/loplxl/OSlivionOptions"))
        self.OSOGHFrame.pack(side="top", pady=(8,0))


        #Discord Link
        self.DCFrame = ctk.CTkFrame(self, fg_color="transparent")

        self.DCNameLabel = ctk.CTkLabel(self.DCFrame, text="Discord:", font=ctk.CTkFont(size=16))
        self.DCLinkLabel = ctk.CTkLabel(self.DCFrame, text="discord.gg/CSJfvagRbt",
            font=ctk.CTkFont(size=16), cursor="hand2", text_color="#0000ff")

        self.DCNameLabel.pack(side="left", padx=(0,10))
        self.DCLinkLabel.pack(side="left")

        self.DCLinkLabel.bind("<Enter>", lambda e: e.widget.master.configure(text_color="#0000aa"))
        self.DCLinkLabel.bind("<Leave>", lambda e: e.widget.master.configure(text_color="#0000ff"))
        self.DCLinkLabel.bind("<Button-1>", lambda e: openLink("https://discord.gg/CSJfvagRbt"))
        self.DCFrame.pack(side="top", pady=(5,0))

        self.creditsTitle = ctk.CTkLabel(self, text="Credits", font=ctk.CTkFont(size=28))
        self.creditsTitle.pack(side="top", pady=(15,4))

        self.creditsLabel1 = ctk.CTkLabel(self, text="Hickensa (SapphireOS/Tool) for being the main inspiration for uchr's development of OSlivion, and my development of this tool.", font=ctk.CTkFont(size=16), cursor="hand2")
        self.creditsLabel1.bind("<Button-1>", lambda e: openLink("https://github.com/HickerDicker"))
        self.creditsLabel1.pack(side="top", pady=(8,0))

        self.creditsLabel2 = ctk.CTkLabel(self, text="Chr for making OSlivion!!", font=ctk.CTkFont(size=16), cursor="hand2")
        self.creditsLabel2.bind("<Button-1>", lambda e: openLink("https://github.com/u2chr2"))
        self.creditsLabel2.pack(side="top", pady=(2,0))


