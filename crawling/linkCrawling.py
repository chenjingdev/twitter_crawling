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
from backend.userCrawling import users
from backend.linkCrawling import updateLink
from customModule import el_located
from database import *

logging.basicConfig(filename='error.log', level=logging.ERROR) #에러 로그 찍기
chromedriver_autoinstaller.install() # chrome driver를 자동으로 설치함
options = webdriver.ChromeOptions() # Browser 세팅하기
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('lang=ko_KR') # 사용언어 한국어
options.add_argument('--start-maximized') # 창 최대화
options.add_argument('disable-gpu') # 하드웨어 가속 안함
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
options.add_argument("user-data-dir=C:/Users/chenj/AppData/Local/Google/Chrome/User Data/Default") # 로그인 인증번호 발송되는 현상 방지(window용)
# options.add_argument("user-data-dir=/Users/chenjing/Library/Application Support/Google/Chrome/Default") # 로그인 인증번호 발송되는 현상 방지(mac용)
# options.add_argument('headless') # 창 숨기기
options.add_argument("--proxy-server=socks5://127.0.0.1:9150") # Tro브라우저사용
driver = webdriver.Chrome(options=options) # 브라우저 세팅

# print(int(time.time()*1000))
# currdate = datetime.datetime.strptime("2022-11-07T11:28:24.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
# currdate2 = datetime.datetime.strptime("2022-11-09T11:28:24.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
# print(int(currdate.timestamp()*1000),"test")
# print(currdate > currdate2)
# print(currdate < currdate2)
# d = datetime.datetime.now()
# print(d)

# exit()
tweetLinks = []
startingDday = 7

def linkCrowaling(user):
	# 브라우저 호출
	driver.get(url=f'https://twitter.com/{user["user_name"]}')

	# 첫번째 트윗 리플 갯수 조회
	# 리플 1개 이상이면 주소 추출
	# 첫번째 트윗 삭제
	try:
		while True:
			# sleep(1)
			el_located(driver, "[data-testid=cellInnerDiv] [data-testid=app-text-transition-container]")
   
			tweetDate = driver.find_element(By.CSS_SELECTOR, "time[datetime]").get_attribute("datetime")
			tweetChk = len(driver.find_element(By.CSS_SELECTOR, "[data-testid=cellInnerDiv] article > div > div > div > div:nth-child(1)").text)
			tweetTime = int(datetime.datetime.strptime(tweetDate,"%Y-%m-%dT%H:%M:%S.%fZ").timestamp()*1000)
			crawlStartTime = int(time.time()*1000) - (startingDday * 86400000)
			crawlEndTime = int(datetime.datetime.strptime(user["break_date"],"%Y-%m-%dT%H:%M:%S.%fZ").timestamp()*1000)
   
			# print(tweetTime)
			# print(crawlStartTime)
			print(tweetChk)
			print(type(tweetTime))
			print(type(crawlEndTime))
			print(tweetTime < crawlEndTime)
   
			# 최종 크롤링 날짜에 접근하면 크롤링 중단
			if not(tweetChk) and tweetTime < crawlEndTime: 
				break
  
			# 리트윗 핀트윗 제외
			if tweetChk or crawlStartTime < tweetTime:
				print('트윗 삭제')
				# 블럭삭제
				js_removeBlock = "var target = document.querySelector('[data-testid=cellInnerDiv]');target.parentNode.removeChild(target)"
				driver.execute_script(js_removeBlock)
				continue
  
			# 리플 있을경우 실행
			if driver.find_element(By.CSS_SELECTOR, "[data-testid=cellInnerDiv] [data-testid=app-text-transition-container]").text:
				print('트윗 크롤링')
				href = driver.find_elements(By.CSS_SELECTOR, "[data-testid=cellInnerDiv]:first-child a[role=link]")
				for href in href:
					txt = href.get_attribute("href")
					w = re.search(f"{user['user_name']}\/status\/[0-9]*", txt)
					x = re.search("analytics", txt)
					y = re.search("photo", txt)
					z = re.search("media_tags", txt)

					if w and not x and not y and not z :
						tweetLinks.append(href.get_attribute("href"))
						print(href.get_attribute("href"))

			# 블럭삭제
			js_removeBlock = "var target = document.querySelector('[data-testid=cellInnerDiv]');target.parentNode.removeChild(target)"
			driver.execute_script(js_removeBlock)
		
	except Exception:
		logging.error(traceback.format_exc())
		print('삭제할 트윗이 없거나 에러')

	# 크롤링한 링크 데이터 json 형식으로 저장
	updateLink(user, tweetLinks)

for user in users:
  print(user)
  linkCrowaling(user)

print('done!')
sleep(600)
# 브라우저 탭 닫기
# driver.close()
# 브라우저 종료하기 (탭 모두 종료)
# driver.quit()