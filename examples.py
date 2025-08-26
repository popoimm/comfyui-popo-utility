"""
ComfyUI Popo Utility 使用示例
展示如何在ComfyUI工作流中使用图片尺寸获取节点
"""

# 这是一个示例工作流的JSON配置，展示了如何使用我们的节点

EXAMPLE_WORKFLOW = {
    "1": {
        "inputs": {
            "image": "example.jpg",
            "upload": "image"
        },
        "class_type": "LoadImage"
    },
    "2": {
        "inputs": {
            "image": ["1", 0]  # 连接到LoadImage节点的输出
        },
        "class_type": "ImageSizeNode"  # 我们的长短边尺寸节点
    },
    "3": {
        "inputs": {
            "image": ["1", 0]  # 连接到LoadImage节点的输出  
        },
        "class_type": "ImageDimensionsNode"  # 我们的详细尺寸节点
    },
    "4": {
        "inputs": {
            "text": "Long side: {long_side}, Short side: {short_side}",
            "long_side": ["2", 0],  # 连接到ImageSizeNode的长边输出
            "short_side": ["2", 1]  # 连接到ImageSizeNode的短边输出
        },
        "class_type": "ShowText"
    }
}

# 常见使用场景示例

def usage_examples():
    """展示常见的使用场景"""
    
    scenarios = [
        {
            "name": "条件图片处理",
            "description": "根据图片是横图还是竖图选择不同的处理方式",
            "workflow": "LoadImage → ImageSizeNode → 条件判断 → 不同的处理分支"
        },
        {
            "name": "图片尺寸标准化",
            "description": "获取图片尺寸用于计算缩放比例",
            "workflow": "LoadImage → ImageDimensionsNode → 计算缩放比例 → Resize"
        },
        {
            "name": "批量图片分析",
            "description": "分析一批图片的尺寸分布",
            "workflow": "LoadImage → ImageDimensionsNode → 收集尺寸数据 → 统计分析"
        },
        {
            "name": "智能裁剪准备",
            "description": "根据长边和短边决定裁剪策略",
            "workflow": "LoadImage → ImageSizeNode → 裁剪参数计算 → 智能裁剪"
        }
    ]
    
    print("🎯 常见使用场景:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print(f"   描述: {scenario['description']}")  
        print(f"   工作流: {scenario['workflow']}")

if __name__ == "__main__":
    print("📖 ComfyUI Popo Utility 使用示例")
    print("=" * 50)
    
    usage_examples()
    
    print("\n" + "=" * 50)
    print("💡 提示:")
    print("- 在ComfyUI中，右键点击空白区域选择'Add Node'")
    print("- 在分类中找到'popo-utility'")
    print("- 选择需要的节点拖拽到工作区")
    print("- 连接IMAGE输入到图片加载节点的输出")
    print("- 连接节点输出到需要使用尺寸信息的其他节点")