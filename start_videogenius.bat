@echo off
cd /d "C:\Users\Evgenyi\Desktop\VideoGenius AI Agent\VideoGenius PRO"
echo Запускаем VideoGenius PRO...
echo.
docker run -it --rm -p 7860:7860 --env-file .env videogenius-pro
pause