import glob
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from google.cloud import bigquery
from google.oauth2 import service_account

# def CREATE_USER_TABLE(df):
#   # 서비스 계정 키 JSON 파일 경로
# 	key_path = glob.glob("key.json")[0]

# 	# Credentials 객체 생성
# 	credentials = service_account.Credentials.from_service_account_file(key_path) 

# 	# GCP 클라이언트 객체 생성
# 	client = bigquery.Client(credentials = credentials, project = credentials.project_id)
 
# 	# 테이블 ID
# 	table_id = "twitter-crawling-371104.twitter_crawling.user_info"
 
# 	# 데이블 객체 생성
# 	table = client.get_table(table_id)

# 	# 데이터프레임을 테이블에 삽입
# 	client.load_table_from_dataframe(df, table)
 
def CREATE_USER_TABLE(df):
  # 서비스 계정 키 JSON 파일 경로
	key_path = glob.glob("key.json")[0]

	# Credentials 객체 생성
	credentials = service_account.Credentials.from_service_account_file(key_path) 

	# GCP 클라이언트 객체 생성
	client = bigquery.Client(credentials = credentials, project = credentials.project_id)
 
	# 테이블 ID
	table_id = "twitter-crawling-371104.twitter_crawling.user_info"
 
	# 데이블 객체 생성
	table = client.get_table(table_id)

	# 데이터프레임을 테이블에 삽입
	client.load_table_from_dataframe(df, table)

def READ_USER_TABLE():
	key_path = glob.glob("key.json")[0]
	credentials = service_account.Credentials.from_service_account_file(key_path) 
	client = bigquery.Client(credentials = credentials, project = credentials.project_id)
 
	query = f"""
	SELECT *
	FROM `twitter-crawling-371104.twitter_crawling.user_info`
	"""
	check = client.query(query).to_dataframe()
 
	return check

def UPDATE_USER_TABLE(df):
	key_path = glob.glob("key.json")[0]
	credentials = service_account.Credentials.from_service_account_file(key_path) 
	client = bigquery.Client(credentials = credentials, project = credentials.project_id)
 
	query = f"""
	SELECT *
	FROM `twitter-crawling-371104.twitter_crawling.user_info`
	"""