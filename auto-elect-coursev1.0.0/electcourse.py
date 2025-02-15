from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import stdiomask
import logging
print("自动帮你选课程序，请输入学号和密码，课程编号，自动帮你选课")
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

username = input("请输入您的学号") #请输入您的学号
password = stdiomask.getpass("请输入密码：") #请输入您的密码
course_number = input("请输入课程编号")  # 请替换为你要选择的课程编号
if int(username)>0 :
    course_name = course_number[:-2] # 课程类别由course_number去除后两位构成

    logging.info(f"用户输入的学号: {username}")
    logging.info(f"用户输入的课程编号: {course_number}")
    logging.info(f"课程类别: {course_name}")

    # 初始化Edge浏览器
    try:
        driver = webdriver.Edge()
        logging.info("Edge浏览器已启动")
    except Exception as e:
        logging.error("无法启动Edge浏览器")
        raise e

    # 打开登录页面
    try:
        login_url = "https://1.tongji.edu.cn"  # 登录 URL
        driver.get(login_url)
        logging.info(f"打开1系统登录页面")
    except Exception as e:
        logging.error(f"无法打开1系统登录页面")
        raise e

    # 使用WebDriverWait来等待元素出现
    try:
        wait = WebDriverWait(driver, 10)  # 最长等待时间为10秒

        # 定位用户名和密码输入框，并输入登录信息
        username_input = wait.until(EC.presence_of_element_located((By.ID, "j_username")))
        password_input = wait.until(EC.presence_of_element_located((By.ID, "j_password")))
        logging.info("定位用户名和密码输入框")

        # 填入用户名和密码
        username_input.send_keys(username)
        password_input.send_keys(password)
        logging.info("填入用户名和密码")

    except Exception as e:
        logging.error(f"用户名或密码输入错误")
        raise e

    # 定位登录按钮并点击
    try:
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "loginButton")))
        logging.info("点击登录按钮")
    except Exception as e:
        logging.error(f"找不到登录按钮")
        raise e
    # 高亮显示元素的函数
    def highlight(element):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                            element, "border: 2px solid red;")

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
        logging.error(f"无法跳转选课界面")
        raise e

    time.sleep(3)
    # 使用WebDriverWait来等待下一个元素出现
    # wait.until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "el-button--primary") and contains(span, "进入选课")]')))

    # 1.定位“进入选课”按钮并点击
    try:
        enter_elect_button = driver.find_element(By.XPATH, '//button[contains(@class, "el-button--primary") and contains(span, "进入选课")]')
        highlight(enter_elect_button)  # 高亮“进入选课”按钮
        enter_elect_button.click()
        logging.info("1.点击“进入选课”按钮")
    except Exception as e:
        logging.error(f"1.找不到“进入选课”按钮")
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
        logging.error(f"2.找不到“确定”按钮")
        raise e
    #input("进入选课界面后，请按任意键继续...") # 测试用

    # 3.定位“选择课程”按钮并点击
    try:
        wait = WebDriverWait(driver, 1)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div[2]/button[1]')))
        logging.info("2.找到“选择课程”按钮")
        select_course_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div[2]/button[1]')
        highlight(select_course_button)  # 高亮“选择课程”按钮
        select_course_button.click()
        logging.info("3.点击“选择课程”按钮")
    except Exception as e:
        logging.error(f"3.找不到“选择课程”按钮")
        raise e

    # 4. 定位课程并添加到选课列表
    try:
        # 序号
        target_course_number = course_number[:-2]  # 课程类别由course_number去除后两位构成

        # 检查是否在 iframe 中
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            logging.info(f"页面中存在 {len(iframes)} 个 iframe，尝试切换到 iframe")
            driver.switch_to.frame(iframes[0])  # 假设目标 iframe 是第一个

        # 等待序号所在的 <span> 元素加载，并通过祖先定位到 <tr>
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

        # 如果需要切回主内容
        if iframes:
            driver.switch_to.default_content()

        # 5.定位提交按钮元素并点击
        try:
            submit_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[4]/div/div[3]/span/button[2]')
            highlight(submit_button)  # 高亮提交按钮
            submit_button.click()
            logging.info("5.点击提交按钮")
        except Exception as e:
            logging.error(f"5.找不到提交按钮")
            raise e    

    except Exception as e:
        logging.error(f"定位序号 {target_course_number} 的行元素时发生错误: {e}")
        # 如果定位目标行失败，尝试点击取消按钮
        try:
            cancel_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[4]/div/div[3]/span/button[1]')
                )
            )
            logging.info("未找到目标课程，定位到取消按钮")

            # 点击取消按钮
            cancel_button.click()
            logging.info("已点击取消按钮")

        except Exception as cancel_exception:
            logging.error(f"未能点击取消按钮: {cancel_exception}")

    # input("进入选课界面后，请按任意键继续...") # 测试用

    time.sleep(0.5)
    # 使用WebDriverWait来等待下一个元素出现
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[4]/div/div[3]/span/button[2]')))

    # 6.定位课程并点击
    # 定位含有课号的元素并点击
    try:
        # 使用WebDriverWait来等待下一个元素出现
        wait.until(EC.presence_of_element_located((By.XPATH, f'//td/div[contains(@class, "courseName") and contains(text(), "{course_name}")]')))
        course_element = driver.find_element(By.XPATH, f'//td/div[contains(@class, "courseName") and contains(text(), "{course_name}")]')
        highlight(course_element)  # 高亮含有课号的元素
        course_element.click()
        #input("按任意键继续...")
        logging.info(f"已成功定位到课程编号为 {course_number} 的元素")
    except Exception as e:
        logging.error(f"找不到课程编号为 {course_number} 的元素: {e}")

    # 7.选择目标课程
    try:
        # 目标课程编号
        target_course_number = course_number

        # 定位目标行的 <tr> 元素
        target_row = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f'//tr[.//td[@class="courseName" and text()="{target_course_number}"]]')
            )
        )
        logging.info(f"已成功定位到课程编号为 {target_course_number} 的行")

        # 滚动到目标行以确保可见
        driver.execute_script("arguments[0].scrollIntoView(true);", target_row)

        # 高亮显示目标行（可选，便于调试）
        driver.execute_script("arguments[0].setAttribute('style', 'border: 2px solid red;');", target_row)

        # 点击目标行
        target_row.click()
        logging.info(f"已点击课程编号为 {target_course_number} 的行")

    except Exception as e:
        logging.error(f"定位或点击课程编号为 {target_course_number} 的行时发生错误: {e}")

    # 8.保存课表
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

    # 等待保存操作完成
    time.sleep(1)
    # 9.定位返回的信息并获取
    try:
        # 定位结果框
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
            print(f"选课结果：{result_text}")
            
            # 定位关闭按钮并点击
            close_button = result_dialog.find_element(By.XPATH, './/button[contains(@class, "el-button--default") and span[text()="关闭"]]')
            close_button.click()
            logging.info("点击关闭按钮，退出程序")
            #input("按任意键退出...") #测试用
            #driver.quit()
        else:
            logging.warning("未检测到选课成功消息")
            print(f"选课结果：{result_text}")
            
            # 定位关闭按钮并点击
            close_button = result_dialog.find_element(By.XPATH, './/button[contains(@class, "el-button--default") and span[text()="关闭"]]')
            close_button.click()
            logging.info("点击关闭按钮，继续运行程序")
    except Exception as e:
        logging.error(f"处理结果框时发生错误: {e}")
else:
    print("拒绝使用！")
    
