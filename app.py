from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import pandas as pd

from slugify import slugify


def generate_article(title, list_of_questions):
    # Initialize Chrome WebDriver
    chrome_op = webdriver.ChromeOptions()
    chrome_op.add_experimental_option("prefs", {"download.default_directory": "F:\TLA\scripts\selenium_serpstat\\articles", "safebrowsing.enabled":"false"})
    driver = webdriver.Chrome(chrome_options=chrome_op) #executable_path="../chromedriver_win32/chromedriver.exe", 
    driver.implicitly_wait(10) # in seconds
    driver.get("https://testlab.serpstat.com/Article_builder")

    # step 1
    try:
        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/div[1]/div/div/div/section[2]/div/div[1]/div/div[6]/ul/li/div[2]/div[1]/div/div/div[1]/div/div[1]/div/div[1]/div/input'))
        )

    except:
        print("some error happen !!")

    api_key_input = driver.find_element("xpath", '//*[@id="root"]/div[1]/div[1]/div/div/div/section[2]/div/div[1]/div/div[6]/ul/li/div[2]/div[1]/div/div/div[1]/div/div[1]/div/div[1]/div/input')
    api_key_input.send_keys("XXXXXXXXXXXX") # Serpstat API Key

    button_set_token = driver.find_element("xpath", '//button[text()="💡 Set token"]')
    button_set_token.click()


    # step 2
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "step-1-title-generation-optional"))
        )

        enter_your_title_field = driver.find_element("xpath", '//*[@id="root"]/div[1]/div[1]/div/div/div/section[2]/div/div[1]/div/div[11]/div[1]/div/div[1]/div/div[1]/div/input')
        enter_your_title_field.send_keys(title)

        button_set_title = driver.find_element("xpath", '//button[text()="✅ Set title and use my outline"]')
        button_set_title.click()
        
    except:
        print("2 some error happen !!")

    # step 3
    try:
        element = WebDriverWait(driver, 500).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="📝 Generate text for all paragraphs"]'))
        )
        article_outline_textarea = driver.find_element("xpath", '//*[@id="root"]/div[1]/div[1]/div/div/div/section[2]/div/div[1]/div/div[12]/div[1]/div/div[1]/div/div[1]/div/textarea')

        for question in list_of_questions:
            question = question+'\n'
            article_outline_textarea.send_keys(question)
        
        button_generate_text = driver.find_element("xpath", '//button[text()="📝 Generate text for all paragraphs"]')
        button_generate_text.click()

    except:
        print("some error happen !! step 3")


    # step 4
    try:
        element = WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Download (.html)"]'))
        )
        download_button = driver.find_element("xpath", '//button[text()="Download (.html)"]')
        download_button.click()

    except:
        print("some error happen !! step 4")

    # step 5
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Download22 (.html)"]'))
        )
        download_button = driver.find_element("xpath", '//button[text()="Download (.html)"]')
        download_button.click()

    except:
        print("some error happen !! step 5")

    print('done >>>  ' + title)


def latest_download_file():
    # path = r'./articles'
    os.chdir('./articles')
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]
    return newest


df = pd.read_csv('cluster_names.csv')
cluster_names = df['cluster_name'].unique()

for name in cluster_names:
    dataFrame = df[df['cluster_name'].str.contains(name)]
    list_of_questions = dataFrame['question'].unique()
    generate_article(name, list_of_questions)

    old_name = latest_download_file()
    new_name = slugify(name)
    new_name = new_name+'.html'
    os.rename(old_name, new_name)
    os.chdir('..')      # костиль для функції latest_download_file

