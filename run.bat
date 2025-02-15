@echo off
echo 正在激活 Python 虚拟环境...
call venv\Scripts\activate

echo 启动自动选课程序...
python auto_select_course.py

echo 选课程序已结束！
pause
