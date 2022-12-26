import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def INSERT_USER_TABLE(df):
  print('insert')

def READ_USER_TABLE():
	with open("database/user_list.json", 'r', encoding='utf-8') as f:
		return json.load(f)

users = READ_USER_TABLE()

def UPDATE_USER_TABLE(df):
	with open(f"database/user_list.json", 'w', encoding='utf-8') as f:
		return json.load(f)

# updateUsers = UPDATE_USER_TABLE()