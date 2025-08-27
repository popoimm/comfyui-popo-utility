#!/bin/bash
# 快速切换到Python 3.12.9开发环境

set -e

PROJECT_DIR="/Users/getway/QoderProject/comfyui-popo-utility"

echo "🔄 切换到Python 3.12.9开发环境"
echo "================================"

cd "$PROJECT_DIR"

# 检查Python 3.12.9是否已安装
if pyenv versions | grep -q "3.12.9"; then
    echo "✅ Python 3.12.9 已安装"
    
    # 设置本地版本
    pyenv local 3.12.9
    echo "✅ 项目Python版本设置为 3.12.9"
    
    # 验证版本
    CURRENT_VERSION=$(python --version)
    echo "📋 当前版本: $CURRENT_VERSION"
    
    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        echo "📦 创建Python 3.12.9虚拟环境..."
        python -m venv venv
        echo "✅ 虚拟环境创建完成"
    else
        echo "✅ 虚拟环境已存在"
    fi
    
    echo ""
    echo "🚀 环境准备完成！"
    echo ""
    echo "下一步操作："
    echo "1. 激活虚拟环境: source venv/bin/activate"
    echo "2. 安装依赖: pip install -e \".[dev]\""
    echo "3. 验证环境: python verify_env.py"
    echo ""
    
else
    echo "❌ Python 3.12.9 尚未安装完成"
    echo "⏳ 请等待安装完成后再运行此脚本"
    echo ""
    echo "检查安装进度："
    echo "pyenv install --list | grep 3.12.9"
    echo "pyenv versions"
fi