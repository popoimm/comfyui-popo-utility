# Python LZMA 模块修复指南

## 🔍 问题描述

Python 3.12.9 安装时出现警告：
```
WARNING: The Python lzma extension was not compiled. Missing the lzma lib?
```

这会导致 `torchvision` 导入失败：
```
ModuleNotFoundError: No module named '_lzma'
```

## 💡 解决方案

### 方法1: 安装系统依赖并重新编译Python (推荐)

```bash
# 安装 xz 库 (包含 lzma)
brew install xz

# 重新安装 Python 3.12.9
pyenv uninstall 3.12.9
pyenv install 3.12.9

# 切换到项目目录并设置版本
cd /Users/getway/QoderProject/comfyui-popo-utility
pyenv local 3.12.9

# 重新创建虚拟环境
rm -rf venv
python -m venv venv
source venv/bin/activate

# 重新安装依赖
pip install --upgrade pip
pip install -e ".[dev]"
```

### 方法2: 使用已编译的Python版本

如果方法1失败，可以使用conda或官方Python：

```bash
# 选项A: 使用conda
conda create -n comfyui-dev python=3.12.9
conda activate comfyui-dev

# 选项B: 使用官方Python
# 从 https://www.python.org/downloads/ 下载Python 3.12.9
# 安装后创建虚拟环境
```

### 方法3: 使用替代版本

如果无法修复，可以使用Python 3.11：

```bash
# 安装Python 3.11 (通常更稳定)
pyenv install 3.11.10
pyenv local 3.11.10

# 更新项目配置
echo "3.11.10" > .python-version
```

## 🧪 验证修复

```bash
# 测试lzma模块
python -c "import lzma; print('lzma模块正常工作')"

# 测试torchvision
python -c "import torchvision; print(f'torchvision: {torchvision.__version__}')"

# 运行完整验证
python verify_env.py
```

## 📝 注意事项

1. **对ComfyUI的影响**: lzma主要用于数据压缩，大多数ComfyUI功能不受影响
2. **替代方案**: 如果问题持续，可以暂时不使用torchvision的高级功能
3. **兼容性**: Python 3.11.x 通常比3.12.x更稳定，推荐在生产环境使用

## 🔧 自动修复脚本

项目提供了自动修复脚本：

```bash
# 运行自动修复
chmod +x fix_lzma.sh
./fix_lzma.sh
```

## ✅ 成功标志

修复成功后，`python verify_env.py` 应该显示：
- ✅ torchvision: x.x.x
- 🎉 所有检查通过