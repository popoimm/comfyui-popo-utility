# ComfyUI 节点显示问题 - 完整解决方案

## 🚨 当前状态
✅ **插件已优化**：我们已经创建了一个完全兼容ComfyUI的简化版本  
✅ **格式验证通过**：所有节点都符合ComfyUI标准  
✅ **功能测试正常**：节点可以正确处理图片数据

## 📍 问题定位

如果节点仍然不显示，问题很可能是以下几种情况之一：

### 1. 插件安装位置不正确
ComfyUI需要插件位于特定目录：
```
ComfyUI/
└── custom_nodes/
    └── comfyui-popo-utility/
        ├── __init__.py
        ├── nodes_direct.py
        └── ...
```

### 2. ComfyUI缓存问题
ComfyUI可能缓存了旧的节点信息。

### 3. Python环境不匹配
ComfyUI和插件使用了不同的Python环境。

## 🔧 逐步解决方案

### 步骤1: 验证安装位置
```bash
# 检查ComfyUI目录结构
ls -la ComfyUI/custom_nodes/
# 应该看到 comfyui-popo-utility 目录

# 检查插件文件
ls -la ComfyUI/custom_nodes/comfyui-popo-utility/
# 应该看到 __init__.py 和 nodes_direct.py
```

### 步骤2: 完全清理和重新安装
```bash
# 1. 停止ComfyUI
# 2. 删除现有插件
rm -rf ComfyUI/custom_nodes/comfyui-popo-utility

# 3. 重新克隆最新版本
cd ComfyUI/custom_nodes/
git clone https://github.com/popoimm/comfyui-popo-utility.git

# 4. 清除ComfyUI缓存
rm -rf ComfyUI/temp/
rm -rf ComfyUI/__pycache__/

# 5. 重启ComfyUI
```

### 步骤3: 验证Python环境
```bash
# 在ComfyUI目录下检查Python版本
cd ComfyUI
python --version

# 检查torch是否可用
python -c "import torch; print(torch.__version__)"
```

### 步骤4: 测试插件加载
```bash
# 在插件目录下测试
cd ComfyUI/custom_nodes/comfyui-popo-utility
python test_comfyui_specific.py

# 应该看到：✅ 节点应该能在ComfyUI中正常显示!
```

## 🔍 在ComfyUI中查找节点

### 方法1: 类别浏览
1. 在ComfyUI界面中右键点击空白区域
2. 选择 "Add Node"
3. 找到 **"popo-utility"** 类别
4. 选择以下节点之一：
   - **Popo Image Size**
   - **Popo Image Dimensions**
   - **Popo Image Aspect Ratio**

### 方法2: 搜索功能
在节点添加对话框的搜索框中输入：
- `popo` (会显示所有我们的节点)
- `Image Size` (查找尺寸节点)
- `Dimensions` (查找详细尺寸节点)
- `Aspect` (查找宽高比节点)

### 方法3: 检查所有节点
如果上述方法都找不到，请：
1. 打开节点浏览器/节点列表
2. 查看是否有 "popo-utility" 分类
3. 检查ComfyUI控制台的启动日志

## 🐛 常见问题排查

### 问题1: 控制台无加载信息
**症状**: ComfyUI启动时没有看到 "Popo Utility v1.0.1 - Simple version loaded!"

**解决方案**:
```bash
# 检查插件是否在正确位置
ls ComfyUI/custom_nodes/comfyui-popo-utility/__init__.py

# 检查文件权限
chmod +r ComfyUI/custom_nodes/comfyui-popo-utility/*

# 检查Python语法
cd ComfyUI/custom_nodes/comfyui-popo-utility
python -m py_compile __init__.py
```

### 问题2: 看到加载信息但找不到节点
**症状**: 控制台显示插件加载成功，但界面中找不到

**解决方案**:
1. 确保搜索时没有拼写错误
2. 尝试搜索 "popo" 而不是完整名称
3. 检查是否被其他插件的同名类别覆盖
4. 重启ComfyUI并清除浏览器缓存（如果使用Web版本）

### 问题3: 节点显示但无法使用
**症状**: 节点出现在列表中但添加时出错

**解决方案**:
```bash
# 检查依赖
cd ComfyUI/custom_nodes/comfyui-popo-utility
python -c "import torch; import numpy as np; print('依赖正常')"

# 测试节点功能
python -c "
from nodes_direct import PopoImageSizeNode
import torch
test_image = torch.randn(1, 256, 256, 3)
node = PopoImageSizeNode()
result = node.get_image_size(test_image)
print(f'测试结果: {result}')
"
```

## 📱 ComfyUI Manager 说明

**为什么ComfyUI Manager中找不到？**

ComfyUI Manager显示的是社区维护的官方插件列表。我们的插件需要提交到以下位置才能被Manager收录：

1. [ComfyUI-Manager 插件列表](https://github.com/ltdrdata/ComfyUI-Manager)
2. 满足官方的提交要求
3. 等待审核通过

**当前安装方式**（推荐）：
```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/popoimm/comfyui-popo-utility.git
```

## 🧪 验证安装成功

创建测试工作流：

1. **添加Load Image节点**
   - 加载任意图片

2. **添加我们的节点**
   - 右键 → Add Node → popo-utility → Popo Image Size

3. **连接节点**
   - 将图片输出连接到尺寸节点的image输入

4. **执行并查看结果**
   - 应该看到图片的长边和短边尺寸数值

## 📞 需要帮助？

如果问题仍然存在，请提供以下信息：

1. **ComfyUI版本**: 在控制台查看版本号
2. **操作系统**: Windows/macOS/Linux
3. **Python版本**: `python --version`
4. **安装方式**: git clone / 手动下载
5. **错误信息**: 完整的控制台输出
6. **测试结果**: 运行 `python test_comfyui_specific.py` 的输出

## ✅ 检查清单

在确认"找不到节点"之前，请确保：

- [ ] 插件在 `ComfyUI/custom_nodes/comfyui-popo-utility/` 目录下
- [ ] ComfyUI完全重启（关闭进程并重新启动）
- [ ] 控制台显示 "Popo Utility v1.0.1 - Simple version loaded!"
- [ ] 运行 `python test_comfyui_specific.py` 显示成功
- [ ] 在 "popo-utility" 类别下查找节点
- [ ] 尝试搜索 "popo" 关键词
- [ ] 清除了ComfyUI缓存（temp目录）
- [ ] 没有其他插件冲突

如果所有步骤都完成但仍然找不到节点，可能是ComfyUI版本兼容性问题，建议：

1. 更新ComfyUI到最新版本
2. 检查ComfyUI的GitHub Issues
3. 尝试其他已知工作的插件确认ComfyUI功能正常

---

**记住**: 我们已经验证了插件完全符合ComfyUI规范。如果按照上述步骤操作后仍有问题，那很可能是环境配置或ComfyUI本身的问题，而不是插件的问题。