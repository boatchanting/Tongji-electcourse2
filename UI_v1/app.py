# 导入python库
import os
import uuid
import logging
import queue
import threading
import webview
import multiprocessing
from multiprocessing import Process, Queue
from logging.handlers import QueueHandler,RotatingFileHandler
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import hashlib
import requests
import logging
# 导入自定义库
from download_webdriver import init_edge_driver, test_driver_health  # init_edge_driver自动管理webriver的版本和下载，test_driver_health测试驱动是否可用
from core.tongji import auto_elect_course_tongji

def run_with_queue(log_queue, username, password, course_number, max_retries):
    """
    在子进程里把所有 logging 输出发到 log_queue。
    """
    # 1) 用 QueueHandler 接管 root logger
    qh = QueueHandler(log_queue)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(qh)

    # 2) 调用原始自动选课函数
    auto_elect_course_tongji(username, password, course_number, max_retries)

class Api:
    def __init__(self):
        self.username = None
        self.password = None
        self.tasks = {}
        # tasks: {
        #   task_id: {
        #     'process': Process,
        #     'log_queue': Queue,
        #     'logs': [str, ...],
        #     'listener': Thread,
        #     'course_number': str,
        #     'max_retries': int
        #   }
        # }

    # ---- 1.登录/选课任务管理API ----
    def login(self, username, password):
        self.username = username
        self.password = password
        return True

    def add_task(self, course_number, max_retries):
        tid = str(uuid.uuid4())
        self.tasks[tid] = {
            'process': None,
            'log_queue': Queue(),
            'logs': [],
            'listener': None,
            'course_number': course_number,
            'max_retries': int(max_retries)
        }
        return tid

    def start_task(self, task_id):
        task = self.tasks.get(task_id)
        if not task:
            return False
        # 如果已经运行中，忽略
        if task['process'] and task['process'].is_alive():
            return False

        # 启动日志监听线程
        listener = threading.Thread(
            target=self._log_listener,
            args=(task_id,),
            daemon=True
        )
        listener.start()
        task['listener'] = listener

        # 启动选课子进程
        p = Process(
            target=run_with_queue,
            args=(
                task['log_queue'],
                self.username,
                self.password,
                task['course_number'],
                task['max_retries']
            )
        )
        p.daemon = True
        p.start()
        task['process'] = p
        return True

    def stop_task(self, task_id):
        task = self.tasks.get(task_id)
        if not task or not task['process']:
            return False
        if task['process'].is_alive():
            task['process'].terminate()
            task['process'].join()
        task['process'] = None
        return True

    def get_tasks(self):
        """
        返回所有任务及其状态，供前端展示
        """
        out = []
        for tid, t in self.tasks.items():
            status = 'running' if t['process'] and t['process'].is_alive() else 'stopped'
            out.append({
                'id': tid,
                'course_number': t['course_number'],
                'max_retries': t['max_retries'],
                'status': status
            })
        return out
    
    def delete_task(self, task_id):
        """
        停止并删除指定的任务
        """
        task = self.tasks.pop(task_id, None)
        if not task:
            return False
        # 如果进程还在运行，先终止它
        p = task.get('process')
        if p and p.is_alive():
            p.terminate()
            p.join()
        return True

    # ---- 2.日志接口API ----
    def get_logs(self, task_id):
        """
        前端定时轮询，拉取到目前为止所有新日志
        """
        task = self.tasks.get(task_id)
        if not task:
            return []
        new_logs = task['logs'][:]
        task['logs'].clear()
        return new_logs

    def _log_listener(self, task_id):
        """
        后台线程：不断从 Queue 里取 LogRecord，
        加上毫秒级时间戳后，存到内存
        v1.2.1 修复内存泄露
        """
        task = self.tasks[task_id]
        q = task['log_queue']
        while True:
            try:
                record = q.get(timeout=0.5)
                # 格式化时间：时:分:秒.毫秒
                ts = datetime.fromtimestamp(record.created).strftime('%H:%M:%S.%f')[:-3]
                task['logs'].append(f"[{ts}] {record.getMessage()}")
                
                # 保持日志列表最多只有100条记录
                if len(task['logs']) > 100:
                    task['logs'].pop(0)
            except queue.Empty:
                # 如果子进程已结束，读完剩余再退出
                if not task['process'] or not task['process'].is_alive():
                    while True:
                        try:
                            record = q.get_nowait()
                            ts = datetime.fromtimestamp(record.created).strftime('%H:%M:%S.%f')[:-3]
                            task['logs'].append(f"[{ts}] {record.getMessage()}")
                            
                            # 保持日志列表最多只有100条记录
                            if len(task['logs']) > 100:
                                task['logs'].pop(0)
                        except queue.Empty:
                            break
                    break
    
    # ---- 3.版本信息API ----
    def get_version(self):
        """
        获取软件当前版本号
        
        Returns:
            dict: 包含版本信息的字典
        """
        return {
            "version": "Tongji-electcourse2v1.3.1",
            "build_date": "2025-9-12",  # 构建日期
            "api_version": "1.3.1", # API 版本
            "ui_version": "1.3.0+", # UI 版本
            "status": "stable"# 可以是 'alpha', 'beta', 'stable' 等
        }
    
    # ---- 4. 测试浏览器驱动API ----
    def test_browser_driver(self):
        """
        测试浏览器驱动是否正常
        返回示例：
        {
            "success": true,
            "browser_version": "128.0.2750.99",
            "driver_version": "128.0.2750.99",
            "message": "...",
            "error": null
        }
        """
        return test_driver_health()

def check_url_accessible(url):
    """
    检查给定的 URL 是否可访问。
    :param url: 要检查的 URL
    :return: 如果 URL 可访问，返回 True，否则返回 False
    """
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False
    
if __name__ == '__main__':
    multiprocessing.freeze_support() # 用于打包成 exe, 必须放在所有代码的最前面, 否则会报错
    multiprocessing.set_start_method('spawn', force=True)
    api = Api()

    # 本地页面路径
    local_index = os.path.abspath(os.path.join(os.path.dirname(__file__), 'system-scheduler.html'))
    local_404 = os.path.abspath(os.path.join(os.path.dirname(__file__), '404.html'))

    # 远程页面地址
    remote_url = 'https://boatchanting.github.io/Tongji-electcourse2/UI_v1/system.html'

    #检查远程地址是否可访问
    if check_url_accessible(remote_url):
        final_url = remote_url
    else:
        final_url = f'file://{local_404}'  # fallback 到404页面

    # 创建窗口
    window = webview.create_window(
        title='Tongji-electcourse2-v1.3.1',
        url=final_url,
        js_api=api,
        width=850,
        height=700
    )
    webview.start()
