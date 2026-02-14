@echo off
chcp 65001 > nul
echo ============================================================
echo          重启工具管理器 - 清理所有旧进程
echo ============================================================
echo.

echo [1/3] 正在停止所有Python进程...
taskkill /IM python.exe /F 2>nul
if errorlevel 1 (
    echo 没有找到Python进程
) else (
    echo 已停止所有Python进程
)

echo.
echo [2/3] 等待端口释放...
timeout /t 2 /nobreak > nul

echo.
echo [3/3] 启动新的工具管理器...
cd /d "%~dp0"
python run_tool_manager.py

pause
