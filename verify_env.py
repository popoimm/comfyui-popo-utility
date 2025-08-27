#!/usr/bin/env python3
"""
ComfyUI Popo Utility - 开发环境验证脚本
验证Python 3.12.9环境是否正确配置
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("🐍 Python版本检查")
    print("-" * 30)
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"当前Python版本: {version_str}")
    print(f"Python路径: {sys.executable}")
    
    if version.major == 3 and version.minor == 12:
        print("✅ Python 3.12 - 符合要求")
        if version.micro == 9:
            print("✅ Python 3.12.9 - 完美匹配ComfyUI环境")
        else:
            print(f"⚠️  Python 3.12.{version.micro} - 与ComfyUI的3.12.9略有差异")
        return True
    else:
        print(f"❌ Python {version_str} - 需要Python 3.12.x")
        return False

def check_virtual_environment():
    """检查虚拟环境"""
    print("\n📦 虚拟环境检查")
    print("-" * 30)
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ 在虚拟环境中运行")
        print(f"虚拟环境路径: {sys.prefix}")
        return True
    else:
        print("⚠️  未在虚拟环境中运行")
        print("建议: 使用虚拟环境以避免依赖冲突")
        return False

def check_dependencies():
    """检查关键依赖"""
    print("\n📚 依赖包检查")
    print("-" * 30)
    
    dependencies = {
        'torch': '>=1.12.0',
        'torchvision': '>=0.13.0', 
        'numpy': '>=1.20.0',
        'PIL': '>=8.0.0'
    }
    
    all_ok = True
    
    for package, min_version in dependencies.items():
        try:
            if package == 'PIL':
                import PIL
                version = PIL.__version__
                module_name = 'Pillow'
            elif package == 'torchvision':
                # 特殊处理torchvision，因为可能有lzma依赖问题
                try:
                    import torchvision
                    version = torchvision.__version__
                    module_name = package
                except ImportError as e:
                    if '_lzma' in str(e):
                        print(f"⚠️  {package}: 已安装但lzma库缺失 (不影响ComfyUI使用)")
                        continue
                    else:
                        raise e
            else:
                module = __import__(package)
                version = module.__version__
                module_name = package
                
            print(f"✅ {module_name}: {version}")
        except ImportError:
            print(f"❌ {package}: 未安装")
            all_ok = False
        except AttributeError:
            print(f"⚠️  {package}: 已安装但无法获取版本信息")
    
    return all_ok

def check_comfyui_compatibility():
    """检查ComfyUI兼容性"""
    print("\n🎨 ComfyUI兼容性检查")
    print("-" * 30)
    
    try:
        # 测试插件导入
        import __init__ as plugin
        print("✅ 插件主模块导入成功")
        
        # 检查节点注册
        if hasattr(plugin, 'NODE_CLASS_MAPPINGS'):
            node_count = len(plugin.NODE_CLASS_MAPPINGS)
            print(f"✅ 节点注册成功: {node_count} 个节点")
            
            # 列出注册的节点
            for name, display_name in plugin.NODE_DISPLAY_NAME_MAPPINGS.items():
                print(f"   - {display_name} ({name})")
        else:
            print("❌ 节点映射未找到")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ 插件导入失败: {e}")
        return False

def check_project_structure():
    """检查项目结构"""
    print("\n📁 项目结构检查")
    print("-" * 30)
    
    required_files = [
        '__init__.py',
        'pyproject.toml',
        'README.md',
        '.python-version',
        'nodes/__init__.py',
        'nodes/base_node.py',
        'nodes/registry.py',
        'nodes/image_utils.py'
    ]
    
    all_exist = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 缺失")
            all_exist = False
    
    return all_exist

def check_git_status():
    """检查Git状态"""
    print("\n📝 Git状态检查")
    print("-" * 30)
    
    try:
        # 检查是否在Git仓库中
        result = subprocess.run(['git', 'status'], 
                              capture_output=True, text=True, check=True)
        print("✅ Git仓库状态正常")
        
        # 检查远程仓库
        result = subprocess.run(['git', 'remote', '-v'], 
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("✅ 远程仓库已配置")
            for line in result.stdout.strip().split('\n'):
                if 'origin' in line and 'fetch' in line:
                    print(f"   - {line.strip()}")
        else:
            print("⚠️  未配置远程仓库")
        
        return True
        
    except subprocess.CalledProcessError:
        print("❌ Git检查失败")
        return False

def main():
    """主检查函数"""
    print("🔍 ComfyUI Popo Utility 开发环境验证")
    print("=" * 50)
    
    checks = [
        ("Python版本", check_python_version),
        ("虚拟环境", check_virtual_environment), 
        ("依赖包", check_dependencies),
        ("项目结构", check_project_structure),
        ("ComfyUI兼容性", check_comfyui_compatibility),
        ("Git状态", check_git_status),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name}检查失败: {e}")
            results.append((check_name, False))
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 检查结果总结")
    print("-" * 30)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{check_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项检查通过")
    
    if passed == total:
        print("\n🎉 恭喜！开发环境配置完全正确！")
        print("🚀 你可以开始开发ComfyUI节点了！")
    else:
        print(f"\n⚠️  还有 {total - passed} 项需要解决")
        print("💡 请参考上面的错误信息进行修复")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)