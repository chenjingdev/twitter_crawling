import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def INSERT_USER_TABLE(df):
  print('insert')

def READ_USER_TABLE():
	with open(f"database/user_list.json", encoding='utf-8') as f:
		data = json.load(f)
		return data

def UPDATE_USER_TABLE(df):
	print('update')