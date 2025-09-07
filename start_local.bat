@echo off
cd /d "C:\Users\Evgenyi\Desktop\VideoGenius AI Agent\VideoGenius PRO"
echo Активируем виртуальное окружение...
call .venv\Scripts\activate
echo Запускаем приложение...
python app.py
pause