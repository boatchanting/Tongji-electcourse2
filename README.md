<div align="center">
  <h1 style="font-family: 'Arial', sans-serif; color: #333;">Tongji Electcourse</h1>
  <p style="font-size: 1.2rem; color: #777;">轻松、高效、透明 —— 自动选课，解放双手！</p>
  <img src="https://boatchanting.github.io/Tongji-electcourse2/icon/logo.png" width="300" alt="Logo">
</div>
<!-- 添加一些徽章 -->
<div align="center">
  <a href="https://github.com/boatchanting/Tongji-electcourse2/releases"><img src="https://img.shields.io/github/downloads/boatchanting/Tongji-electcourse2/total" alt="Total Downloads"></a>
  <a href="https://github.com/boatchanting/Tongji-electcourse2/issues"><img src="https://img.shields.io/github/issues/boatchanting/Tongji-electcourse2" alt="Open Issues"></a>
  <a href="https://github.com/boatchanting/Tongji-electcourse2/releases"><img src="https://img.shields.io/github/v/release/boatchanting/Tongji-electcourse2?style=flat-square&label=Version" alt="Version"></a>
  <a href="https://www.python.org/downloads/release/python-3100/"><img src="https://img.shields.io/badge/Python-%3E%3D3.10-blue?style=flat-square" alt="Python Version"></a>
  <a href="https://github.com/boatchanting/Tongji-electcourse2/graphs/contributors"><img src="https://img.shields.io/github/contributors/boatchanting/Tongji-electcourse2?style=flat-square" alt="Contributors"></a>
</div>
<div align="center">
  <p>本项目使用Selenium及webdriver实现自动选课功能，适配各大学校选课网站(暂完成TJ适配)。它能够模拟你的选课操作自动登录、选择课程，且软件安全友好，免安装一键运行。</p>
</div>

[🔗v1版本发布页](https://boatchanting.github.io/Tongji-electcourse2/UI_v1/introduction.html)

## 界面预览
|                                                                                                                                |                                                                                               |
| :----------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------: |
|                  ![](https://raw.githubusercontent.com/boatchanting/Tongji-electcourse2/main/UI_v1/img/p1.png)                 | ![](https://raw.githubusercontent.com/boatchanting/Tongji-electcourse2/main/UI_v1/img/p2.png) |
|                  ![](https://raw.githubusercontent.com/boatchanting/Tongji-electcourse2/main/UI_v1/img/p3.png)                 | ![](https://raw.githubusercontent.com/boatchanting/Tongji-electcourse2/main/UI_v1/img/p4.png) |
| <img src="https://raw.githubusercontent.com/boatchanting/Tongji-electcourse2/main/UI_v1/img/p5.png" alt="主题切换示例" width="100%"> |                                                                                               |

> **图 1‑5**：自动选课系统展示

<h3>功能特点</h3>
<ul style="list-style: none; padding: 0;">
  <li>✅ 自动登录选课网站</li>
  <li>✅ 通过学号和密码进行身份验证</li>
  <li>✅ 自动定位并选择指定课程</li>
  <li>✅ 结果反馈，确认选课是否成功</li>
  <li>✅ 不用守在电脑前，可以做其他事情</li>
  <li>✅ 选课自动化展示，用户可以实时查看选课过程</li>
  <li>✅ 选课日志展示</li>
</ul>

## 常见问题 (Q&A)

### 1. 这个程序只是代替鼠标进行点击操作吗？
是的，但是其可以自动运行并支持后台运行，并有实时展示以及所有过程的日志信息，想去干什么事情都是可以滴~

---

### 2. 程序本身是本地运行吗？
是的，本程序完全本地运行。

---

### 3. 会不会导致信息泄露？
不会，本程序完全本地运行，信息仅用于选课系统的身份验证，并不会上传您的信息。如果您对此不放心的话，也可以查看源代码或自行根据源代码运行本程序。

---

### 4. 可以同时选择多门课程吗？
当然可以，v1.0.0 + 版本具有该功能!

---

### 5. 如何确保程序的稳定性？
程序经过多次测试，确保在大多数情况下能够稳定运行。如果遇到问题，可以通过查看日志信息定位问题，或者提交[Issues](https://github.com/boatchanting/Tongji-electcourse2/issues)寻求帮助。

---

### 6. 是否需要安装额外的浏览器驱动？
默认情况下，程序使用Edge浏览器。如果系统未自带Edge WebDriver，您需要手动安装并配置环境变量。具体步骤请参考[Edge WebDriver下载页面](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)。

---

### 7. 如何更新到最新版本？
您可以直接从[Releases页面](https://github.com/boatchanting/Tongji-electcourse2/releases)下载最新版本的可执行文件，或者通过Git拉取最新代码：
```bash
git pull origin main
```
## 环境配置（新版）

暂时没有写，以后补上...

## 环境配置（老版）（快速）
1. 下载/克隆本项目到本地：
   ```sh
   git clone https://github.com/boatchanting/Tongji-electcourse2.git
   cd your-path
   ```
2. 运行 `setup_env.bat` 配置环境（Windows）。
3. 运行 `run.bat` 启动程序。

## 环境配置（老版）
### 1. 创建虚拟环境并安装 Python 依赖
本项目依赖 `Selenium`，请先确保你已经安装 Python，并使用以下命令安装必要的依赖：
```sh
pip install -r requirements.txt
```
或手动安装：
```sh
pip install selenium==4.25.0 PyQt5==5.15.11
```

### 2. 配置 WebDriver（可以略过，大多数windows电脑默认自带，出现问题再来配置这一步）
本程序默认使用 `Edge` 浏览器，需要安装 [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) 并将其路径加入系统环境变量。

### 3. 运行程序
执行以下命令启动程序：
```sh
python auto_elect_course.py
```

## 其他说明
```
1. 本程序仅供学习和交流使用，请勿用于非法用途。
2. 在使用过程中，所有的操作和行为都运行在您的**本地环境**中，我们不会收集、存储或上传任何个人信息。
3. 用户在使用本程序时，应自行承担由此产生的一切后果和责任，包括但不限于数据丢失、系统故障、个人信息泄露等。
4. 本程序不提供任何形式的担保，包括但不限于对程序的适用性、准确性和完整性的担保。
5. 本程序的开发者和分发者不承担因使用本程序而引起的任何直接或间接损失和责任。
6. 用户在使用本程序时，应遵守当地法律法规，不得利用本程序从事任何违法活动。
7. 本程序中的任何更新、修改或终止，开发者有权不事先通知用户。
8. 用户使用本程序即表示同意上述所有条款。
```




