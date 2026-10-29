@echo off
rem Auto‑install required Python packages and launch DTechCom Tool

rem Ensure Python is in PATH
python -V >nul 2>&1
if errorlevel 1 (
    echo Python không được tìm thấy trong PATH. Vui lòng cài đặt Python trước.
    exit /b 1
)

rem Upgrade pip và cài các phụ thuộc
python -m pip install --upgrade pip
python -m pip install customtkinter psutil

rem Chạy script Python
python "%~dp0dtechcom_tool.py"
