import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM

# TU SOBIE WPISZ SWOJE DANE LOGOWANIA
USR_LOGIN = input('USERNAME: ')
USR_PASSWORD = input('PASSWORD: ')

usr = input('Nazwa rudej na insta: ')

user_input = input(
    'Ile jej followersow chcesz, ale nie za duzo bo to troche zajmie xD:')
TIME = 0.069 * int(user_input)


def scrape(username):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")

    # mobile wersion xD
    mobile_emulation = {
        "userAgent": 'Mozilla/5.0 (Linux; Android 4.0.3; HTC One X Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/83.0.1025.133 Mobile Safari/535.19'
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    # auto install manager
    browser = webdriver.Chrome(executable_path=CM().install(), options=options)

    browser.get('https://instagram.com/')
    browser.set_window_size(500, 950)
    time.sleep(1)

    # accept cookies
    browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/button[1]').click()
    time.sleep(1)

    # Log in
    browser.find_element_by_xpath(
        '/html/body/div[1]/section/main/article/div/div/div/div[2]/button').click()
    print("Logging in...")
    time.sleep(1)

    # username input
    username_field = browser.find_element_by_xpath(
        '/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[3]/div/label/input')
    username_field.send_keys(USR_LOGIN)

    # password input
    find_pass_field = (
        By.XPATH, '/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[4]/div/label/input')
    WebDriverWait(browser, 50).until(
        EC.presence_of_element_located(find_pass_field))
    pass_field = browser.find_element(*find_pass_field)
    WebDriverWait(browser, 50).until(
        EC.element_to_be_clickable(find_pass_field))
    pass_field.send_keys(USR_PASSWORD)

    # Logging button
    browser.find_element_by_xpath(
        '/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[6]/button').click()
    time.sleep(2)

    link = 'https://www.instagram.com/{}/'.format(usr)
    browser.get(link)
    time.sleep(2)

    # Followers reference
    browser.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/ul/li[2]/a').click()

    time.sleep(3)
    print('Scrapping...')

    # scrolling in followers using end button
    for i in range(round(TIME)):
        ActionChains(browser).send_keys(Keys.END).perform()
        time.sleep(3)

        followers = browser.find_elements_by_xpath(
            '//*[@id="react-root"]/section/main/div/ul/div/li/div/div[1]/div[2]/div[1]/a')

        urls = []

        # getting url from href attribute in title
        for n in followers:
            if n.get_attribute('href') is not None:
                urls.append(n.get_attribute('href'))
            else:
                continue

    print('Converting...')
    users = []
    for url in urls:
        # user = url.replace('https://www.instagram.com/', '').replace('/', '')
        users.append(url)

    print('Saving...')
    f = open('followers.csv', 'w')
    s1 = '\n'.join(users)
    f.write(s1)
    f.close()


scrape(usr)
