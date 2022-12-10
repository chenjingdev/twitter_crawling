from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from private import *

# 선택한 요소가 나올때까지 대기
def el_located(driver, cssSelector):
	WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.CSS_SELECTOR, cssSelector))
	)
 
def twitter_loggin(driver):
  # 이메일
	try:
		el_located(driver, "[name=text]")
		username_field = driver.find_element_by_name("text")
		username_field.send_keys(email)
		username_field.send_keys(Keys.RETURN)
	except:
		print('이메일 입력 오류')

	# 아이디
	try:
		el_located(driver, "[name=text]")
		username_field2 = driver.find_element_by_name("text")
		username_field2.send_keys(id)
		username_field2.send_keys(Keys.RETURN)
	except:
		print('아이디 입력 오류')

	# 비밀번호
	try:
		el_located(driver, "[name=password]")
		password_field = driver.find_element_by_name("password")
		password_field.send_keys(password)
		password_field.send_keys(Keys.RETURN)
	except:
		print('비밀번호 입력 오류')