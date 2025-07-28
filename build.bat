@echo off
echo Instaluji zavislosti...
.\.venv\Scripts\pip.exe install -r requirements.txt

echo Kompiluji aplikaci do EXE...
.\.venv\Scripts\pyinstaller.exe ClusterAnalysis.spec

pause
