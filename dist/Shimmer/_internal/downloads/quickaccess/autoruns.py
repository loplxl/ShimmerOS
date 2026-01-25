from pathlib import Path
from os import getcwd
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://live.sysinternals.com/autoruns.exe",(getcwd()[:2] + r"\Shimmer\Software\quickaccess\autoruns.exe"))