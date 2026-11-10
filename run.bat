@echo off
echo python src/main.py %*
python src/main.py %*
exit /b %errorlevel%