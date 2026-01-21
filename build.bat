pyinstaller --noconfirm --onedir --windowed --icon=icon.ico --add-data "about.png;." --add-data "options.png;." --add-data "icon.png;." --add-data "TimerResolution;TimerResolution" --add-data "downloads;downloads" --add-data "dependencies;dependencies" --hidden-import bs4 main.py --name OSO --noconfirm
timeout /t 1 /nobreak >nul
powershell -Command Compress-Archive -Path .\dist\OSO -DestinationPath .\dist\OSO.zip -Update

pause