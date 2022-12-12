import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def INSERT_USER_TABLE(df):
  print('insert')

def READ_USER_TABLE(nickName):
	file_path = f"database/twit_links/{nickName}_links.json"
	with open(file_path+"data.json", encoding='utf-8') as f:
		data = json.load(f)
		print(data)

def UPDATE_USER_TABLE(df):
	print('update')