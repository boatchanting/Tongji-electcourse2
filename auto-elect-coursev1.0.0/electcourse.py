from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

username = "" #请输入您的学号
password = "" #请输入您的密码
course_name = ""  # 请替换为你要选择的课程类别
course_number = ""  # 请替换为你要选择的课程编号

# 初始化Edge浏览器
driver = webdriver.Edge()

# 打开登录页面
login_url = "https://1.tongji.edu.cn"  # 登录 URL
driver.get(login_url)

# 使用WebDriverWait来等待元素出现
wait = WebDriverWait(driver, 10)  # 最长等待时间为10秒

# 定位用户名和密码输入框，并输入登录信息
username_input = wait.until(EC.presence_of_element_located((By.ID, "j_username")))
password_input = wait.until(EC.presence_of_element_located((By.ID, "j_password")))

# 请替换为您的账号和密码
username_input.send_keys(username)
password_input.send_keys(password)

# 定位登录按钮并点击
login_button = wait.until(EC.element_to_be_clickable((By.ID, "loginButton")))

# 高亮元素的函数
def highlight(element):
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                          element, "border: 2px solid red;")

highlight(login_button)
login_button.click()

#input("登录完成后，请按任意键继续...")
time.sleep(3)

# 等待登录过程完成
wait.until(EC.url_changes(login_url))

mode = "electcourse"
if mode == "electcourse":
    # 跳转界面https://1.tongji.edu.cn/studentElect
    driver.get("https://1.tongji.edu.cn/studentElect")

    time.sleep(3)
    # 使用WebDriverWait来等待下一个元素出现
    # wait.until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "el-button--primary") and contains(span, "进入选课")]')))

    # 1.定位“进入选课”按钮并点击
    enter_elect_button = driver.find_element(By.XPATH, '//button[contains(@class, "el-button--primary") and contains(span, "进入选课")]')
    
    highlight(enter_elect_button)  # 高亮“进入选课”按钮
    enter_elect_button.click()

    # 使用WebDriverWait来等待下一个元素出现
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[3]/div/div[3]/span/button')))

    # 2.定位“确定”按钮并点击 /html/body/div[1]/div[1]/div[1]/section/main/div/div[3]/div/div[3]/span/button
    confirm_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[3]/div/div[3]/span/button')
    highlight(confirm_button)  # 高亮“确定”按钮
    confirm_button.click()

    # input("进入选课界面后，请按任意键继续...") # 测试用
    # 使用WebDriverWait来等待下一个元素出现
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div[2]/button[1]')))

    # 3.定位选择课程按钮并点击 /html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div[2]/button[1]
    select_course_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div[2]/button[1]')
    highlight(select_course_button)  # 高亮“选择课程”按钮
    select_course_button.click()

    # input("进入选课界面后，请按任意键继续...") # 测试用
    # 使用WebDriverWait来等待下一个元素出现
    wait.until(EC.presence_of_element_located((By.XPATH, f'//div[contains(@class, "cell el-tooltip") and contains(text(),"{course_name}")]')))

    # 4.定位课程并添加
    course_element = driver.find_element(By.XPATH, f'//div[contains(@class, "cell el-tooltip") and contains(text(),"{course_name}")]')
    highlight(course_element)  # 高亮选择的课程元素
    course_element.click()

    # 使用WebDriverWait来等待下一个元素出现
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[4]/div/div[3]/span/button[2]')))

    # 5.定位提交按钮元素并点击
    # xpath路径 /html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[4]/div/div[3]/span/button[2]
    submit_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[4]/div/div[3]/span/button[2]')
    highlight(submit_button)  # 高亮提交按钮
    submit_button.click()

    # 使用WebDriverWait来等待下一个元素出现
    wait.until(EC.presence_of_element_located((By.XPATH, f'//td/div[contains(@class, "courseName") and contains(text(), "{course_name}")]')))

    # 6.定位课程并点击
    # 定位含有课号的元素并点击
    course_element = driver.find_element(By.XPATH, f'//td/div[contains(@class, "courseName") and contains(text(), "{course_name}")]')
    highlight(course_element)  # 高亮含有课号的元素
    course_element.click()

    # 7.定位课号并点击
    course_number_base_xpath = "/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div[2]/div/div/div/div[2]/table/tr"
    last_two_digits = int(course_number[-2:]) + 2
    new_course_number = course_number[:-2] + f"{last_two_digits:01d}" 
    row_index = last_two_digits - 1 
    xpath = f"{course_number_base_xpath}[{row_index}]/td[1]"
    new_course_sequence_element = driver.find_element(By.XPATH, xpath)
    highlight(new_course_sequence_element)  # 高亮课程序号的元素
    new_course_sequence_element.click()
    
    # 8.点击保存课表按钮
    save_schedule_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div[2]/button[2]')
    highlight(save_schedule_button)  # 高亮保存课表按钮
    save_schedule_button.click()
    input("按任意键继续...")
    # 后续在等待选课窗口开放再进行测试...
    
input("按任意键退出...")
# 退出浏览器
driver.quit()
