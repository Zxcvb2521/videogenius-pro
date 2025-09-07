@echo off
cd /d "%~dp0"
mkdocs build
echo ✅ Документация сгенерирована в папке site/
pause