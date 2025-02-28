<div align="center">
  <h1 style="font-family: 'Arial', sans-serif; color: #333;">Tongji Electcourse</h1>
  <p style="font-size: 1.2rem; color: #777;">使用 Selenium 库实现自动选课功能</p>
  <img src="https://boatchanting.github.io/Tongji-electcourse2/icon/logo.png" width="300" alt="Logo">
</div>

<div align="center">
  <p>本项目使用 `Selenium` 库及 webdriver 实现自动选课功能，适配学校选课网站。它能够自动登录、选择课程，并进行选课操作。</p>
</div>

<div align="center">
  <h3>🌟🌟🌟直接看release下载exe可执行文件</h3>
  <a href="https://github.com/boatchanting/Tongji-electcourse2/releases">
    <button style="background-color: #007BFF; color: white; border: none; padding: 10px 20px; font-size: 1.2rem; border-radius: 5px; cursor: pointer;">
      我要下载
    </button>
  </a>
</div>

<div align="center">
  <h4>v0.2.0版本截图</h4>
  <img src="https://boatchanting.github.io/Tongji-electcourse2/img/example_v0.2.0.png" width="400" alt="v0.2.0 Screenshot">
</div>

<div align="center">
  <h4>v0.1.1版本截图</h4>
  <img src="https://boatchanting.github.io/Tongji-electcourse2/example.png" width="600" alt="v0.1.1 Screenshot">
</div>


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


## 环境配置（快速）
1. 下载/克隆本项目到本地：
   ```sh
   git clone https://github.com/boatchanting/Tongji-electcourse2.git
   cd your-path
   ```
2. 运行 `setup_env.bat` 配置环境（Windows）。
3. 运行 `run.bat` 启动程序。

## 环境配置
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
python auto_select_course.py
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




