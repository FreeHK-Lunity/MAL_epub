import ebookmeta
from ebooklib import epub
from io import BytesIO
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import requests
import json
from dotenv import load_dotenv
import os
from PIL import Image
from scipy.spatial.distance import hamming


import threading
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
    book = epub.read_epub(f'{e_book_path}')
    book_forced_to_make_a_new_one = epub.EpubBook()
    meta = epub.read_epub(f'{e_book_path}')
    e = meta.get_metadata('DC', 'title')
    title = e[0][0].strip()
    print(title)
    #print(e)
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
                print(f'Found {title} in Stage 1')
                get_the_id = item['node']['id']
                break
            else:
                #title_exists = False
                #print(f'you`re out of luck m8, {title} does not exist in MAL :(')
                split_text = e[0][0].split(" - ")
                title = split_text[0]
                if title == item['node']['title'] or item['node']['alternative_titles']['synonyms'] == title or item['node']['alternative_titles']['en'] == title or item['node']['alternative_titles']['ja'] == title:
                    title_exists = True
                    print(f'{title} exists in MAL!!')
                    print(f'Found {title} in Stage 2')
                    get_the_id = item['node']['id']
                    break
                else:
                    try:
                        title = split_text[1]
                    except:
                        pass
                    if title == item['node']['title'] or item['node']['alternative_titles']['synonyms'] == title or item['node']['alternative_titles']['en'] == title or item['node']['alternative_titles']['ja'] == title:
                        title_exists = True
                        print(f'{title} exists in MAL!!')
                        print(f'Found {title} in Stage 3')
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
                            print(f'Found {title} in Stage 4')
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

            
            ##########REIMPLEMENTING IN EBOKLIB############
            book_forced_to_make_a_new_one.set_title(f'{title} - {json_file["alternative_titles"]["ja"]}')
            for i in json_file["authors"]:
                book_forced_to_make_a_new_one.add_author(f'{i["node"]["first_name"]} {i["node"]["last_name"]}')
                #print(book_forced_to_make_a_new_one.get_metadata('DC', 'creator'))
            book_forced_to_make_a_new_one.add_metadata('DC', 'description', f'{json_file["synopsis"]}')
            for i in json_file["genres"]:
                genrelist = []
                genrelist.append(i["name"])
                book_forced_to_make_a_new_one.add_metadata('DC', 'subject', f'{json_file["synopsis"]}')
            
            #print(meta.tag_list)
            for i in json_file["serialization"]:
                book_forced_to_make_a_new_one.add_metadata('DC', 'publisher', f'{i["node"]["name"]}')
                #print(meta.publisher)
            response = requests.get(f'{json_file["main_picture"]["large"]}')
            img = Image.open(BytesIO(response.content))
            image_data = img.tobytes()
            #<meta name="cover" content="image_0000"/>
            book_forced_to_make_a_new_one.set_cover("image_0000", image_data)
            book_forced_to_make_a_new_one.set_direction('ltr')
            getallitems = book.get_items()
            for i in getallitems:
                book_forced_to_make_a_new_one.add_item(i)
            # Split the file path into directory and file name
            directory, filename = os.path.split(e_book_path)

            # Remove the file extension
            directory_without_extension = os.path.splitext(directory)[0]
            
            epub.write_epub(f'{directory_without_extension}/{title}.epub', book_forced_to_make_a_new_one)
            def write_epub_thread(directory, title, book):
                epub.write_epub(f'{directory}/{title}.epub', book)

            # Create a new thread
            thread = threading.Thread(target=write_epub_thread, args=(directory_without_extension, title, book_forced_to_make_a_new_one))

            # Start the thread
            thread.start()

            # Wait for the thread to complete
            thread.join()
            
main(filename)
