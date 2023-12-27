import requests
import base64
import json
from urlextract import URLExtract
from supabase import create_client , Client

clietn_id = "2e70938512224563b7008d24060ca8fd"
client_secret = "711e07e611884465b309a0697d0f81c1"
supabase: Client = create_client("https://jtmmyaessuezbacyyuqx.supabase.co",
                                 "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp0bW15YWVzc3VlemJhY3l5dXF4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTA2Mjg0NjQsImV4cCI6MjAwNjIwNDQ2NH0.WvzjXcEV4aNEb1KXCGrqefcdDYjKJW_8XAaLKqMwh50")
def get_token():
    auth = clietn_id + ":" + client_secret
    auth_bytes = auth.encode("utf-8")
    auth_base64= str(base64.b64encode(auth_bytes),'utf-8')
    url = "https://accounts.spotify.com/api/token"
    header = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}
    res = requests.post(url,headers=header,data=data)
    json_res = json.loads(res.content)
    token = json_res["access_token"]
    return token
token = get_token()
print(token)

def get_authHeaders(token):
    return {
        "Authorization" : "Bearer " + token
    }
token = get_token()
headers = get_authHeaders(token)
extractor = URLExtract()

show_id= input("enter show id : ")
res = requests.get(f'https://api.spotify.com/v1/shows/{show_id}',headers=headers)
json_res = json.loads(res.content)
#epsiode number, episode name, description, guests, link websites -
#3dDGiHwKl3a6Dr2mzudPo1
episode_no = [item+1 for item in range(len(json_res['episodes']['items']))]

episode_name = [item['name'] for item in json_res['episodes']['items']]
episode_description = [item['description'] for item in json_res['episodes']['items']]
urls =  [ extractor.find_urls(desc) for desc in episode_description]

for  i in range(len(episode_no)):
    data,count = supabase.table("random_scraped").insert({"epsiode_number" : episode_no[i] , "episode_name" : episode_name[i] , "description" : episode_description[i] , "guests" : "null" , "link_websites" : urls[i]}).execute()
    print(i)
print("done")