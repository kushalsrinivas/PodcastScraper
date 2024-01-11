import requests
import base64
import json
import re
from urlextract import URLExtract
from supabase import create_client, Client
from bs4 import BeautifulSoup

clietn_id = ""
client_secret = ""
supabase: Client = create_client("",
                                 "")


def get_token():
    auth = clietn_id + ":" + client_secret
    auth_bytes = auth.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    url = "https://accounts.spotify.com/api/token"
    header = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    res = requests.post(url, headers=header, data=data)
    json_res = json.loads(res.content)
    token = json_res["access_token"]
    return token


token = get_token()
print(token)


def get_authHeaders(token):
    return {
        "Authorization": "Bearer " + token
    }


token = get_token()

headers = get_authHeaders(token)
extractor = URLExtract()

show_id = input("enter show id : ")
temp = requests.get(f'https://api.spotify.com/v1/shows/{show_id}?limit=50', headers=headers)
temp_json_res = json.loads(temp.content)
total_episosdes = temp_json_res['episodes']['total']
# epsiode number, episode name, description, guests, link websites -
# 1lGD5wIfhnE4bepja42C9S
offset = 0
episode_number = []
episode_name = []
episode_description = []
episode_urls = []


def getLinks(htmlText):
    soup = BeautifulSoup(htmlText, "html.parser")
    links = [link.get('href') for link in soup.find_all('a', attrs={'href': re.compile("^https://")})]
    return links


print("fetching details.....")

while total_episosdes >= 0:
    print(f"fetching {offset} episodes out of {total_episosdes} episodes")
    result = requests.get(f'https://api.spotify.com/v1/shows/{show_id}/episodes?offset={offset}&limit=50',
                          headers=headers)
    resjons = json.loads(result.content)
    no = [offset + item + 1 for item in range(len(resjons['items']))]
    name = [item['name'] for item in resjons['items']]
    desc = [item['description'] for item in resjons['items']]
    urls = [getLinks(item['html_description']) for item in resjons['items']]
    episode_number += no
    episode_name += name
    episode_description += desc
    episode_urls += urls
    offset += 50
    total_episosdes -= 50


print("done")
print("uploading to database")


def sendData():
    for i in range(len(episode_number)):
        data, count = supabase.table("podcasts").insert(
            {"epsiode_number": episode_number[i], "episode_name": episode_name[i],
             "description": episode_description[i],
             "guests": "null", "link_websites": episode_urls[i]}).execute()


print("uploading to database")
sendData()
print("done")
