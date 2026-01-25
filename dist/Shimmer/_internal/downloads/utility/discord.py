from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64",(Path.home() / "Downloads" / "DiscordSetup.exe"))