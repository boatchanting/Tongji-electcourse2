# 自动化选课脚本

本项目使用 `Selenium` 库实现自动选课功能，适配学校选课网站。它能够自动登录、选择课程，并进行选课操作。

## 直接看release下载使用方法

v0.1.1版本截图
<div align="center">
  <img src="https://raw.githubusercontent.com/boatchanting/Tongji-electcourse2/main/example.png" width="600">
</div>

## 功能特点
- 自动登录选课网站
- 通过学号和密码自动进行学校系统身份验证
- 自动定位并选择指定课程
- 结果反馈，确认选课是否成功
- 不用守在电脑前，可以做其他事情

## 环境配置
### 1. 安装 Python 依赖
本项目依赖 `Selenium`，请先确保你已经安装 Python，并使用以下命令安装必要的依赖：
```sh
pip install -r requirements.txt
```

### 2. 配置 WebDriver（可以略过，大多数windows电脑默认自带，出现问题再来配置这一步）
本程序默认使用 `Edge` 浏览器，需要安装 [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) 并将其路径加入系统环境变量。


