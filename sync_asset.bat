@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ======== 1. 切换到 qt_ws 目录并更新 ========
cd /d D:/ws/qt_ws
if errorlevel 1 goto :error
git checkout worker002
git pull origin worker002
if errorlevel 1 goto :error

echo.
echo ======== 2. 切换到 github 仓库 ========
cd /d D:/ws/chenyikuan.github.io
git pull origin master
if errorlevel 1 goto :error

echo ======== 3. 激活 conda 并执行同步脚本 ========
call D:/miniconda3/Scripts/activate base
if errorlevel 1 goto :another_conda_path
:run_python
python sync_asset.py
if errorlevel 1 goto :error

echo.
echo ======== 4. 检查是否有变更需要提交 ========
git status --porcelain
if errorlevel 1 goto :error

for /f %%i in ('git status --porcelain') do set hasChanges=1

if defined hasChanges (
    echo 检测到变更，执行 commit 和 push...
    git commit -am "update net"
    if errorlevel 1 goto :error
    git push origin master
    if errorlevel 1 goto :error
    echo ✅ 提交并推送成功
) else (
    echo ℹ️ 没有需要提交的变更，跳过 commit / push
)

echo.
echo ======== 脚本执行完成 ========
pause
exit /b 0

:error
echo ❌ 脚本执行出错，退出码: %errorlevel%
pause
exit /b %errorlevel%

:another_conda_path
call D:/windows/Softwares/anaconda39/Scripts/activate base
goto :run_python
