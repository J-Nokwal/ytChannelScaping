from concurrent.futures import thread
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import time
from pathlib import Path
from selenium.webdriver.common.action_chains import ActionChains


print("app started")
now=time.strftime('%l:%M%p %z on %b %d, %Y')
#channelKeyWords="sales coatch business ohio"
channelKeyWords = input("Please Enter Channel Name keyword: ")

# profile = "user-data-dir=" + str(Path.home()) + '''\\AppData\\Local\\Google\\Chrome\\User Data\\Default'''
profile = "user-data-dir=" + str(Path.home()) + '''/chromeDriver/profiles/default'''
print(profile)
try:
    options = webdriver.ChromeOptions()
    # options.add_argument('''user-data-dir=C:\\Users\\J-Nokwal\\AppData\\Local\\Google\\Chrome\\User Data\\Default''')
    # print(options.arguments)
    options.add_experimental_option("detach", True)
    options.add_argument(profile)
    driver = webdriver.Chrome( options=options)
except Exception as e:
    print("Chrome Driver Option Error:",e)
    exit()

driver.get(f"https://www.youtube.com/results?search_query={channelKeyWords}&sp=EgIQAg%253D%253D")
wait = WebDriverWait(driver, 60)

def findChannel():
    # input_box = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]")))
    
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "ytd-channel-renderer")))
    values=[]
    for i in driver.find_elements(By.TAG_NAME, "ytd-channel-renderer"):
        suscribedUsersText = i.find_element(By.XPATH, "div/div[2]/a/div[1]/div/span[3]").text
        if "K subs" not in suscribedUsersText:
            continue
        link = i.find_element(By.TAG_NAME, "a").get_attribute("href")
        # print("link",link)
        channelName =i.find_element(By.XPATH, "div/div[2]/a/div[1]/ytd-channel-name/div/div/yt-formatted-string").text
        # print("channelName",channelName)
        values.append((channelName,suscribedUsersText,link))
    createHTMLFile(values=values)
        

def goToEnd():
    wait2 = WebDriverWait(driver, 1)
    while(True):
        driver.find_element(By.TAG_NAME,value='body').send_keys(Keys.END)
        try:
            wait2.until(EC.presence_of_element_located((By.XPATH, "//*[text()='No more results']")))
            print("No more results")
            break
        except Exception as e:
            print("Loading More")

initial_html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{channelKeyWords}</title>
</head>
<body>
    <h1>{channelKeyWords}</h1>
    <p>Time:- {now}</p>
</body>
</html>
"""

def createHTMLFile(values:list[tuple[str,str, str]]):
    file_path = f"./history/{channelKeyWords} {now}.html"
    soup = BeautifulSoup(initial_html_content, "html.parser")
    # Create a new anchor tag
    if not os.path.exists("./history"):
        os.makedirs("./history")
    for (channelName,suscribedUsersText,link) in values:
        container = soup.new_tag("div", id="container" , style="display : flex; flex-direction: row;justify-content: space-between; align-items: center; border-bottom: 1px solid #000; margin-bottom:10px;")
        nameTag= soup.new_tag("div ", id="name" ,style="min-width: 200px;")
        nameTag.append(channelName)
        container.append(nameTag)
        subTag = soup.new_tag("div", id="sub" ,style="min-width: 200px;")
        subTag.append(suscribedUsersText)
        container.append(subTag)
        aTag = soup.new_tag("a", href=link, target="_blank")
        aTag.append(link)
        container.append(aTag)    
        soup.body.append(container)
    with open(file_path, "w") as html_file:
        html_file.write(str(soup))
    # open file in browser in new tab with current directory + file_path
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("file://" + os.path.realpath(file_path))
    

goToEnd()
findChannel()
time.sleep(20)
# createHTMLFile()
print("done")