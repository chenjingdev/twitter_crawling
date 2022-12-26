import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def INSERT_LINK_TABLE(df):
  print('insert')

def READ_LINK_TABLE(nickName):
	with open(f"database/twit_links/{nickName}_links.json", encoding='utf-8') as f:
		data = json.load(f)

def UPDATE_LINK_TABLE(user, tweetLinks):
	with open(f"database/twit_links/{user['user_name']}_links.json", "w") as f:
		json.dump(tweetLinks, f)
  
updateLink = UPDATE_LINK_TABLE