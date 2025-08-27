# ComfyUI 节点显示问题解决方案

## 🔍 问题描述
插件在ComfyUI启动时成功加载，但在界面中找不到节点，ComfyUI Manager中也找不到该项目。

## ✅ 已修复的问题
我们已经优化了以下几个可能导致节点不显示的问题：

1. **简化类别名称**: 从 `popo-utility/image` 改为 `popo-utility`
2. **去除emoji符号**: 移除了可能导致兼容性问题的emoji字符
3. **标准化显示名称**: 使用简洁的英文名称

## 📋 当前节点信息
经过优化后，插件现在注册了以下节点：

| 节点名称 | 显示名称 | 类别 | 功能描述 |
|---------|---------|------|----------|
| ImageSizeNode | Image Size | popo-utility | 获取图片长边和短边尺寸 |
| ImageDimensionsNode | Image Dimensions | popo-utility | 获取详细尺寸信息 |
| ImageAspectRatioNode | Image Aspect Ratio | popo-utility | 计算宽高比和识别比例类型 |

## 🔧 ComfyUI 中查找节点的方法

### 1. 按类别查找
在ComfyUI中右键添加节点时，查找以下路径：
```
Add Node → popo-utility → Image Size
Add Node → popo-utility → Image Dimensions  
Add Node → popo-utility → Image Aspect Ratio
```

### 2. 使用搜索功能
在节点搜索框中输入以下关键词：
- `popo`
- `Image Size`
- `Image Dimensions`
- `Image Aspect Ratio`
- `size`
- `dimensions`
- `aspect`

### 3. 检查所有节点列表
确保在ComfyUI的节点浏览器中能看到 `popo-utility` 分类。

## 🔍 故障排除步骤

### 第1步: 确认插件位置
确保插件位于正确的ComfyUI目录下：
```
ComfyUI/
└── custom_nodes/
    └── comfyui-popo-utility/
        ├── __init__.py
        ├── nodes/
        └── ...
```

### 第2步: 检查ComfyUI控制台
1. 启动ComfyUI时查看控制台输出
2. 应该看到类似以下信息：
```
🚀 Popo Utility v1.0.0 加载完成
📦 已注册 3 个节点
```

### 第3步: 完全重启ComfyUI
1. 完全关闭ComfyUI进程
2. 清除缓存（删除 `ComfyUI/temp` 目录，如果存在）
3. 重新启动ComfyUI

### 第4步: 检查Python环境
确保ComfyUI使用的Python环境包含必要的依赖：
- torch >= 1.12.0
- numpy >= 1.20.0
- Pillow >= 8.0.0

### 第5步: 使用诊断工具
运行我们提供的诊断脚本：
```bash
cd ComfyUI/custom_nodes/comfyui-popo-utility
python diagnose_comfyui.py
```

## 🐛 常见问题及解决方案

### 问题1: 节点类别不显示
**解决方案**: 
- 检查是否有其他插件使用了相同的类别名称
- 尝试搜索节点名称而不是浏览类别

### 问题2: 搜索找不到节点
**解决方案**:
- 确保搜索时没有额外的空格或特殊字符
- 尝试搜索部分名称（如只搜索"Image"）

### 问题3: 插件加载错误
**解决方案**:
- 检查ComfyUI控制台的错误信息
- 确保所有依赖都正确安装
- 检查文件权限

### 问题4: 节点显示但无法使用
**解决方案**:
- 确保输入类型正确（需要IMAGE类型输入）
- 检查节点是否正确连接

## 📱 ComfyUI Manager 集成

要在ComfyUI Manager中显示此项目，需要：

1. **项目发布**: 项目需要发布到官方的ComfyUI节点列表
2. **元数据完整**: 确保 `pyproject.toml` 包含正确的项目信息
3. **标准化结构**: 遵循ComfyUI插件的标准目录结构

当前项目结构已经符合ComfyUI Manager的要求，但需要提交到官方列表才能在Manager中显示。

## 🧪 验证节点功能

创建简单的测试工作流：

1. 添加 `Load Image` 节点
2. 添加我们的 `Image Size` 节点
3. 连接图片输出到尺寸节点的输入
4. 添加 `Preview Text` 或类似节点查看输出

预期输出：
- `long_side`: 图片的长边像素数
- `short_side`: 图片的短边像素数

## 📞 获取支持

如果问题仍然存在：

1. 检查ComfyUI版本兼容性
2. 查看ComfyUI的GitHub Issues
3. 检查其他类似插件的实现
4. 参考ComfyUI官方文档

## 🔄 快速重新安装

如果需要重新安装插件：

```bash
# 1. 删除现有插件
rm -rf ComfyUI/custom_nodes/comfyui-popo-utility

# 2. 重新克隆
cd ComfyUI/custom_nodes/
git clone https://github.com/popoimm/comfyui-popo-utility.git

# 3. 重启ComfyUI
```

## ✅ 确认清单

完成以下检查确保节点正确显示：

- [ ] 插件在正确的 `custom_nodes` 目录下
- [ ] ComfyUI完全重启
- [ ] 控制台显示插件加载成功
- [ ] 在 `popo-utility` 类别下查找节点
- [ ] 尝试搜索节点名称
- [ ] 检查是否有错误信息
- [ ] 清除ComfyUI缓存
- [ ] 验证Python环境依赖

如果所有步骤都完成但仍然找不到节点，可能是ComfyUI版本兼容性问题，建议升级到最新版本的ComfyUI。