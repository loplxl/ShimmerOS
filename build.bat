pyinstaller --noconfirm --onedir --windowed --icon="assets\icon.ico" --add-data "assets;assets" --add-data "TimerResolution;TimerResolution" --add-data "downloads;downloads" --add-data "tools;tools" --add-data "dependencies;dependencies" --hidden-import bs4 --hidden-import win32com main.py --name Shimmer --noconfirm
timeout /t 1 /nobreak >nul
powershell -Command Compress-Archive -Path .\dist\Shimmer -DestinationPath .\dist\Shimmer.zip -Update

pause