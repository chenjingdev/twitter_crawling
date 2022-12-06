import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from private import *

# chrome driver를 자동으로 설치함
chromedriver_autoinstaller.install() 

options = webdriver.ChromeOptions() # Browser 세팅하기
options.add_argument('lang=ko_KR') # 사용언어 한국어
# options.add_argument('disable-gpu') # 하드웨어 가속 안함
options.add_argument('--start-maximized') # 하드웨어 가속 안함
# options.add_argument('headless') # 창 숨기기

# 브라우저 세팅
driver = webdriver.Chrome(options=options)

# 브라우저에 URL 호출하기
driver.get(url='https://twitter.com/i/flow/login')
driver.implicitly_wait(10)

# 이메일
username_field = driver.find_element_by_name("text")
username_field.send_keys(email)
username_field.send_keys(Keys.RETURN)

# 아이디
username_field2 = driver.find_element_by_name("text")
username_field2.send_keys(id)
username_field2.send_keys(Keys.RETURN)

# 비밀번호
password_field = driver.find_element_by_name("password")
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

# 사용자검색
search_field = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
search_field.send_keys("mizuki_i_l")
sleep(2)
search_field.send_keys(Keys.ARROW_DOWN)
search_field.send_keys(Keys.ARROW_DOWN)
search_field.send_keys(Keys.RETURN)

sleep(2)

# 블럭클릭
tweet_block = driver.find_element_by_css_selector("[data-testid=cellInnerDiv]")
ActionChains(driver).key_down(Keys.CONTROL).click(tweet_block).key_up(Keys.CONTROL).perform()

# 블럭삭제
# js_removeBlock = "var target = document.querySelector('[data-testid=cellInnerDiv]');target.parentNode.removeChild(target)"
# driver.execute_script(js_removeBlock)

sleep(600)
# 브라우저 탭 닫기
driver.close()
# 브라우저 종료하기 (탭 모두 종료)
driver.quit()