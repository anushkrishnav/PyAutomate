import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

# It automate the task of Configuring the new or reseted router
# Prerequisite
# 1. Download Python : https://www.python.org/downloads/
# 2. Download ChromeDriver : https://chromedriver.chromium.org/downloads
# 3. Install Selenium : pip install selenium


# Add ISP Credential here
username = "ISP Username"
ispPassword = "564365456"
# Add Wifi Credential here
ssid = "Sainath"
password = "Password"


def Login():
    driver.get("http://192.168.0.1/")
    driver.find_element_by_xpath('//*[@id="userName"]').send_keys("admin")
    driver.find_element_by_xpath('//*[@id="pcPassword"]').send_keys("admin")
    driver.find_element_by_xpath('//*[@id="loginBtn"]').click()


def OpenTab(xpath):
    time.sleep(0.5)
    driver.switch_to.frame("frame1")
    tab = driver.find_element_by_xpath(str(xpath))
    actions = ActionChains(driver)
    actions.move_to_element(tab).perform()
    tab.click()
    driver.switch_to.default_content()
    driver.switch_to.frame("frame2")


def Troubleshoot():
    OpenTab('//*[@id="menu_network"]')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="disConn"]').click()
    driver.find_element_by_xpath('//*[@id="saveBtn"]').click()
    print("Troubleshoot Successful")


def Configuration():
    OpenTab('//*[@id="menu_qs"]')
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="main"]/div/p[4]/input[2]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="tail"]/input[2]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="ppp"]').click()
    driver.find_element_by_xpath('//*[@id="main"]/div/p[4]/input[2]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="usr"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="pwd"]').send_keys(ispPassword)
    driver.find_element_by_xpath('//*[@id="cfm"]').send_keys(ispPassword)
    driver.find_element_by_xpath('//*[@id="main"]/div/p[4]/input[2]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="ssid"]').clear()
    driver.find_element_by_xpath('//*[@id="ssid"]').send_keys(ssid)
    driver.find_element_by_xpath('//*[@id="pwd"]').clear()
    driver.find_element_by_xpath('//*[@id="pwd"]').send_keys(password)
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="main"]/div/p[4]/input[2]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="saveBtn"]').click()
    sec = 0
    # print(bcolors.OKBLUE + '[', end='' + bcolors.ENDC + bcolors.OKGREEN)
    print("[", end="")
    while sec < 10:
        print("-", end="")
        time.sleep(0.6)
        sec += 1
        # print(bcolors.ENDC + bcolors.OKBLUE + ']' + bcolors.ENDC + bcolors.OKGREEN + ' ✓ \n Configuration Successful' )
        # print(bcolors.ENDC)
    print("] ✓ \n Configuration Successful ")


# -------------------------------------------------------------

choice = input("1. Config\n2. Check\n==>")
chromeOption = Options()
chromeOption.headless = True
driver = webdriver.Chrome(executable_path="C:\chromedriver.exe", options=chromeOption)
Login()
if choice == "1":
    Configuration()
elif choice == "2":
    Troubleshoot()
else:
    print("Incorrect Option")

driver.quit()
