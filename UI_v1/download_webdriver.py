import os
import platform
import re
import subprocess
import sys
import zipfile
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service


def get_edge_version():
    """自动获取 Edge 浏览器版本"""
    system = platform.system()
    try:
        if system == "Windows":
            cmd = r'reg query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                output = result.stdout.strip()
                match = re.search(r"version\s+REG_SZ\s+(.+)", output)
                if match:
                    return match.group(1)

            edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            if not os.path.exists(edge_path):
                edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

            result = subprocess.run([edge_path, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                match = re.search(r"Microsoft Edge\s+([\d.]+)", result.stdout)
                if match:
                    return match.group(1)

        elif system in ("Linux", "Darwin"):
            result = subprocess.run(["microsoft-edge", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                result = subprocess.run(["/opt/microsoft/msedge/microsoft-edge", "--version"], capture_output=True, text=True)

            if result.returncode == 0:
                match = re.search(r"Microsoft Edge\s+([\d.]+)", result.stdout)
                if match:
                    return match.group(1)
    except Exception as e:
        print(f"获取 Edge 版本失败: {e}")

    raise RuntimeError("无法获取 Edge 浏览器版本，请确认 Edge 已安装。")


def download_edgedriver(version, driver_dir="./webdriver"):
    """下载并解压对应版本的 Edge WebDriver（保存到 ./webdriver 目录）"""
    system = platform.system()
    machine = platform.machine().lower()

    if system == "Windows":
        platform_name = "win64" if machine == "amd64" else "win32"
    elif system == "Linux":
        platform_name = "linux64"
    elif system == "Darwin":
        platform_name = "mac64" if machine == "x86_64" else "mac-arm64"
    else:
        raise RuntimeError(f"不支持的系统: {system}")

    # 修正 URL：移除多余空格
    base_url = f"https://msedgedriver.microsoft.com/{version}/edgedriver_{platform_name}.zip"

    zip_path = os.path.join(driver_dir, f"edgedriver_{version}.zip")
    driver_exe = "msedgedriver.exe" if system == "Windows" else "msedgedriver"
    driver_path = os.path.join(driver_dir, driver_exe)
    version_file = os.path.join(driver_dir, "VERSION")

    os.makedirs(driver_dir, exist_ok=True)

    # 如果驱动已存在且版本文件匹配，跳过下载
    if os.path.exists(driver_path) and os.path.exists(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            recorded_version = f.read().strip()
        if recorded_version == version:
            print(f"驱动已存在且版本匹配: {driver_path} (v{version})")
            return driver_path

    print(f"正在下载 EdgeDriver {version} for {platform_name} 到 {driver_dir}...")
    try:
        response = requests.get(base_url, timeout=30)
        response.raise_for_status()

        with open(zip_path, "wb") as f:
            f.write(response.content)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(driver_dir)

        if system != "Windows":
            os.chmod(driver_path, 0o755)

        os.remove(zip_path)

        # ✅ 记录版本号到 VERSION 文件
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(version)

        print(f"✅ 驱动下载并解压成功: {driver_path}")
        return driver_path

    except Exception as e:
        raise RuntimeError(f"下载 EdgeDriver 失败: {e}")


def init_edge_driver(headless=False):
    """自动初始化 Edge WebDriver"""
    try:
        version = get_edge_version()
        print(f"检测到 Edge 浏览器版本: {version}")

        driver_path = download_edgedriver(version)  # 内部已包含版本校验和重装逻辑

        from selenium.webdriver.edge.options import Options
        edge_options = Options()

        if headless:
            edge_options.add_argument("--headless=new")
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            edge_options.add_argument("--disable-gpu")
            edge_options.add_argument("--window-size=1920,1080")

        service = Service(executable_path=driver_path)
        driver = webdriver.Edge(service=service, options=edge_options)

        print("✅ Edge WebDriver 启动成功！")
        return driver

    except Exception as e:
        print(f"❌ 启动 Edge 失败: {e}")
        raise


# if __name__ == "__main__":
#     try:
#         driver = init_edge_driver(headless=False)
#         driver.get("https://www.baidu.com")
#         print("页面标题:", driver.title)

#         input("按回车关闭浏览器...")
#         driver.quit()

#     except Exception as e:
#         print(f"程序异常退出: {e}")
#         sys.exit(1)