import customtkinter as ctk
from tkinter import StringVar
from os.path import join, exists
from os import environ, system, remove
from subprocess import Popen, PIPE, CREATE_NO_WINDOW, DETACHED_PROCESS, CREATE_NEW_PROCESS_GROUP, HIGH_PRIORITY_CLASS
import threading
from random import randint
import re
from time import sleep, time
from utils import resource_path

lastres = 5000
bestdelta = 1000
bestres = -1
import ctypes
def handleNtSetTimerResolution(minres,maxres,interval,samples,label,stress):
    global bestdelta
    global lastres
    global bestres
    try:
        Popen(["taskkill","/f","/im","SetTimerResolution.exe"],creationflags=CREATE_NO_WINDOW)
        ntdll = ctypes.WinDLL("ntdll")
        NtSetTimerResolution = ntdll.NtSetTimerResolution
        NtSetTimerResolution.argtypes = [ctypes.wintypes.ULONG,ctypes.wintypes.BOOLEAN,ctypes.POINTER(ctypes.wintypes.ULONG)]

        bestlabel = ctk.CTkLabel(label.master, fg_color="transparent", text="")
        bestlabel.seed = randint(0,5000)
        bestlabel.pack()
        lastiterationseed = -1
        for res in range(minres,maxres+1,interval):
            lastiterationseed = bestlabel.seed
            if not label.master.winfo_exists(): #toplevel is gone
                return
            NtSetTimerResolution(res, True, ctypes.wintypes.ULONG())
            label.configure(text=f"Benchmarking: {res}")
            with Popen((resource_path("TimerResolution\\MeasureSleep").split(" ") + ["--samples",samples]),stdout=PIPE,text=True,creationflags=CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS | HIGH_PRIORITY_CLASS) as MeasureSleep:
                label.master.master.openSubprocesses.append(MeasureSleep)
                output = MeasureSleep.stdout.read()
                label.master.master.openSubprocesses.remove(MeasureSleep)
            print(output)
            match = re.search(r"Max: (\d+\.\d+)",output)
            if match:
                max = float(match.group(1))
                if max < bestdelta:
                    bestdelta = max
                    bestres = res
            if not label.master.winfo_exists(): #toplevel is gone
                if lastiterationseed != bestlabel.seed: #closing and reopening toplevel during measuresleep can give inaccurate results, this is here to prevent that.
                    return
            bestlabel.configure(text=f"Best: {bestres} {bestdelta}")
        stress.terminate()
        label.configure(text="Done, trying to apply...")
        saveTRESShortcut(bestres)
        label.after(500)
        label.configure(text=("Successfully applied!" if exists(shortcut_location) else f"Failed, manually apply {bestres}. Guide in Discord."))
        bestlabel.destroy()
        NtSetTimerResolution(0, False, ctypes.wintypes.ULONG()) #disable temporary timer res
        system(f'"{shortcut_location}"') #must be system so that the settimerres exe stays open after closing shimmer
    except Exception as e:
        print(f"unexpected error during timer res\n{str(e)}")
        stress.terminate()



import win32com.client as cli
import pythoncom
shortcut_location = join(environ["APPDATA"],r"Microsoft\Windows\Start Menu\Programs\Startup",f"SetTimerResolution.exe.lnk")
def saveTRESShortcut(bestres):
    pythoncom.CoInitialize()
    global shortcut_location
    shell = cli.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_location)
    shortcut.Targetpath = resource_path("TimerResolution\\SetTimerResolution.exe")
    shortcut.Arguments = f"--no-console --resolution {bestres}"
    shortcut.save()
    pythoncom.CoUninitialize()

def default(self,btn):
    global shortcut_location
    if exists(shortcut_location):
        remove(shortcut_location)
    btn.configure(text="Applied.")
    Popen(["taskkill","/f","/im","SetTimerResolution.exe"],creationflags=CREATE_NO_WINDOW)
    btn.master.after(1500, lambda: btn.configure(text="Confirm"))



running = False

def on_close(self):
    print("close atrtoplevel")
    self.stop.set()
    self.ATRtoplevel.destroy()
    for process in self.openSubprocesses:
        print(f"Terminating {process}")
        process.terminate()

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
        self.ATRtoplevel.protocol("WM_DELETE_WINDOW", lambda: on_close(self))
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


        statusLabel = ctk.CTkLabel(self.ATRtoplevel, text="", font=ctk.CTkFont(size=24))
        statusLabel.pack(side="top", pady=(10,0))

        
        self.confirmBtn = ctk.CTkButton(self.ATRtoplevel, text="Confirm", font=ctk.CTkFont(size=20), fg_color="#1a1720", hover_color="#16131c")
        self.timerresthread = threading.Thread(target=confirm, args=(minres, maxres, interval, samples, self.confirmBtn, statusLabel), daemon=True)
        self.confirmBtn.configure(command=lambda: parseAndStart(minres,maxres,interval,samples,self.confirmBtn))

        self.confirmBtn.pack(side="top", pady=(10,0))

        threading.Thread(target=heartbeat,args=(self.ATRtoplevel,self.stop), daemon=True).start()
    self.ATRtoplevel.attributes("-topmost", True)
    self.ATRtoplevel.after(10,lambda: self.ATRtoplevel.attributes("-topmost", False))
    

TRES_DIR = r"TimerResolution"


def confirm(minres,maxres,interval,samples,btn,label):
    with Popen(resource_path("TimerResolution\\stress").split(" "),creationflags=CREATE_NO_WINDOW) as stresstest:
        label.master.master.openSubprocesses.append(stresstest)
        label.configure(text="Loading...")
        beforetime = time()
        while time() - beforetime < 1: #wait 1s for stress test
            pass
        
        threading.Thread(target=handleNtSetTimerResolution,args=(int(minres.get()),int(maxres.get()),int(interval.get()),samples.get(),label,stresstest), daemon=True).start()

def error(btn,msg):
    btn.configure(text=msg)
    btn.master.after(1500, lambda: btn.configure(text="Confirm"))

def heartbeat(toplevel: ctk.CTkToplevel, stopflag):
    while True:
        #print("heartbeat") #for debugging
        try:
            if not toplevel.winfo_exists():
                stopflag.set()
                break
            else:
                sleep(0.5)
        except RuntimeError as e:
            print(e)
            stopflag.set()
            break

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
