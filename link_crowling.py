import chromedriver_autoinstaller
import re
import logging
import traceback
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from private import *

logging.basicConfig(filename='error.log', level=logging.ERROR)
nickName = "mizuki_i_l"
startDate = ""
endDate = ""
tweetLinks = []

# chrome driver를 자동으로 설치함
chromedriver_autoinstaller.install() 

options = webdriver.ChromeOptions() # Browser 세팅하기
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('lang=ko_KR') # 사용언어 한국어
# options.add_argument('disable-gpu') # 하드웨어 가속 안함
options.add_argument('--start-maximized') # 하드웨어 가속 안함
# options.add_argument('headless') # 창 숨기기

# 브라우저 세팅
driver = webdriver.Chrome(options=options)

# 브라우저에 URL 호출하기
driver.get(url='https://twitter.com/i/flow/login')

# 이메일
try:
	element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.CSS_SELECTOR, "[name=text]"))
	)
	username_field = driver.find_element_by_name("text")
	username_field.send_keys(email)
	username_field.send_keys(Keys.RETURN)
except:
  print('이메일 입력 오류')

# 아이디
try:
	element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.CSS_SELECTOR, "[name=text]"))
	)
	username_field2 = driver.find_element_by_name("text")
	username_field2.send_keys(id)
	username_field2.send_keys(Keys.RETURN)
except:
  print('아이디 입력 오류')


# 비밀번호
try:
	element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.CSS_SELECTOR, "[name=password]"))
	)
	password_field = driver.find_element_by_name("password")
	password_field.send_keys(password)
	password_field.send_keys(Keys.RETURN)
except:
  print('비밀번호 입력 오류')
  
# url 변경
try:
	element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid=cellInnerDiv]"))
	)
	driver.get(url=f'https://twitter.com/{nickName}')
except:
  print('url변경 오류')

# 첫번째 트윗 리플 갯수 조회
# 리플 1개 이상이면 주소 추출
# 첫번째 트윗 삭제
try:
	while True:
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid=cellInnerDiv] [data-testid=app-text-transition-container]"))
		)

		# 리플 있을경우 실행
		if driver.find_element(By.CSS_SELECTOR, "[data-testid=cellInnerDiv] [data-testid=app-text-transition-container]").text:
			href = driver.find_elements(By.CSS_SELECTOR, "[data-testid=cellInnerDiv]:first-child a[role=link]")
			for href in href:
				txt = href.get_attribute("href")
				x = re.search(f"{nickName}\/status\/[0-9]*", txt)
				y = re.search("photo", txt)

				if x and not y:
					tweetLinks.append(href.get_attribute("href"))
					print(href.get_attribute("href"))

		# 블럭삭제
		js_removeBlock = "var target = document.querySelector('[data-testid=cellInnerDiv]');target.parentNode.removeChild(target)"
		driver.execute_script(js_removeBlock)
		sleep(0.5)
  
except Exception:
	logging.error(traceback.format_exc())
	print('삭제할 트윗이 없거나 에러')

# 크롤링한 링크 데이터 json 형식으로 저장
with open(f"link_files/{nickName}_links.json", "w") as f:
  json.dump(tweetLinks, f)
   
# print(tweetLinks)
print('done!')
 
 
 
 
 
# 블럭클릭
# tweet_block = driver.find_element_by_css_selector("[data-testid=cellInnerDiv]")
# ActionChains(driver).key_down(Keys.CONTROL).click(tweet_block).key_up(Keys.CONTROL).perform()



sleep(600)
# 브라우저 탭 닫기
# driver.close()
# 브라우저 종료하기 (탭 모두 종료)
# driver.quit()