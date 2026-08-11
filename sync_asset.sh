#!/bin/bash

ws_dir='/home/yikuan/ws'

echo "======== 1. 切换到 qt_ws 目录并更新 ========"
cd $ws_dir/qt_ws || exit
git checkout worker002
git pull origin worker002

echo ""
echo "======== 2. 切换到 github 仓库 ========"
cd $ws_dir/chenyikuan.github.io || exit
git pull origin master

echo "======== 3. 激活 conda 并执行同步脚本 ========"
# source /home/yikuan/miniconda3/etc/profile.d/conda.sh
# conda activate base
python sync_asset.py

echo ""
echo "======== 4. 检查是否有变更需要提交 ========"
git status --porcelain
hasChanges=$(git status --porcelain | wc -l)

if [ $hasChanges -gt 0 ]; then
    echo "检测到变更，执行 commit 和 push..."
    git commit -am "update net"
    git push origin master
    echo "✅ 提交并推送成功"
else
    echo "ℹ️ 没有需要提交的变更，跳过 commit / push"
fi

echo ""
echo "======== 脚本执行完成 ========"
# pause 在bash中不需要，用read替代（如需暂停）
# read -p "按任意键继续..."
exit 0
