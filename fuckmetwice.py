import zipfile
from lxml import etree
import xml.etree.ElementTree as ET
from io import BytesIO
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import requests
import json
from dotenv import load_dotenv
import os
from PIL import Image
from scipy.spatial.distance import hamming
from ebooklib.utils import debug
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

def extract_epub(filename):
    zip_file = zipfile.ZipFile(filename)
    # Split the file path into directory and file name
    directory, filename = os.path.split(filename)
    # Remove the file extension
    directory_without_extension = os.path.splitext(directory)[0]
    zip_file.extractall(path=f'{directory_without_extension}/temp')
    zip_file.close()
    return f"{directory_without_extension}/temp"

def find_opf(filename):
    directory, filename = os.path.split(filename)
    # Remove the file extension
    directory_without_extension = os.path.splitext(directory)[0]
    os.walk(f'{directory_without_extension}/temp')
    for root, dirs, files in os.walk(f'{directory_without_extension}/temp'):
        for i in files:
            if ".opf" in i:
                print('found opf')
                return f'{root}/{i}'
            break
def get_opf_title(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    '''
    <?xml version="1.0"  encoding="UTF-8"?>
    <package xmlns="http://www.idpf.org/2007/opf" unique-identifier="0aea9f43-d4a9-4bf7-bebc-550a512f9b95" version="2.0">
        <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
            <dc:title>Shikimori's Not Just a Cutie, Vol. 1</dc:title>
            <dc:creator opf:role="aut" opf:file-as="Maki, Keigo">Keigo Maki</dc:creator>
            <dc:identifier id="0aea9f43-d4a9-4bf7-bebc-550a512f9b95" opf:scheme="UUID">
            0aea9f43-d4a9-4bf7-bebc-550a512f9b95
            </dc:identifier>
            <dc:publisher>Kodansha Comics</dc:publisher>
            <dc:subject>Slice of Life</dc:subject>
            <dc:subject>Humour</dc:subject>
            <dc:subject>School Life</dc:subject>
            <dc:subject>Comics</dc:subject>
            <dc:subject>Romance</dc:subject>
            <dc:subject>Young Adult</dc:subject>
            <dc:subject>Manga</dc:subject>
            <dc:subject>Comedy</dc:subject>
            <dc:description>&lt;p&gt;Shikimori seems like the perfect girlfriend: cute, fun to be around, sweet when she wants to be... but she has a cool dark side that comes out under the right circumstances. And her boyfriend Izumi loves to be around when that happens! A fun and funny high school romance with a sassy twist perfect for fans of Nagatoro-san and Komi Can't Communicate!  &lt;/p&gt;
            &lt;p&gt;Shikimori and Izumi are high school sweethearts. They hold hands walking home from school, they flirt in the halls, they tease each other. But Shikimori knows what she wants, and how to get it, and she can turn from cutie to cool in an instant.&lt;/p&gt;</dc:description>
            <dc:contributor opf:role="bkp">calibre (6.25.0) [https://calibre-ebook.com]</dc:contributor>
            <dc:date>2019-06-07T07:00:00+00:00</dc:date>
            <dc:language>en</dc:language>
            <dc:identifier opf:scheme="calibre">388f736e-5b36-4022-af64-74d2710bb660</dc:identifier>
            <dc:identifier opf:scheme="GOODREADS">55504721</dc:identifier>
            <dc:identifier opf:scheme="AMAZON">1646511751</dc:identifier>
            <dc:identifier opf:scheme="ISBN">9781646511754</dc:identifier>
            <meta name="calibre:title_sort" content="Shikimori's Not Just a Cutie, Vol. 1"/>
            <meta name="calibre:series" content="可愛いだけじゃない式守さん [Kawaii dake ja Nai Shikimori-san]"/>
            <meta name="calibre:series_index" content="1.0"/>
            <meta name="calibre:rating" content="8.0"/>
            <meta name="cover" content="cover"/>
        </metadata>
    '''
    genre = []
    for i in root:
        for e in i:
            if e.tag == '{http://purl.org/dc/elements/1.1/}title':
                title = e.text
                return title
                break















def main(e_book_path,opf_location,filename):
    def get_orig_filename(filename):
        directory, filename = os.path.split(filename)
        # Remove the file extension
        directory_without_extension = os.path.splitext(directory)[0]
        return directory_without_extension
    title = get_opf_title(opf_location)



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
                split_text = title.split(" - ")
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
            #write to xml, then figure out a way to zip it into a epub
            tree = ET.parse(opf_location)
            root = tree.getroot()
            #make a new folder using author from xml
            for i in root:
                for e in i:
                    if e.tag == '{http://purl.org/dc/elements/1.1/}title':
                        print(e.text)
                        title = e.text
                        break
            dir_of_file = get_orig_filename(filename)
            if os.path.isdir(f'{dir_of_file}/{title}') == False:
                os.mkdir(f'{dir_of_file}/{title}')
            else:
                pass
            #copy everything from temp folder to new folder and delete the temp folder
            os.system(f'robocopy temp {dir_of_file}/{title} /s /e')
            os.system(f'rmdir /s /q temp')

            
            

    else:
        print("Fatal Error:", response.status_code)
filename2 = extract_epub(filename)
print(filename2)
opf_location = find_opf(filename2)
print(opf_location)
main(filename,opf_location,filename)
pause = input('pause')