from pathlib import Path
async def getURL():
    return "https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64",(Path.home() / "Downloads" / "DiscordSetup.exe")