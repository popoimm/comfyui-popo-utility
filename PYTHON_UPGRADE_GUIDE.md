# ComfyUI Popo Utility - Python 3.12.9 开发环境升级指南

## 🎯 目标
将本地开发环境从 Python 3.10.9 升级到 Python 3.12.9，以匹配 ComfyUI 环境。

## 📋 当前状态
- 当前版本：Python 3.10.9  
- 目标版本：Python 3.12.9
- 环境管理：pyenv

## 🚀 升级步骤

### 1. 安装 Python 3.12.9

#### 方法A: 使用 pyenv (推荐)
```bash
# 更新 pyenv 版本数据库
brew update && brew upgrade pyenv

# 安装 Python 3.12.9
pyenv install 3.12.9

# 在项目目录设置本地版本
cd /Users/getway/QoderProject/comfyui-popo-utility
pyenv local 3.12.9
```

#### 方法B: 如果 pyenv 版本过旧
```bash
# 安装最接近的版本
pyenv install --list | grep 3.12
pyenv install 3.12.0  # 或其他可用版本

# 设置项目版本
pyenv local 3.12.0
```

#### 方法C: 使用 Homebrew
```bash
# 安装 Python 3.12
brew install python@3.12

# 创建符号链接 (如果需要)
ln -sf /opt/homebrew/bin/python3.12 /usr/local/bin/python3.12
```

### 2. 创建新的虚拟环境

```bash
# 删除旧的虚拟环境 (如果存在)
rm -rf venv

# 使用 Python 3.12 创建新环境
python3.12 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 验证版本
python --version  # 应该显示 Python 3.12.x
```

### 3. 安装项目依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装开发依赖
pip install -e ".[dev]"

# 安装 PyTorch (CPU版本，适合开发)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### 4. 验证环境

```bash
# 测试基本导入
python -c "import torch; print(f'PyTorch: {torch.__version__}')"

# 测试插件加载
python -c "import __init__; print('✅ 插件加载成功')"

# 运行测试
python test_nodes.py
```

## 🔧 项目配置更新

项目已更新以支持 Python 3.12.9：

### pyproject.toml 更新
- ✅ 添加 Python 3.12 分类器
- ✅ 更新 black 目标版本
- ✅ 更新 mypy Python 版本

### 新增文件
- ✅ `.python-version`: 指定项目 Python 版本
- ✅ `setup_dev_env.sh`: 自动化环境设置脚本
- ✅ `PYTHON_UPGRADE_GUIDE.md`: 本升级指南

## 🐛 常见问题解决

### 问题1: pyenv 版本过旧
```bash
# 手动更新 pyenv
git -C $(pyenv root) pull
# 或者重新安装
brew uninstall pyenv
brew install pyenv
```

### 问题2: Python 3.12.9 不可用
```bash
# 使用最新的 3.12 版本
pyenv install --list | grep "3\.12\.[0-9]" | tail -1
pyenv install <最新版本>
```

### 问题3: 依赖兼容性问题
```bash
# 清理 pip 缓存
pip cache purge

# 重新安装依赖
pip install --force-reinstall -e ".[dev]"
```

## 📦 推荐的开发工具链

### IDE 配置
- **VSCode**: 安装 Python 扩展，配置解释器路径
- **PyCharm**: 设置项目解释器为虚拟环境中的 Python

### 代码质量工具
```bash
# 代码格式化
black .

# 类型检查
mypy nodes/

# 代码风格检查
flake8 .
```

## 🔄 自动化脚本使用

项目提供了自动化设置脚本：

```bash
# 给脚本执行权限
chmod +x setup_dev_env.sh

# 运行环境设置
./setup_dev_env.sh
```

## ✅ 验证清单

完成升级后，请验证以下项目：

- [ ] Python 版本为 3.12.x
- [ ] 虚拟环境正常激活
- [ ] 所有依赖正确安装
- [ ] 插件可以正常导入
- [ ] 测试全部通过
- [ ] ComfyUI 兼容性正常

## 🚀 下一步

环境升级完成后：

1. **测试兼容性**: 在实际 ComfyUI 环境中测试插件
2. **更新文档**: 确保 README.md 反映新的环境要求  
3. **CI/CD 更新**: 如果有持续集成，更新配置文件
4. **团队同步**: 通知其他开发者环境升级要求

## 🆘 需要帮助？

如果遇到问题：
1. 检查 Python 和 pip 版本
2. 查看错误日志
3. 参考项目 Issues
4. 联系维护团队