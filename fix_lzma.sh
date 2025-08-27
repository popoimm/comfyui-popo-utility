#!/bin/bash
# 自动修复Python lzma模块问题

set -e

echo "🔧 Python LZMA 模块自动修复脚本"
echo "================================="

PROJECT_DIR="/Users/getway/QoderProject/comfyui-popo-utility"
cd "$PROJECT_DIR"

# 检查当前问题
echo "🔍 检查当前问题..."
if python -c "import lzma" 2>/dev/null; then
    echo "✅ lzma模块工作正常，无需修复"
    exit 0
else
    echo "❌ 检测到lzma模块问题，开始修复..."
fi

# 检查并安装xz库
echo ""
echo "📦 检查系统依赖..."
if brew list xz &>/dev/null; then
    echo "✅ xz库已安装"
else
    echo "📥 安装xz库..."
    if brew install xz; then
        echo "✅ xz库安装成功"
    else
        echo "❌ xz库安装失败，请手动安装"
        exit 1
    fi
fi

# 提供用户选择
echo ""
echo "🤔 选择修复方案："
echo "1. 重新安装Python 3.12.9 (推荐，需要时间)"
echo "2. 跳过修复，继续使用当前环境 (某些功能可能受限)"
echo "3. 切换到Python 3.11.10 (最稳定)"
echo ""
read -p "请选择 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "🔄 重新安装Python 3.12.9..."
        
        # 卸载现有版本
        pyenv uninstall -f 3.12.9
        
        # 重新安装
        echo "📥 重新安装Python 3.12.9 (这可能需要几分钟)..."
        if pyenv install 3.12.9; then
            echo "✅ Python 3.12.9重新安装成功"
        else
            echo "❌ Python 3.12.9重新安装失败"
            exit 1
        fi
        
        # 设置本地版本
        pyenv local 3.12.9
        echo "✅ 项目Python版本设置为3.12.9"
        
        # 重新创建虚拟环境
        echo "🔄 重新创建虚拟环境..."
        rm -rf venv
        python -m venv venv
        source venv/bin/activate
        
        # 重新安装依赖
        echo "📦 重新安装依赖..."
        pip install --upgrade pip
        pip install -e ".[dev]"
        
        echo ""
        echo "🧪 验证修复结果..."
        if python -c "import lzma; import torchvision; print('✅ 修复成功！')" 2>/dev/null; then
            echo "🎉 lzma和torchvision现在都工作正常！"
        else
            echo "⚠️  修复可能不完整，但基本功能应该可用"
        fi
        ;;
        
    2)
        echo ""
        echo "⚠️  继续使用当前环境"
        echo "注意：某些torchvision功能可能不可用"
        echo "ComfyUI基本功能不受影响"
        ;;
        
    3)
        echo ""
        echo "🔄 切换到Python 3.11.10..."
        
        # 检查是否已安装3.11.10
        if pyenv versions | grep -q "3.11.10"; then
            echo "✅ Python 3.11.10已安装"
        else
            echo "📥 安装Python 3.11.10..."
            pyenv install 3.11.10
        fi
        
        # 设置本地版本
        pyenv local 3.11.10
        echo "3.11.10" > .python-version
        echo "✅ 项目Python版本设置为3.11.10"
        
        # 重新创建虚拟环境
        echo "🔄 重新创建虚拟环境..."
        rm -rf venv
        python -m venv venv
        source venv/bin/activate
        
        # 重新安装依赖
        echo "📦 重新安装依赖..."
        pip install --upgrade pip
        pip install -e ".[dev]"
        
        echo ""
        echo "🧪 验证修复结果..."
        if python -c "import lzma; import torchvision; print('✅ 修复成功！')" 2>/dev/null; then
            echo "🎉 环境现在完全正常！"
        else
            echo "❌ 仍然存在问题，请查看错误信息"
        fi
        ;;
        
    *)
        echo "❌ 无效选择，退出"
        exit 1
        ;;
esac

echo ""
echo "🏁 修复脚本完成"
echo ""
echo "📋 下一步："
echo "1. 运行验证: python verify_env.py"
echo "2. 测试插件: python -c \"import __init__; print('插件工作正常')\""
echo "3. 在ComfyUI中测试节点功能"