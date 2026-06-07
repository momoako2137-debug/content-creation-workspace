@echo off
chcp 65001 > nul
cd /d %~dp0
echo 個別相談カルテアプリを起動中...
pip install -r requirements.txt -q
python app.py
pause
