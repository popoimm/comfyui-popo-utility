#!/bin/bash
# ComfyUI Popo Utility 开发环境设置脚本

set -e

echo "🚀 ComfyUI Popo Utility 开发环境设置"
echo "====================================="

# 检查Python版本
REQUIRED_PYTHON="3.12.9"
CURRENT_PYTHON=$(python --version 2>&1 | cut -d' ' -f2)

echo "📋 环境检查:"
echo "   需要 Python: ${REQUIRED_PYTHON}"
echo "   当前 Python: ${CURRENT_PYTHON}"

# 检查是否需要安装Python 3.12.9
if ! command -v python3.12 &> /dev/null; then
    echo "⚠️  Python 3.12 未找到"
    echo "🔧 安装建议:"
    echo ""
    echo "   方法1: 使用pyenv安装 (推荐)"
    echo "   pyenv install 3.12.9"
    echo "   pyenv local 3.12.9"
    echo ""
    echo "   方法2: 使用Homebrew安装"
    echo "   brew install python@3.12"
    echo ""
    echo "   方法3: 从官网下载"
    echo "   https://www.python.org/downloads/"
    echo ""
else
    echo "✅ Python 3.12 已安装"
    python3.12 --version
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 创建虚拟环境..."
    
    if command -v python3.12 &> /dev/null; then
        python3.12 -m venv venv
        echo "✅ 使用 Python 3.12 创建虚拟环境"
    else
        python -m venv venv
        echo "⚠️  使用当前 Python 版本创建虚拟环境"
    fi
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境
echo ""
echo "🔄 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "📦 升级pip..."
pip install --upgrade pip

# 安装依赖
echo "📦 安装项目依赖..."
pip install -e ".[dev]"

# 安装ComfyUI兼容的依赖
echo "📦 安装ComfyUI兼容依赖..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

echo ""
echo "🎉 开发环境设置完成！"
echo ""
echo "🔧 使用方法:"
echo "   1. 激活虚拟环境: source venv/bin/activate"
echo "   2. 运行测试: python test_nodes.py"
echo "   3. 开发新节点: 参考 node_template.py"
echo ""
echo "📚 文档:"
echo "   - 开发指南: DEVELOPMENT_GUIDE.md"
echo "   - 项目说明: README.md"
echo ""
echo "⚡ 快速验证:"
echo "   python -c \"import __init__; print('✅ 插件加载成功')\""