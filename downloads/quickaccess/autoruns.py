from pathlib import Path
from os import getcwd
async def getURL():
    return "https://live.sysinternals.com/autoruns.exe",(getcwd()[:2] + r"\Oslivion\OSO\quickaccess\autoruns.exe")