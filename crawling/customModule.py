from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from private import *

# 선택한 요소가 나올때까지 대기
def el_located(driver, cssSelector):
	element = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.CSS_SELECTOR, cssSelector))
	)
	return element
 
def twitter_loggin(driver):
  # 이메일
	try:
		element = el_located(driver, "[name=text]")
		element.send_keys(email)
		element.send_keys(Keys.RETURN)
	except:
		print('이메일 입력 오류')

	# 아이디
	try:
		element = el_located(driver, "[name=text]")
		element.send_keys(id)
		element.send_keys(Keys.RETURN)
	except:
		print('아이디 입력 오류')

	# 비밀번호
	try:
		element = el_located(driver, "[name=password]")
		element.send_keys(password)
		element.send_keys(Keys.RETURN)
	except:
		print('비밀번호 입력 오류')