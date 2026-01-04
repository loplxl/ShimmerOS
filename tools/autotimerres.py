import customtkinter as ctk
from tkinter import StringVar
from os.path import join
from os import environ,system,startfile
from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE, CREATE_NO_WINDOW
import threading
import re
from time import sleep, time

running = False


def apply(self):
    self.stop = threading.Event()
    createnewtl = False
    try:
        if not self.ATRtoplevel.winfo_exists():
            createnewtl = True
    except Exception:
        createnewtl = True
    if createnewtl:
        self.ATRtoplevel = ctk.CTkToplevel(self, fg_color="#201d26")
        self.ATRtoplevel.geometry("600x200")
        self.ATRtoplevel.title("Apply Timer Resolution")

        #create a frame to hold entries, then pack the frame and submit button
        minres = StringVar(value=5000)
        maxres = StringVar(value=5100)
        interval = StringVar(value=5)
        samples = StringVar(value=50)


        self.varsFrame = ctk.CTkFrame(self.ATRtoplevel, fg_color="#201d26")


        minresFrame = ctk.CTkFrame(self.varsFrame, fg_color="transparent", width=120)
        minresLabel = ctk.CTkLabel(minresFrame, text="Minimum Resolution")
        minresEntry = ctk.CTkEntry(minresFrame, textvariable=minres, justify="center")

        minresLabel.pack()
        minresEntry.pack()
        minresFrame.grid(row=0,column=0)

        
        maxresFrame = ctk.CTkFrame(self.varsFrame, fg_color="transparent", width=120)
        maxresLabel = ctk.CTkLabel(maxresFrame, text="Maximum Resolution")
        maxresEntry = ctk.CTkEntry(maxresFrame, textvariable=maxres, justify="center")

        maxresLabel.pack()
        maxresEntry.pack()
        maxresFrame.grid(row=0,column=1)


        intervalFrame = ctk.CTkFrame(self.varsFrame, fg_color="transparent", width=120)
        intervalLabel = ctk.CTkLabel(intervalFrame, text="Interval")
        intervalEntry = ctk.CTkEntry(intervalFrame, textvariable=interval, justify="center")

        intervalLabel.pack()
        intervalEntry.pack()
        intervalFrame.grid(row=0,column=2)


        samplesFrame = ctk.CTkFrame(self.varsFrame, fg_color="transparent", width=120)
        samplesLabel = ctk.CTkLabel(samplesFrame, text="Samples")
        samplesEntry = ctk.CTkEntry(samplesFrame, textvariable=samples, justify="center")

        samplesLabel.pack()
        samplesEntry.pack()
        samplesFrame.grid(row=0,column=3)

        
        for i in range(4):
            self.varsFrame.grid_columnconfigure(i, weight=1, uniform="col")
        self.varsFrame.pack(side="top", pady=(10,0), fill="x")


        self.statusLabel = ctk.CTkLabel(self.ATRtoplevel, text="", font=ctk.CTkFont(size=24))
        self.statusLabel.pack(side="top", pady=(10,0))

        
        self.confirmBtn = ctk.CTkButton(self.ATRtoplevel, text="Confirm", font=ctk.CTkFont(size=20), fg_color="#1a1720", hover_color="#16131c")
        self.timerresthread = threading.Thread(target=confirm, args=(minres, maxres, interval, samples, self.confirmBtn, self.statusLabel), daemon=True)
        self.confirmBtn.configure(command=lambda: parseAndStart(minres,maxres,interval,samples,self.confirmBtn))

        self.confirmBtn.pack(side="top", pady=(10,0))

        threading.Thread(target=heartbeat,args=(self.ATRtoplevel,self.timerresthread), daemon=True).start()
    self.ATRtoplevel.attributes("-topmost", True)
    self.ATRtoplevel.after(10,lambda: self.ATRtoplevel.attributes("-topmost", False))
    

TRES_DIR = r"C:\PostInstall\TimerResolution"
lastres = 5000
bestdelta = 1000
bestres = -1
def confirm(minres,maxres,interval,samples,btn,label):
    global bestres
    global bestdelta
    global lastres
    label.configure(text="Waiting for stress test to load...")
    startfile(join(TRES_DIR,"stress.exe"))
    beforetime = time()
    while time() - beforetime < 0.1:
        pass
    cmd = f"{join(TRES_DIR,"timerres.exe")} --minRes {minres.get()} --maxRes {maxres.get()} --interval {interval.get()} --samples {samples.get()}"
    process = Popen(cmd.split(" "),creationflags=CREATE_NO_WINDOW,stdout=PIPE,text=True)
    for line in process.stdout:

        if btn.master.master.stop.is_set(): #toplevel is gone
            break
        
        line = line.strip()
        print(line)
        if line.startswith("Benchmarking: "):
            label.configure(text=f"{line}{f"\nBest: {bestres} (delta: {bestdelta})" if bestres != -1 else ""}")
            lastres = line[14:]
        elif "<" in line:
            bestdelta = line.split(" ",1)[0]
            bestres = lastres
        elif re.search(r"^\d+$",line):
            label.configure(text=f"Benchmark complete\nApplying resolution {bestres} (delta: {bestdelta})")
            apps = ["stress","MeasureSleep","SetTimerResolution"]
            for app in apps:
                Popen(["taskkill","/f","/im",f"{app}.exe"],creationflags=CREATE_NO_WINDOW)

            #save settimerres shortcut to startup folder
            import win32com.client as cli
            shortcut_location = join(environ["APPDATA"],r"Microsoft\Windows\Start Menu\Programs\Startup",f"SetTimerResolution.lnk")
            shell = cli.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_location)
            shortcut.Targetpath = "C:\\PostInstall\\TimerResolution\\SetTimerResolution.exe"
            shortcut.Arguments = f"--no-console --resolution {bestres}"
            shortcut.save()


            sleep(0.5)
            #Popen(
            #    [
            #        "start",'""',"/b",r"C:/PostInstall/TimerResolution/SetTimerResolution.exe","--no-console","--resolution",bestres
            #    ] #command of 2 hours of pain PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK PLEASE WORK
            #    ,creationflags=CREATE_NO_WINDOW)
            #if youre seeing this tell me why this doesnt work ^ please plase paslepaslepaslepsalesaleap i tried \ instead of /
            system(r'start "" /b C:/PostInstall/TimerResolution/SetTimerResolution.exe --no-console --resolution ' + str(bestres))
            label.configure(text=f"Tool execution complete, added startup task:\nResolution: {bestres} Delta: {bestdelta}")
    

def error(btn,msg):
    btn.configure(text=msg)
    btn.master.after(1500, lambda: btn.configure(text="Confirm"))

def heartbeat(toplevel: ctk.CTkToplevel, thread: threading.Thread):
    while True:
        try:
            if not toplevel.winfo_exists():
                toplevel.master.stop.set()
            else:
                sleep(0.5)
        except RuntimeError:
            pass

def parseAndStart(minres,maxres,interval,samples,btn):
    try:
        int(minres.get())
        int(maxres.get())
        int(interval.get())
        int(samples.get())
    except Exception:
        error(btn,"Integers only.")
        return
    btn.destroy()
    btn.master.master.timerresthread.start()