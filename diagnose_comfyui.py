#!/usr/bin/env python3
"""
ComfyUI 插件集成诊断工具
诊断为什么节点在ComfyUI界面中不显示
"""

import sys
import os
import json
from pathlib import Path

def diagnose_comfyui_integration():
    """诊断ComfyUI集成问题"""
    
    print("🔍 ComfyUI 插件集成诊断")
    print("=" * 50)
    
    # 1. 检查节点映射
    print("📋 1. 检查节点映射...")
    try:
        import __init__ as plugin
        
        if hasattr(plugin, 'NODE_CLASS_MAPPINGS') and hasattr(plugin, 'NODE_DISPLAY_NAME_MAPPINGS'):
            mappings = plugin.NODE_CLASS_MAPPINGS
            display_mappings = plugin.NODE_DISPLAY_NAME_MAPPINGS
            
            print(f"✅ NODE_CLASS_MAPPINGS: {len(mappings)} 个节点")
            print(f"✅ NODE_DISPLAY_NAME_MAPPINGS: {len(display_mappings)} 个显示名称")
            
            if len(mappings) == 0:
                print("❌ 错误: 没有注册任何节点！")
                return False
                
            for class_name, node_class in mappings.items():
                display_name = display_mappings.get(class_name, class_name)
                print(f"   - {display_name} ({class_name})")
                
                # 检查节点类的必要属性
                required_attrs = ['INPUT_TYPES', 'RETURN_TYPES', 'RETURN_NAMES', 'FUNCTION']
                missing_attrs = []
                
                for attr in required_attrs:
                    if not hasattr(node_class, attr):
                        missing_attrs.append(attr)
                
                if missing_attrs:
                    print(f"     ❌ 缺少属性: {missing_attrs}")
                else:
                    print(f"     ✅ 节点接口完整")
                    
                # 检查CATEGORY
                category = getattr(node_class, 'CATEGORY', '未设置')
                print(f"     📂 类别: {category}")
                
        else:
            print("❌ 错误: 插件缺少必要的节点映射!")
            print("   请确保__init__.py导出了NODE_CLASS_MAPPINGS和NODE_DISPLAY_NAME_MAPPINGS")
            return False
            
    except Exception as e:
        print(f"❌ 节点映射检查失败: {e}")
        return False
    
    # 2. 检查ComfyUI模块格式兼容性
    print("\n🎨 2. 检查ComfyUI格式兼容性...")
    
    # 检查是否有WEB_DIRECTORY (前端资源)
    if hasattr(plugin, 'WEB_DIRECTORY'):
        web_dir = plugin.WEB_DIRECTORY
        print(f"📁 WEB_DIRECTORY: {web_dir}")
        if web_dir and os.path.exists(web_dir):
            print("✅ 前端资源目录存在")
        elif web_dir:
            print("⚠️  前端资源目录不存在，但不影响基本功能")
        else:
            print("ℹ️  未设置前端资源目录")
    else:
        print("ℹ️  未定义WEB_DIRECTORY (可选)")
    
    # 3. 测试节点实例化
    print("\n🧪 3. 测试节点实例化...")
    
    for class_name, node_class in mappings.items():
        try:
            # 测试实例化
            instance = node_class()
            print(f"✅ {class_name}: 实例化成功")
            
            # 测试INPUT_TYPES调用
            input_types = node_class.INPUT_TYPES()
            if isinstance(input_types, dict) and 'required' in input_types:
                print(f"   ✅ INPUT_TYPES格式正确")
            else:
                print(f"   ❌ INPUT_TYPES格式错误: {input_types}")
                
            # 测试执行函数是否存在
            func_name = getattr(node_class, 'FUNCTION', '')
            if func_name and hasattr(instance, func_name):
                print(f"   ✅ 执行函数 '{func_name}' 存在")
            else:
                print(f"   ❌ 执行函数 '{func_name}' 不存在")
                
        except Exception as e:
            print(f"❌ {class_name}: 实例化失败 - {e}")
    
    # 4. 生成ComfyUI兼容性报告
    print("\n📊 4. ComfyUI兼容性报告...")
    
    compatibility_issues = []
    
    for class_name, node_class in mappings.items():
        issues = []
        
        # 检查RETURN_TYPES是否是元组
        if hasattr(node_class, 'RETURN_TYPES'):
            if not isinstance(node_class.RETURN_TYPES, tuple):
                issues.append("RETURN_TYPES不是元组")
        else:
            issues.append("缺少RETURN_TYPES")
            
        # 检查RETURN_NAMES是否是元组
        if hasattr(node_class, 'RETURN_NAMES'):
            if not isinstance(node_class.RETURN_NAMES, tuple):
                issues.append("RETURN_NAMES不是元组")
        else:
            issues.append("缺少RETURN_NAMES")
            
        # 检查FUNCTION是否是字符串
        if hasattr(node_class, 'FUNCTION'):
            if not isinstance(node_class.FUNCTION, str):
                issues.append("FUNCTION不是字符串")
        else:
            issues.append("缺少FUNCTION")
            
        # 检查INPUT_TYPES是否是类方法
        if not (hasattr(node_class, 'INPUT_TYPES') and callable(node_class.INPUT_TYPES)):
            issues.append("INPUT_TYPES不是可调用方法")
            
        if issues:
            compatibility_issues.append((class_name, issues))
    
    if compatibility_issues:
        print("❌ 发现兼容性问题:")
        for class_name, issues in compatibility_issues:
            print(f"   {class_name}:")
            for issue in issues:
                print(f"     - {issue}")
        return False
    else:
        print("✅ 所有节点都符合ComfyUI规范")
    
    # 5. 生成ComfyUI节点信息JSON
    print("\n📄 5. 生成节点信息...")
    
    try:
        node_info = {}
        for class_name, node_class in mappings.items():
            try:
                instance = node_class()
                input_types = node_class.INPUT_TYPES()
                
                node_info[class_name] = {
                    "display_name": display_mappings.get(class_name, class_name),
                    "category": getattr(node_class, 'CATEGORY', 'popo-utility'),
                    "input_types": input_types,
                    "return_types": list(node_class.RETURN_TYPES) if hasattr(node_class, 'RETURN_TYPES') else [],
                    "return_names": list(node_class.RETURN_NAMES) if hasattr(node_class, 'RETURN_NAMES') else [],
                    "function": getattr(node_class, 'FUNCTION', ''),
                    "description": getattr(node_class, 'DESCRIPTION', ''),
                }
            except Exception as e:
                print(f"⚠️  无法生成 {class_name} 的信息: {e}")
        
        # 保存节点信息到文件
        with open('comfyui_node_info.json', 'w', encoding='utf-8') as f:
            json.dump(node_info, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 节点信息已保存到 comfyui_node_info.json")
        
    except Exception as e:
        print(f"❌ 生成节点信息失败: {e}")
    
    # 6. 提供解决建议
    print("\n💡 6. 可能的解决方案...")
    
    suggestions = [
        "确保ComfyUI已完全重启 (关闭并重新启动)",
        "检查ComfyUI控制台是否有错误信息",
        "清除ComfyUI缓存 (删除ComfyUI/temp目录)",
        "确认插件安装在正确的custom_nodes目录下",
        "检查节点类别名称是否正确 (可能被归类到意外的分类下)",
        "尝试在ComfyUI的节点搜索功能中搜索'popo'或'Image Size'",
        "检查是否有其他插件与此插件冲突",
    ]
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
    
    print("\n" + "=" * 50)
    return True

def main():
    """主函数"""
    success = diagnose_comfyui_integration()
    
    if success:
        print("🎉 诊断完成！请根据上述建议检查ComfyUI。")
    else:
        print("❌ 发现问题！请修复上述错误后重新测试。")
    
    print("\n📋 快速检查清单:")
    print("□ ComfyUI已完全重启")
    print("□ 插件在custom_nodes目录下")
    print("□ 控制台没有错误信息")
    print("□ 尝试搜索节点名称")
    print("□ 检查节点分类")
    
    return success

if __name__ == "__main__":
    main()