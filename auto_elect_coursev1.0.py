import os
import uuid
import logging
import queue
import threading
import webview
import multiprocessing
from multiprocessing import Process, Queue
from logging.handlers import QueueHandler
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

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
    auto_elect_course(username, password, course_number, max_retries)

class Api:
    def __init__(self):
        self.username = None
        self.password = None
        self.tasks = {}
        # 返回格式：
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

    # ---- 登录/任务管理 ----
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

    # ---- 日志接口 ----
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
        """
        task = self.tasks[task_id]
        q = task['log_queue']
        while True:
            try:
                record = q.get(timeout=0.5)
                # 格式化时间：时:分:秒.毫秒
                ts = datetime.fromtimestamp(record.created).strftime('%H:%M:%S.%f')[:-3]
                task['logs'].append(f"[{ts}] {record.getMessage()}")
            except queue.Empty:
                # 如果子进程已结束，读完剩余再退出
                if not task['process'] or not task['process'].is_alive():
                    while True:
                        try:
                            record = q.get_nowait()
                            ts = datetime.fromtimestamp(record.created).strftime('%H:%M:%S.%f')[:-3]
                            task['logs'].append(f"[{ts}] {record.getMessage()}")
                        except queue.Empty:
                            break
                    break

# 初始化Edge浏览器
try:
    driver = webdriver.Edge()
    logging.info("Edge浏览器已启动")
except Exception as e:
    logging.error("无法启动Edge浏览器")
    raise e
# 高亮显示元素的函数
def highlight(element):
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                        element, "border: 2px solid red;")
    
def auto_elect_course(username, password, course_number, max_retries):
    """
    自动选课的主函数
    :param username: 学号
    :param password: 密码
    :param course_number: 课程编号
    :param max_retries: 最大重试次数
    """
    feedback = "，请检查页面是否正常或向开发者反馈:https://github.com/boatchanting/Tongji-electcourse2/issues"

    if (int(username)>0):# 简单检查学号是否可以使用
        course_name = course_number[:-2] # 课程类别由course_number去除后两位构成

        logging.info(f"用户输入的学号: {username}")
        logging.info(f"用户输入的课程编号: {course_number}")
        logging.info(f"课程类别: {course_name}")

        # 打开登录页面
        try:
            login_url = "https://1.tongji.edu.cn"  # 登录 URL
            driver.get(login_url)
            logging.info(f"打开1系统登录页面")
        except Exception as e:
            logging.error(f"无法打开1系统登录页面{feedback}")
            time.sleep(10)
            raise e

        # 使用WebDriverWait来等待元素出现
        try:
            wait = WebDriverWait(driver, 100)  # 最长等待时间为100秒

            # 定位用户名和密码输入框，并输入登录信息
            username_input = wait.until(EC.presence_of_element_located((By.ID, "j_username")))
            password_input = wait.until(EC.presence_of_element_located((By.ID, "j_password")))
            logging.info("定位用户名和密码输入框")

            # 填入用户名和密码
            username_input.send_keys(username)
            password_input.send_keys(password)
            logging.info("填入用户名和密码")

        except Exception as e:
            logging.error(f"用户名或密码输入错误{feedback}")
            time.sleep(10)
            raise e

        # 定位登录按钮并点击
        try:
            login_button = wait.until(EC.element_to_be_clickable((By.ID, "loginButton")))
            logging.info("点击登录按钮")
        except Exception as e:
            logging.error(f"找不到登录按钮{feedback}")
            time.sleep(10)
            raise e

        highlight(login_button)
        login_button.click()
        logging.info("点击登录按钮")

        #input("登录完成后，请按任意键继续...") #测试用
        time.sleep(3)

        # 等待登录过程完成
        wait.until(EC.url_changes(login_url))

        # 跳转界面https://1.tongji.edu.cn/studentElect
        try:
            driver.get("https://1.tongji.edu.cn/studentElect")
            logging.info("跳转选课界面")
        except Exception as e:
            logging.error(f"无法跳转选课界面{feedback}")
            time.sleep(10)
            raise e

        time.sleep(3)
        # 使用WebDriverWait来等待下一个元素出现
        # wait.until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "el-button--primary") and contains(span, "进入选课")]')))

        # 1.定位“进入选课”按钮并点击
        try:
            # 等待“进入选课”按钮出现
            wait = WebDriverWait(driver, 10)  # 最长等待时间为10秒
            wait.until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "el-button--primary") and contains(span, "进入选课")]')))
            enter_elect_button = driver.find_element(By.XPATH, '//button[contains(@class, "el-button--primary") and contains(span, "进入选课")]')
            highlight(enter_elect_button)  # 高亮“进入选课”按钮
            enter_elect_button.click()
            logging.info("1.点击“进入选课”按钮")
        except Exception as e:
            logging.error(f"1.找不到“进入选课”按钮{feedback}")
            time.sleep(10)
            raise e

        # 使用WebDriverWait来等待下一个元素出现
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[3]/div/div[3]/span/button')))

        # 2.定位“确定”按钮并点击 /html/body/div[1]/div[1]/div[1]/section/main/div/div[3]/div/div[3]/span/button
        try:
            confirm_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[3]/div/div[3]/span/button')
            highlight(confirm_button)  # 高亮“确定”按钮
            confirm_button.click()
            logging.info("2.点击“确定”按钮")
        except Exception as e:
            logging.error(f"2.找不到“确定”按钮{feedback}")
            time.sleep(10)
            raise e
        #input("进入选课界面后，请按任意键继续...") # 测试用

        # 3.定位“选择课程”按钮并点击
        try:
            wait = WebDriverWait(driver, 3)
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div[2]/button[1]')))
            logging.info("2.找到“选择课程”按钮")
            select_course_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div[2]/button[1]')
            highlight(select_course_button)  # 高亮“选择课程”按钮
            select_course_button.click()
            logging.info("3.点击“选择课程”按钮")
            # 调试用，暂停10s
            

        except Exception as e:
            logging.error(f"3.找不到“选择课程”按钮{feedback}")
            time.sleep(10)
            raise e

        # 4. 定位课程并添加到选课列表 (v0.2.1升级适配选修课)
        search_and_add_course(course_number, driver, wait, highlight)

        # 5.定位提交按钮元素并点击
        try:
            submit_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[4]/div/div[3]/span/button[2]')
            highlight(submit_button)  # 高亮提交按钮
            submit_button.click()
            logging.info("5.点击提交按钮")
        except Exception as e:
            logging.error(f"5.找不到提交按钮")
            raise e

        # input("进入选课界面后，请按任意键继续...") # 测试用
        #！！！需要优化的地方
        #logging.info("请检查课程是否已经被添加到选课列表中，如果没有请在一分钟内手动添加，如果已经添加请忽略")
        #for i in range(6):
        #    time.sleep(10)
        #    wait_time_checkcourse = (6 - i)*10
        #    logging.info(f"等待手动检查中...{wait_time_checkcourse}秒后结束")

        time.sleep(0.5)
        # 使用WebDriverWait来等待下一个元素出现
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[4]/div/div[3]/span/button[2]')))
        
        # 初始化重试机制
        max_retries = max_retries
        retries = 0
        success = False

        while not success and retries < max_retries:
            retries += 1
            logging.info(f"开始第 {retries} 次选课尝试")

            # 6. 定位课程并点击
            try:
                # 使用WebDriverWait来等待下一个元素出现
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, f'//td/div[contains(@class, "courseName") and contains(text(), "{course_name}")]')))
                course_element = driver.find_element(By.XPATH, f'//td/div[contains(@class, "courseName") and contains(text(), "{course_name}")]')
                highlight(course_element)  # 高亮含有课号的元素
                course_element.click()
                logging.info(f"已成功定位到课程编号为 {course_number} 的元素")
            except Exception as e:
                logging.error(f"找不到课程编号为 {course_number} 的元素: {e}")
                # 等待一段时间后重试
                sleep_time=random.randint(3,6)
                time.sleep(sleep_time)
                logging.info(f"等待{sleep_time}秒后重试")
                continue  # 进入下一个循环

            # 7. 选择目标课程
            try:
                # 目标课程编号
                target_course_number_full = course_number

                # 定位目标行的 <tr> 元素
                target_row = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, f'//tr[.//td[@class="courseName" and text()="{target_course_number_full}"]]')
                    )
                )
                logging.info(f"已成功定位到课程编号为 {target_course_number_full} 的行")

                # 滚动到目标行以确保可见
                driver.execute_script("arguments[0].scrollIntoView(true);", target_row)

                # 高亮显示目标行（可选，便于调试）
                driver.execute_script("arguments[0].setAttribute('style', 'border: 2px solid red;');", target_row)

                # 点击目标行
                target_row.click()
                logging.info(f"已点击课程编号为 {target_course_number_full} 的行")

            except Exception as e:
                logging.error(f"定位或点击课程编号为 {target_course_number_full} 的行时发生错误: {e}")
                # 等待一段时间后重试
                sleep_time=random.randint(3,6)
                time.sleep(sleep_time)
                logging.info(f"等待{sleep_time}秒后重试")
                continue  # 进入下一个循环

            # 8. 保存课表
            try:
                # 定位 "保存课表" 按钮
                save_button = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//button[@type="button" and contains(@class, "el-button--primary") and span[text()="保存课表"]]')
                    )
                )
                logging.info("已成功定位到 '保存课表' 按钮")

                # 高亮按钮（可选，便于调试）
                driver.execute_script("arguments[0].setAttribute('style', 'border: 2px solid red;');", save_button)

                # 点击按钮
                save_button.click()
                logging.info("已点击 '保存课表' 按钮")

            except Exception as e:
                logging.error(f"定位或点击 '保存课表' 按钮时发生错误: {e}")
                # 可选择在此处添加等待时间后重试
                time.sleep(2)
                continue  # 进入下一个循环

            # 等待保存操作完成
            time.sleep(1)

            # 9. 定位返回的信息并获取
            return_info_status = False # 初始化返回信息状态为False
            
            while not return_info_status:
                try:
                    # 定位结果框
                    wait = WebDriverWait(driver, 10)
                    result_dialog = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//div[@role="dialog" and @aria-label="结果"]'))
                    )
                    logging.info("结果对话框已定位")

                    # 定位到具体的结果信息内容
                    result_text = result_dialog.find_element(By.XPATH, './/div[@class="edu-dialog_body"]/div').text
                    logging.info(f"获取到的结果信息: {result_text}")

                    # 判断结果信息
                    if "选课成功" in result_text:
                        logging.info("检测到选课成功消息")
                        return_info_status = True  # 设置返回信息状态为True，退出循环
                        print(f"选课结果：{result_text}")

                        # 定位关闭按钮并点击
                        close_button = result_dialog.find_element(By.XPATH, './/button[contains(@class, "el-button--default") and span[text()="关闭"]]')
                        close_button.click()
                        logging.info("点击关闭按钮，退出程序")
                        success = True  # 设置成功标志，退出循环
                    elif "保存课程中" in result_text:
                        logging.info("检测到保存课程中消息，休息1秒后重新检测")
                        time.sleep(1)  # 休息1秒后重新检测
                    else:
                        logging.warning("未检测到选课成功消息")
                        print(f"选课结果：{result_text}")

                        # 定位关闭按钮并点击
                        close_button = result_dialog.find_element(By.XPATH, './/button[contains(@class, "el-button--default") and span[text()="关闭"]]')
                        close_button.click()
                        logging.info("点击关闭按钮，继续运行程序")

                        # 等待一段时间后重试
                        sleep_time = random.randint(3, 6)
                        time.sleep(sleep_time)
                        logging.info(f"等待{sleep_time}秒后重试")
                        return_info_status = True  # 设置返回信息状态为True，退出循环
                except Exception as e:
                    logging.error(f"发生错误: {e}")

        if not success:
            logging.error(f"在尝试了 {max_retries} 次后，仍未成功选课。请手动检查或稍后重试。")
            print(f"在尝试了 {max_retries} 次后，仍未成功选课。请手动检查或稍后重试。")
            input("按任意键退出程序...")
        else:
            logging.info("选课成功，程序结束。")

        # 关闭浏览器
        driver.quit()
    else:
        logging.info("拒绝使用！")

def search_and_add_course(course_number, driver, wait, highlight):
    # 4.1 定位课程并添加到选课列表：默认值（计划内课程） v0.2.1版本改进
    try:
        # 序号
        target_course_number = course_number[:-2]  # 课程类别由 course_number 去除后两位构成
        logging.info(f"目标课程序号: {target_course_number}")

        # 检查是否在 iframe 中
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            logging.info(f"页面中存在 {len(iframes)} 个 iframe，尝试切换到 iframe")
            driver.switch_to.frame(iframes[0])  # 假设目标 iframe 是第一个

        # 尝试定位目标课程行
        try:
            target_row = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'//tr[.//span[normalize-space(text())="{target_course_number}"]]')
                )
            )
            logging.info(f"已成功定位到序号为 {target_course_number} 的行元素")
            
            # 打印整个 <tr> 元素的 HTML
            print(target_row.get_attribute("outerHTML"))

            # 定位复选框的父级 <label> 并点击
            checkbox_label = target_row.find_element(By.XPATH, './/label[contains(@class, "el-checkbox")]')
            logging.info("已定位到复选框的父级标签")

            # 滚动到复选框并确保可见
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_label)

            # 高亮显示复选框父级标签并点击
            highlight(checkbox_label)
            checkbox_label.click()
            logging.info(f"已点击序号为 {target_course_number} 的行中的复选框")

        except: #4.2 通识选修课（人文经典与审美素养）
            # 如果未找到目标课程，尝试跳转到选修课界面
            logging.warning(f"未找到序号为 {target_course_number} 的课程，跳转到选修课界面（人文经典）")

            # 切回主内容（如果之前切换到了 iframe）
            if iframes:
                driver.switch_to.default_content()

            # 定位并点击 "通识选修课" 按钮
            elective_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//span[@class="el-radio-button__inner" and contains(text(), "通识选修课")]')
                )
            )
            logging.info("已定位到 '通识选修课' 按钮")
            elective_button.click()
            logging.info("已点击 '通识选修课' 按钮，跳转至选修课界面")

            # 尝试定位选修课-人文经典与审美素养中是否有目标课程
            # 尝试定位目标课程行
            try:
                target_row = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, f'//tr[.//div[contains(text(), "{target_course_number}")]]')
                    )
                )
                logging.info(f"已成功定位到序号为 {target_course_number} 的行元素")
                
                # 打印整个 <tr> 元素的 HTML
                print(target_row.get_attribute("outerHTML"))

                # 定位复选框的父级 <label> 并点击
                checkbox_label = target_row.find_element(By.XPATH, './/label[contains(@class, "el-checkbox")]')
                logging.info("已定位到复选框的父级标签")

                # 滚动到复选框并确保可见
                driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_label)

                # 高亮显示复选框父级标签并点击
                highlight(checkbox_label)
                checkbox_label.click()
                logging.info(f"已点击序号为 {target_course_number} 的行中的复选框")

            except:#4.3 通识选修课（工程能力与创新思维）
                target_tab = wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, "tab-工程能力与创新思维")  # 使用 id 定位
                    )
                )
                logging.info("已定位到 '选修课-工程能力与创新思维'")
                target_tab.click()
                # 尝试定位选修课-工程能力与创新思维中是否有目标课程
                # 尝试定位目标课程行
                try:
                    target_row = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, f'//tr[.//div[contains(text(), "{target_course_number}")]]')
                        )
                    )
                    logging.info(f"已成功定位到序号为 {target_course_number} 的行元素")
                    
                    # 打印整个 <tr> 元素的 HTML
                    print(target_row.get_attribute("outerHTML"))

                    # 定位复选框的父级 <label> 并点击
                    checkbox_label = target_row.find_element(By.XPATH, './/label[contains(@class, "el-checkbox")]')
                    logging.info("已定位到复选框的父级标签")

                    # 滚动到复选框并确保可见
                    driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_label)

                    # 高亮显示复选框父级标签并点击
                    highlight(checkbox_label)
                    checkbox_label.click()
                    logging.info(f"已点击序号为 {target_course_number} 的行中的复选框")

                except:
                    #4.4 通识选修课（社会发展与国际视野）
                    target_tab = wait.until(
                        EC.element_to_be_clickable(
                            (By.ID, "tab-社会发展与国际视野")  # 使用 id 定位
                        )
                    )
                    logging.info("已定位到 '选修课-社会发展与国际视野'")
                    target_tab.click()
                    # 尝试定位选修课-社会发展与国际视野中是否有目标课程
                    # 尝试定位目标课程行
                    try:
                        target_row = wait.until(
                            EC.presence_of_element_located(
                                (By.XPATH, f'//tr[.//div[contains(text(), "{target_course_number}")]]')
                            )
                        )
                        logging.info(f"已成功定位到序号为 {target_course_number} 的行元素")
                        
                        # 打印整个 <tr> 元素的 HTML
                        print(target_row.get_attribute("outerHTML"))

                        # 定位复选框的父级 <label> 并点击
                        checkbox_label = target_row.find_element(By.XPATH, './/label[contains(@class, "el-checkbox")]')
                        logging.info("已定位到复选框的父级标签")

                        # 滚动到复选框并确保可见
                        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_label)

                        # 高亮显示复选框父级标签并点击
                        highlight(checkbox_label)
                        checkbox_label.click()
                        logging.info(f"已点击序号为 {target_course_number} 的行中的复选框")

                    except:
                        #4.5 通识选修课（科学探索与生命关怀）
                        target_tab = wait.until(
                            EC.element_to_be_clickable(
                                (By.ID, "tab-科学探索与生命关怀")  # 使用 id 定位
                            ) 
                        )
                        logging.info("已定位到 '选修课-科学探索与生命关怀'")
                        target_tab.click()
                        # 尝试定位选修课-科学探索与生命关怀中是否有目标课程
                        # 尝试定位目标课程行
                        target_row = wait.until(
                            EC.presence_of_element_located(
                                (By.XPATH, f'//tr[.//div[contains(text(), "{target_course_number}")]]')
                            )
                        )
                        logging.info(f"已成功定位到序号为 {target_course_number} 的行元素")
                        
                        # 打印整个 <tr> 元素的 HTML
                        print(target_row.get_attribute("outerHTML"))

                        # 定位复选框的父级 <label> 并点击
                        checkbox_label = target_row.find_element(By.XPATH, './/label[contains(@class, "el-checkbox")]')
                        logging.info("已定位到复选框的父级标签")

                        # 滚动到复选框并确保可见
                        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_label)

                        # 高亮显示复选框父级标签并点击
                        highlight(checkbox_label)
                        checkbox_label.click()
                        logging.info(f"已点击序号为 {target_course_number} 的行中的复选框")
                            
        # 如果需要切回主内容
        if iframes:
            driver.switch_to.default_content()

    except:
        feedback = "，请检查页面是否正常或向开发者反馈:https://github.com/boatchanting/Tongji-electcourse2/issues"
        logging.error(f"在定位课程并添加到选课列表时发生错误，请检查课号是否输入错误，{feedback}")

if __name__ == '__main__':
    #multiprocessing.freeze_support() # 用于打包成 exe, 必须放在所有代码的最前面, 否则会报错
    #multiprocessing.set_start_method('spawn', force=True)
    api = Api()
    remote_url = 'https://boatchanting.github.io/Tongji-electcourse2/v0.3test.html'
    window = webview.create_window(
        title='TJ-ElectCourse2test',
        url=remote_url,
        js_api=api,
        width=800,
        height=650
    )
    webview.start()
