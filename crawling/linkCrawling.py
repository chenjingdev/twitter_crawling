import chromedriver_autoinstaller
import re
import logging
import traceback
import json
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from backend.userCrawling import *
from customModule import *
from selenium.webdriver.chrome.options import Options

logging.basicConfig(filename='error.log', level=logging.ERROR)

nickName = "mizuki_i_l"
startDate = ""
endDate = ""
tweetLinks = []

options = Options()
options.add_argument("user-data-dir=C:\\Users\\AtechM_03\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
driver = webdriver.Chrome(executable_path=r'C:\path\to\chromedriver.exe', chrome_options=options)

# chrome driver를 자동으로 설치함
chromedriver_autoinstaller.install() 

options = webdriver.ChromeOptions() # Browser 세팅하기
options.add_argument("user-data-dir=/Users/chenjing/Library/Application Support/Google/Chrome/Default")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('lang=ko_KR') # 사용언어 한국어
options.add_argument('--start-maximized') # 창 최대화
options.add_argument('disable-gpu') # 하드웨어 가속 안함
# options.add_argument('headless') # 창 숨기기

# chrome_options = Options()
options.add_argument("--proxy-server=socks5://127.0.0.1:9150")

# 브라우저 세팅
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(executable_path='C:/Users/user/Desktop/크롤링/crawler/crwaling code/chromedriver/chromedriver.exe', options=options)
driver = webdriver.Chrome(executable_path="myPath", options=options)

# 브라우저에 URL 호출하기
driver.get(url='https://twitter.com/i/flow/login')

# 트위터 로그인
twitter_loggin(driver)

# url 변경
try:
	el_located(driver, "[data-testid=cellInnerDiv]")
	driver.get(url=f'https://twitter.com/{nickName}')
except:
  print('url변경 오류')

# 첫번째 트윗 리플 갯수 조회
# 리플 1개 이상이면 주소 추출
# 첫번째 트윗 삭제
try:
	while True:
		el_located(driver, "[data-testid=cellInnerDiv] [data-testid=app-text-transition-container]")

		# 리플 있을경우 실행
		if driver.find_element(By.CSS_SELECTOR, "[data-testid=cellInnerDiv] [data-testid=app-text-transition-container]").text:
			href = driver.find_elements(By.CSS_SELECTOR, "[data-testid=cellInnerDiv]:first-child a[role=link]")
			for href in href:
				txt = href.get_attribute("href")
				x = re.search(f"{nickName}\/status\/[0-9]*", txt)
				y = re.search("photo", txt)
				z = re.search("media_tags", txt)

				if x and not y and not z:
					tweetLinks.append(href.get_attribute("href"))
					print(href.get_attribute("href"))

		# 블럭삭제
		js_removeBlock = "var target = document.querySelector('[data-testid=cellInnerDiv]');target.parentNode.removeChild(target)"
		driver.execute_script(js_removeBlock)
		# sleep(0.5)
  
except Exception:
	logging.error(traceback.format_exc())
	print('삭제할 트윗이 없거나 에러')

# 크롤링한 링크 데이터 json 형식으로 저장
with open(f"link_files/{nickName}_links.json", "w") as f:
  json.dump(tweetLinks, f)
   
# print(tweetLinks)
print('done!')

sleep(600)
# 브라우저 탭 닫기
# driver.close()
# 브라우저 종료하기 (탭 모두 종료)
# driver.quit()