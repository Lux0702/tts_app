@echo off
title Ung Dung Chuyen Van Ban Thanh Giong Noi AI
cd /d "%~dp0"
echo =======================================================
echo   UNG DUNG DOC VAN BAN THANH GIONG NOI AI (TTS)
echo   100%% Mien phi - Khong gioi han ky tu - Xuat MP3
echo =======================================================
echo.
echo Dang khoi dong ung dung...
echo Vui long doi trong giay lat, trinh duyet web se tu dong mo len.
echo.
python -m streamlit run app.py
pause
