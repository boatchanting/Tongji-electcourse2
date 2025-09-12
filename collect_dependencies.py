#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖收集工具
用于扫描项目中的Python文件，提取所有导入的外部库，并生成requirements.txt文件
"""

import os
import re
import sys
import importlib.util
from pathlib import Path

# 内置模块列表（不需要在requirements.txt中声明的模块）
BUILTIN_MODULES = {
    'os', 'sys', 'io', 'json', 'xml', 'csv', 'datetime', 'time', 'collections',
    'math', 'random', 'hashlib', 'uuid', 'logging', 'threading', 'multiprocessing',
    'queue', 'subprocess', 'platform', 're', 'zipfile', 'shutil', 'tempfile',
    'socket', 'urllib', 'http', 'argparse', 'configparser', 'typing',
    'inspect', 'ast', 'enum', 'itertools', 'functools', 'operator'
}

# 项目内部模块前缀（根据项目结构调整）
INTERNAL_MODULE_PREFIXES = {
    'download_webdriver', 'core', 'autoelect'
}

class DependencyCollector:
    def __init__(self, project_root):
        """初始化依赖收集器"""
        self.project_root = Path(project_root)
        self.dependencies = set()
        self.import_pattern = re.compile(r'^\s*(?:import|from)\s+([\w\.]+)')
        self.from_import_pattern = re.compile(r'^\s*from\s+([\w\.]+)\s+import')
        
    def is_internal_module(self, module_name):
        """判断是否为项目内部模块"""
        for prefix in INTERNAL_MODULE_PREFIXES:
            if module_name.startswith(f'{prefix}.') or module_name == prefix:
                return True
        return False
    
    def is_builtin_module(self, module_name):
        """判断是否为Python内置模块"""
        # 处理带点的模块名，只取第一个部分
        base_module = module_name.split('.')[0]
        return base_module in BUILTIN_MODULES
    
    def collect_from_file(self, file_path):
        """从单个Python文件中收集依赖"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # 跳过注释行
                    if line.strip().startswith('#'):
                        continue
                    
                    # 处理import语句
                    import_match = self.import_pattern.match(line)
                    if import_match:
                        module_name = import_match.group(1)
                        if not self.is_builtin_module(module_name) and not self.is_internal_module(module_name):
                            self.dependencies.add(module_name.split('.')[0])  # 只取主模块名
                    
                    # 处理from...import语句
                    from_import_match = self.from_import_pattern.match(line)
                    if from_import_match:
                        module_name = from_import_match.group(1)
                        if not self.is_builtin_module(module_name) and not self.is_internal_module(module_name):
                            self.dependencies.add(module_name.split('.')[0])  # 只取主模块名
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}", file=sys.stderr)
    
    def collect_all(self):
        """扫描整个项目收集依赖"""
        print(f"正在扫描项目: {self.project_root}")
        
        # 遍历项目中的所有Python文件
        for root, _, files in os.walk(self.project_root):
            # 跳过某些目录（可根据需要调整）
            if '.git' in root or 'venv' in root or '__pycache__' in root:
                continue
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self.collect_from_file(file_path)
        
        return self.dependencies
    
    def update_requirements(self, requirements_file='requirements.txt'):
        """更新requirements.txt文件"""
        requirements_path = self.project_root / requirements_file
        
        # 读取现有的requirements.txt
        existing_deps = {}
        if requirements_path.exists():
            with open(requirements_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # 处理带版本号的依赖
                        if '==' in line or '>=' in line or '<=' in line or '~=' in line:
                            parts = re.split(r'[=<>~]+', line, 1)
                            module_name = parts[0].strip()
                            version = line[len(module_name):].strip()
                            existing_deps[module_name] = version
                        else:
                            existing_deps[line] = ''
        
        # 添加新发现的依赖
        for dep in self.dependencies:
            if dep not in existing_deps:
                existing_deps[dep] = ''
        
        # 写入更新后的requirements.txt
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write("# 项目依赖库列表\n")
            f.write("# 由依赖收集工具自动生成和更新\n\n")
            
            # 按照字母顺序排序
            for dep, version in sorted(existing_deps.items()):
                f.write(f"{dep}{version}\n")
        
        print(f"已更新 {requirements_path}")
        print(f"共收集到 {len(self.dependencies)} 个外部依赖库")
        print(f"依赖列表: {', '.join(sorted(self.dependencies))}")

if __name__ == '__main__':
    # 获取项目根目录（默认为当前目录）
    project_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    
    # 创建依赖收集器并执行收集
    collector = DependencyCollector(project_dir)
    collector.collect_all()
    collector.update_requirements()

    # 提示用户如何安装依赖
    print("\n安装依赖命令:")
    print(f"pip install -r {os.path.join(project_dir, 'requirements.txt')}")