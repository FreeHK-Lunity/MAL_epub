import ebookmeta

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import requests
import json
from dotenv import load_dotenv
import os


load_dotenv()
client_id = os.getenv("CLIENT_ID")
print(client_id)
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

def main(e_book_path):
    meta = ebookmeta.get_metadata(f'{e_book_path}')
    e = meta.title
    title = e[0][0].strip()
    #print(title)
    url = "https://api.myanimelist.net/v2/manga"
    headers = {
        "X-MAL-CLIENT-ID": f"{client_id}"
    }
    params = {
        "q": f"{title}",
        "fields": "alternative_titles"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        # Process the data as needed
        json_data = data
        #save to json file
        with open('data.json', 'w',encoding='utf-8') as outfile:
            json.dump(json_data, outfile, indent=4)
        #load json file
        with open('data.json',encoding='utf-8') as json_file:
            json_file = json.load(json_file)
        for item in json_file['data']:
            if title == item['node']['title'] or item['node']['alternative_titles']['synonyms'] == title or item['node']['alternative_titles']['en'] == title or item['node']['alternative_titles']['ja'] == title:
                title_exists = True
                print(f'{title} exists in MAL!!')
                get_the_id = item['node']['id']
                break
            else:
                title_exists = False
                print(f'you`re out of luck m8, {title} does not exist in MAL :(')
                break
        if title_exists == True:
            url = f"https://api.myanimelist.net/v2/manga/{get_the_id}"
            headers = {
                "X-MAL-CLIENT-ID": f"{client_id}"
            }
            params = {
                "fields": "main_picture,alternative_titles,main_picture,authors{first_name,last_name},mean,genres,start_date,background"
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                # Process the data as needed
            json_data = data
            #save to json file
            with open('data2.json', 'w',encoding='utf-8') as outfile:
                json.dump(json_data, outfile, indent=4)
            #load json file
            with open('data2.json',encoding='utf-8') as json_file:
                json_file = json.load(json_file)
            meta.title = f'{title} - {json_file["alternative_titles"]["ja"]}'
            meta.author_list = f'{json_file["authors"]["node"]["first_name"]} {json_file["authors"]["node"]["last_name"]}'
            meta.description = f'{json_file["background"]}'
    else:
        print("Error:", response.status_code)
main(filename)