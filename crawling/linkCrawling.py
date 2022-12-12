import chromedriver_autoinstaller
import re
import logging
import traceback
import json
import pandas as pd
import os
import datetime
import time
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
from database import *

logging.basicConfig(filename='error.log', level=logging.ERROR)

print(READ_USER_TABLE()[0]["user_name"])
print(int(time.time()*1000))
print(datetime.datetime.strptime("2022-11-07T11:28:24.000Z", "%Y-%m-%dT%H:%M:%S.%fZ").time)

tweetLinks = []
d = datetime.datetime.now()
exit()

# chrome driver를 자동으로 설치함
chromedriver_autoinstaller.install() 
options = webdriver.ChromeOptions() # Browser 세팅하기
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('lang=ko_KR') # 사용언어 한국어
options.add_argument('--start-maximized') # 창 최대화
options.add_argument('disable-gpu') # 하드웨어 가속 안함
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
# options.add_argument('headless') # 창 숨기기

# 로그인 인증번호 발송되는 현상 방지(mac용)
# options.add_argument("user-data-dir=/Users/chenjing/Library/Application Support/Google/Chrome/Default")
# 로그인 인증번호 발송되는 현상 방지(window용)
options.add_argument("user-data-dir=C:/Users/chenj/AppData/Local/Google/Chrome/User Data/Default")

# Tro브라우저사용
options.add_argument("--proxy-server=socks5://127.0.0.1:9150")

# 브라우저 세팅
driver = webdriver.Chrome(options=options)

for
  

def linkCrowaling(userName):
	# 브라우저 호출
	driver.get(url=f'https://twitter.com/{userName}')

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
					x = re.search(f"{userName}\/status\/[0-9]*", txt)
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
	with open(f"database/twit_links/{userName}_links.json", "w") as f:
		json.dump(tweetLinks, f)
   
print('done!')

sleep(600)
# 브라우저 탭 닫기
# driver.close()
# 브라우저 종료하기 (탭 모두 종료)
# driver.quit()