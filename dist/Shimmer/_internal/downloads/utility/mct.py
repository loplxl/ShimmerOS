from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://www.igorslab.de/installer/MoreClockTool_v1111_2.zip",Path.home() / "Downloads" / "MoreClockTool_v1111_2.zip")
#very hard to extract latest version, if anyone can help make a pull request, thanks :D