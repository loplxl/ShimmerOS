from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://download.asrock.com/Utility/Formula/TimingConfigurator(v4.1.7).zip",(Path.home() / "Downloads" / "TimingConfigurator(v4.1.7).zip"))