import os
import datetime
import fnmatch # 用于匹配文件名模式，例如 *.pyc

def scan_project_to_txt(
    project_root_dir,
    output_filename="project_scan_report.txt",
    exclude_items=None # 列表，包含要排除的目录名、文件名或文件名模式
):
    """
    扫描指定项目目录，将项目结构和文件内容输出到文本文件。

    Args:
        project_root_dir (str): 项目的根目录路径。
        output_filename (str): 输出的文本文件名。
        exclude_items (list): 一个列表，包含要排除的目录名、文件名或文件名模式。
                              例如：['.git', '__pycache__', 'env', '*.log', 'uploads/']
                              目录需要以 '/' 结尾，或者直接是目录名。
                              文件可以是完整的文件名或使用通配符（如 *.txt）。
    """
    if exclude_items is None:
        exclude_items = []

    # 默认排除一些常见的开发相关文件/目录
    default_excludes = [
        '.git',                 # Git 版本控制目录
        '__pycache__',          # Python 编译缓存
        'env',                  # 虚拟环境目录
        'venv',                 # 虚拟环境目录 (另一种常见命名)
        'node_modules',         # Node.js 依赖
        '.DS_Store',            # macOS 特有文件
        '*.pyc',                # Python 编译文件
        '*.log',                # 日志文件
        '*.bak',                # 备份文件
        '*.tmp',                # 临时文件
        output_filename         # 确保不扫描自身输出文件
    ]
    exclude_items.extend(default_excludes)
    # 将排除列表中的目录名标准化，以便更好地匹配
    exclude_items = [item.rstrip(os.sep) for item in exclude_items]


    # 规范化根目录路径
    project_root_dir = os.path.abspath(project_root_dir)

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.write(f"--- Project Scan Report: {os.path.basename(project_root_dir)} ---\n\n")
        outfile.write(f"Scan Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        outfile.write(f"Root Directory: {project_root_dir}\n")
        outfile.write(f"Excluded Items (user defined + default): {exclude_items}\n\n")
        outfile.write("-" * 80 + "\n\n")

        # 使用 os.walk 遍历目录树
        for dirpath, dirnames, filenames in os.walk(project_root_dir, topdown=True):
            # 获取当前目录相对于项目根目录的路径
            relative_dirpath = os.path.relpath(dirpath, project_root_dir)
            if relative_dirpath == ".":
                relative_dirpath = "" # 根目录本身不带前缀

            # 计算当前目录的缩进级别
            indent_level = relative_dirpath.count(os.sep) if relative_dirpath else 0
            current_indent = "  " * indent_level

            # --- 排除目录处理 ---
            # 必须在 os.walk 的 topdown=True 模式下修改 dirnames，
            # 这样 os.walk 就不会进入这些被移除的目录。
            dirnames_copy = dirnames[:] # 复制一份，因为我们要在循环中修改原列表
            for dname in dirnames_copy:
                full_relative_path_for_dir = os.path.join(relative_dirpath, dname).replace('\\', '/') # 统一斜杠
                
                should_exclude_dir = False
                for exclude_item in exclude_items:
                    # 如果排除项是目录名（不含路径），且是当前目录的直接子目录
                    if exclude_item == dname:
                        should_exclude_dir = True
                        break
                    # 如果排除项是相对路径（如 "env/subdir"）
                    if full_relative_path_for_dir == exclude_item:
                         should_exclude_dir = True
                         break
                    # 如果排除项是完整目录路径（如 "uploads"），并且它是当前目录的直接子目录
                    if full_relative_path_for_dir == exclude_item:
                        should_exclude_dir = True
                        break
                    # 匹配以 '/' 结尾的目录，例如 'uploads/'
                    if exclude_item.endswith('/') and full_relative_path_for_dir == exclude_item.rstrip('/'):
                        should_exclude_dir = True
                        break

                if dname.startswith('.'): # 默认排除所有隐藏目录
                     should_exclude_dir = True
                     
                if should_exclude_dir:
                    outfile.write(f"{current_indent}🚫 SKIPPING DIRECTORY: {dname}/\n")
                    dirnames.remove(dname) # 阻止 os.walk 进入此目录
                    continue

            # --- 写入当前目录结构 ---
            if relative_dirpath: # 根目录不作为子目录显示
                outfile.write(f"{current_indent}📁 {os.path.basename(dirpath)}/\n")

            # --- 文件处理 ---
            for filename in filenames:
                full_relative_path_for_file = os.path.join(relative_dirpath, filename).replace('\\', '/') # 统一斜杠
                
                should_exclude_file = False
                for exclude_item in exclude_items:
                    # 精确匹配文件名
                    if exclude_item == filename:
                        should_exclude_file = True
                        break
                    # 精确匹配相对路径文件
                    if full_relative_path_for_file == exclude_item:
                        should_exclude_file = True
                        break
                    # 使用 fnmatch 匹配模式，如 *.pyc
                    if fnmatch.fnmatch(filename, exclude_item):
                        should_exclude_file = True
                        break
                
                if filename.startswith('.'): # 默认排除所有隐藏文件
                    should_exclude_file = True

                if should_exclude_file:
                    outfile.write(f"{current_indent}  🚫 SKIPPING FILE: {filename}\n")
                    continue

                # 写入文件结构和内容
                file_indent = "  " * (indent_level + 1)
                outfile.write(f"{file_indent}📄 {filename}\n")
                outfile.write(f"{file_indent}{'=' * 60}\n") # 分隔线

                try:
                    filepath = os.path.join(dirpath, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        outfile.write(content)
                        if not content.endswith('\n'): # 确保文件内容后有一个换行符
                            outfile.write('\n')
                except UnicodeDecodeError:
                    outfile.write(f"[WARNING] Could not decode '{filename}' as UTF-8. It might be a binary file or have a different encoding. Content skipped.\n")
                except Exception as e:
                    outfile.write(f"[ERROR] Could not read '{filename}': {e}. Content skipped.\n")
                
                outfile.write(f"{file_indent}{'=' * 60}\n\n")

    print(f"\nScan complete! Report saved to '{output_filename}'")
    print(f"Project root scanned: '{project_root_dir}'")

# --- 使用示例 ---
if __name__ == "__main__":
    # 请将 'PROJECT_ROOT' 替换为你的项目根目录的实际路径
    # 如果脚本放在项目根目录，可以使用 '.'
    PROJECT_ROOT = "." 
    OUTPUT_FILE = "project_scan_report.txt"

    # 你可以手动添加要排除的目录或文件
    # 例如：
    # - 'env' 排除名为 'env' 的目录
    # - 'uploads/' 排除名为 'uploads' 的目录 (注意斜杠，表示目录)
    # - '01modeltest.py' 排除特定文件
    # - '*.json' 排除所有 .json 文件 (如果你不想看到 commands.json)
    # 默认已经排除了 .git, __pycache__, env, venv, .DS_Store, *.pyc, *.log 等
    
    custom_excludes = [
        # 根据你提供的目录结构，你可能想排除：
        # '01modeltest.py',
        # '02demo.py',
        # '04demomistralai.py',
        # 'uploads', # 排除整个 uploads 目录
        # 'commands.json', # 排除 commands.json 文件
        # 'README.en.md', # 排除英文 README
        # 'config.yml', # 排除配置文件
    ]

    scan_project_to_txt(
        project_root_dir=PROJECT_ROOT,
        output_filename=OUTPUT_FILE,
        exclude_items=custom_excludes
    )
