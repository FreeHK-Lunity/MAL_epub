import ebookmeta
from io import BytesIO
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import requests
import json
from dotenv import load_dotenv
import os
from PIL import Image
from scipy.spatial.distance import hamming

#https://machinelearningknowledge.ai/ways-to-calculate-levenshtein-distance-edit-distance-in-python/
def levenshtein_distance(s, t):
    m = len(s)
    n = len(t)
    d = [[0] * (n + 1) for i in range(m + 1)]  

    for i in range(1, m + 1):
        d[i][0] = i

    for j in range(1, n + 1):
        d[0][j] = j
    
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i - 1][j] + 1,      # deletion
                          d[i][j - 1] + 1,      # insertion
                          d[i - 1][j - 1] + cost) # substitution   

    return d[m][n]







load_dotenv()
client_id = os.getenv("CLIENT_ID")
print(client_id)
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

def main(e_book_path):
    meta = ebookmeta.get_metadata(f'{e_book_path}')
    e = meta.title
    split_text = e.split(" - ")
    title = split_text[0]
    print(title)
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
                #title_exists = False
                #print(f'you`re out of luck m8, {title} does not exist in MAL :(')
                title = e.strip()
                if title == item['node']['title'] or item['node']['alternative_titles']['synonyms'] == title or item['node']['alternative_titles']['en'] == title or item['node']['alternative_titles']['ja'] == title:
                    title_exists = True
                    print(f'{title} exists in MAL!!')
                    get_the_id = item['node']['id']
                    break
                else:
                    title = e.strip()
                    string1 = title
                    string2 = item['node']['title']
                    title_exists = False
                    l_dist = levenshtein_distance(string1, string2)
                    if l_dist <= 60:
                        print(f'{title} exists in MAL!!')
                        get_the_id = item['node']['id']
                        title_exists = True
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
                "fields": "main_picture,alternative_titles,main_picture,authors{first_name,last_name},mean,genres,start_date,synopsis,serialization,start_date"
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
            for i in json_file["authors"]:
                meta.set_author_list_from_string(f'{i["node"]["first_name"]} {i["node"]["last_name"]}')
            meta.description = f'{json_file["synopsis"]}'
            print(meta.description)
            for i in json_file["genres"]:
                genrelist = []
                genrelist.append(i["name"])
                
            meta.set_tag_list_from_string = f'{genrelist}'
            #print(meta.tag_list)
            for i in json_file["serialization"]:
                meta.publisher = f'{i["node"]["name"]}'
                #print(meta.publisher)
            response = requests.get(f'{json_file["main_picture"]["large"]}')
            img = Image.open(BytesIO(response.content))

            meta.cover_image_data = img
            ebookmeta.set_metadata(f'{e_book_path}', meta)
            
            

    else:
        print("Fatal Error:", response.status_code)
main(filename)