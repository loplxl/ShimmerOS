from pathlib import Path
from os import getcwd
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://github.com/spddl/GoInterruptPolicy/releases/latest/download/GoInterruptPolicy.exe",(getcwd()[:2] + r"\Shimmer\Software\quickaccess\GoInterruptPolicy.exe"))