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
import re
import threading
import xml.dom.minidom
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


def is_windows_illegal(filename):
    illegal_chars = r'[<>:"/\\|?*\x00-\x1F]'
    match = re.search(illegal_chars, filename)
    return match is not None

def sanitize_filename(filename):
    illegal_chars = r'[<>:"/\\|?*\x00-\x1F]'
    sanitized_filename = re.sub(illegal_chars, '_', filename)
    return sanitized_filename

def make_xhtml():
    pass

def get_numeric_part(filename):
    return int(os.path.splitext(filename)[0].split('_')[0])


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


def pause():
    pause = input('pause')


def send_request(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    return response

def check_MAL_existance(reque,title):
    if reque.status_code == 200:
        data = reque.json()
        # Process the data as needed
        json_data = data
        #save to json file
        with open('data.json', 'w',encoding='utf-8') as outfile:
            json.dump(json_data, outfile, indent=4)
        #load json file
        with open('data.json',encoding='utf-8') as json_file:
            json_file = json.load(json_file)
        title.strip('\n')
        title_exists = False
        for item in json_file['data']:
            if title_exists == True:
                break
            '''            
            if '\n' in title:
            title = title.replace('\n', '')
            title.strip()
            '''
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
                    print(get_the_id)
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
                        print(get_the_id)
                        break
                    else:
                        string1 = title
                        string2 = item['node']['title']
                        title_exists = False
                        l_dist = levenshtein_distance(string1, string2)
                        print(l_dist)
                        if l_dist >= 49:
                            print(f'{title} exists in MAL!!')
                            print(f'Found {title} in Stage 4')
                            get_the_id = item['node']['id']
                            title_exists = True
                            print(get_the_id)
                            
                        else:
                            title_exists = False
                            print(f'you`re out of luck m8, {title} does not exist in MAL :(')

        if title_exists == True:
            return title_exists,get_the_id
        else:
            return title_exists,title_exists



def literally_write_everything_to_content_opf(tree,root,json_file,future_id,dir_of_file,author):
    for i in root:
        if i.tag == "{http://www.idpf.org/2007/opf}metadata":
            i.clear()
            # Create new child elements
            title = ET.Element('{http://purl.org/dc/elements/1.1/}title')
            title.text = f'{json_file["alternative_titles"]["ja"]} - {json_file["title"]}'
            i.append(title)
            
            language = ET.Element('{http://purl.org/dc/elements/1.1/}language')
            language.text = 'en'
            i.append(language)
            
            identifier = ET.Element('{http://purl.org/dc/elements/1.1/}identifier')
            identifier.set('id', f'{future_id}')
            identifier.set('{http://www.idpf.org/2007/opf}scheme', 'UUID')
            identifier.text = f'{future_id}'
            i.append(identifier)
            


            if bool(json_file['serialization']) == False:
                pass
            else:
                for e in json_file['serialization']:
                    publisher = ET.Element('{http://purl.org/dc/elements/1.1/}publisher')
                    publisher.text = f'{e["node"]["name"]}'
                    i.append(publisher)
                    
            if bool(json_file["alternative_titles"]['synonyms']) == False:
                pass
            else:
                alternative_titles = ET.Element('{http://purl.org/dc/elements/1.1/}title')
                alternative_titles.text = f'{json_file["alternative_titles"]["synonyms"]}'
                i.append(alternative_titles)
                


            alternative_titles = ET.Element('{http://purl.org/dc/elements/1.1/}title')
            alternative_titles.text = f'{json_file["alternative_titles"]["en"]}'
            i.append(alternative_titles)
            
            alternative_titles = ET.Element('{http://purl.org/dc/elements/1.1/}title')
            alternative_titles.text = f'{json_file["alternative_titles"]["ja"]}'
            i.append(alternative_titles)
            
            for e in json_file['genres']:
                subject = ET.Element('{http://purl.org/dc/elements/1.1/}subject')
                subject.text = f'{e["name"]}'
                i.append(subject)
                
            for e in json_file['authors']:
                if e['role'] == 'Story & Art' or e['role'] == 'Story':
                    creator = ET.Element('{http://purl.org/dc/elements/1.1/}creator')
                    creator.set('{http://www.idpf.org/2007/opf}role', 'aut')
                    creator.set('{http://www.idpf.org/2007/opf}file-as', f'{e["node"]["last_name"]}, {e["node"]["first_name"]}')
                    creator.text = f'{e["node"]["first_name"]} {e["node"]["last_name"]}'
                    i.append(creator)
                    
            description = ET.Element('{http://purl.org/dc/elements/1.1/}description')
            description.text = f'{json_file["synopsis"]}'
            i.append(description)
            
            date = ET.Element('{http://purl.org/dc/elements/1.1/}date')
            date.text = f'{json_file["start_date"]}'
            i.append(date)
            
            #<meta name="cover" content="cover"/>
            cover = ET.Element('{http://www.idpf.org/2007/opf}meta')
            cover.set('name', 'cover')
            cover.set('content', 'cover')
            i.append(cover)
            
            '''
            <meta name="fixed-layout" content="true"/>
            <meta name="original-resolution" content="1264x1680"/>
            <meta name="book-type" content="comic"/>
            <meta name="primary-writing-mode" content="horizontal-rl"/>
            <meta name="zero-gutter" content="true"/>
            <meta name="zero-margin" content="true"/>
            <meta name="ke-border-color" content="#FFFFFF"/>
            <meta name="ke-border-width" content="0"/>
            <meta property="rendition:spread">landscape</meta>
            <meta property="rendition:layout">pre-paginated</meta>
            <meta name="orientation-lock" content="none"/>
            <meta name="region-mag" content="true"/>
            
            '''
            book_type = ET.Element('{http://www.idpf.org/2007/opf}meta')
            book_type.set('name', 'book-type')
            book_type.set('content', 'comic')
            i.append(book_type)

            primary_writing_mode = ET.Element('{http://www.idpf.org/2007/opf}meta')
            primary_writing_mode.set('name', 'primary-writing-mode')
            primary_writing_mode.set('content', 'horizontal-rl')
            i.append(primary_writing_mode)

            zero_gutter = ET.Element('{http://www.idpf.org/2007/opf}meta')
            zero_gutter.set('name', 'zero-gutter')
            zero_gutter.set('content', 'true')
            i.append(zero_gutter)

            zero_margin = ET.Element('{http://www.idpf.org/2007/opf}meta')
            zero_margin.set('name', 'zero-margin')
            zero_margin.set('content', 'true')
            i.append(zero_margin)

            ke_border_color = ET.Element('{http://www.idpf.org/2007/opf}meta')
            ke_border_color.set('name', 'ke-border-color')
            ke_border_color.set('content', '#FFFFFF')
            i.append(ke_border_color)

            ke_border_width = ET.Element('{http://www.idpf.org/2007/opf}meta')
            ke_border_width.set('name', 'ke-border-width')
            ke_border_width.set('content', '0')
            i.append(ke_border_width)

            rendition_spread = ET.Element('{http://www.idpf.org/2007/opf}meta')
            rendition_spread.set('property', 'rendition:spread')
            rendition_spread.text = 'landscape'
            i.append(rendition_spread)

            rendition_layout = ET.Element('{http://www.idpf.org/2007/opf}meta')
            rendition_layout.set('property', 'rendition:layout')
            rendition_layout.text = 'pre-paginated'
            i.append(rendition_layout)

            orientation_lock = ET.Element('{http://www.idpf.org/2007/opf}meta')
            orientation_lock.set('name', 'orientation-lock')
            orientation_lock.set('content', 'none')
            i.append(orientation_lock)

            region_mag = ET.Element('{http://www.idpf.org/2007/opf}meta')
            region_mag.set('name', 'region-mag')
            region_mag.set('content', 'true')
            i.append(region_mag)

            fixed_layout = ET.Element('{http://www.idpf.org/2007/opf}meta')
            fixed_layout.set('name', 'fixed-layout')
            fixed_layout.set('content', 'true')
            i.append(fixed_layout)

            '''            original_resolution = ET.Element('{http://www.idpf.org/2007/opf}meta')
            original_resolution.set('name', 'original-resolution')
            img = Image.open(f'{dir_of_file}/{author}/{title.text}/OEBPS/images/0_000.png')
            width, height = img.size
            original_resolution.set('content', f'{width}x{height}')
            i.append(original_resolution)'''




            title.text.strip('.')
            title = sanitize_filename(title.text)
            filename = "cover.jpg" # Replace with your image name
            response = requests.get(f'{json_file["main_picture"]["large"]}')
            if response.status_code == 200: # Check if the request was successful
                try:
                    with open(f'{dir_of_file}/{author}/{title.strip(".:")}/OEBPS/{filename}', "wb") as f: # Open a file in write-binary mode
                        f.write(response.content) # Write the content of the response to the file
                except:
                    with open(f'{dir_of_file}/{author}/{title.strip(".:")}/EPUB/{filename}', "wb") as f:
                        f.write(response.content)

                    
            else:
                print("cover could not be downloaded")
        if i.tag == '{http://www.idpf.org/2007/opf}manifest':
            i.clear()
            i.append(ET.Element('{http://www.idpf.org/2007/opf}item', attrib={'href': 'cover.jpg','id': 'cover',  'media-type': 'image/jpeg'}))
            i.append(ET.Element('{http://www.idpf.org/2007/opf}item', attrib={'href': 'toc.ncx','id': 'ncx',  'media-type': 'application/x-dtbncx+xml'}))
            pass
        if i.tag == '{http://www.idpf.org/2007/opf}spine':
            i.clear()
            pass
            
            


        
    ET.indent(tree, '  ')
        # Insert the XML declaration at the beginning of the root element
    try:    
        tree.write(f'{dir_of_file}/{json_file["authors"][0]["node"]["first_name"]} {json_file["authors"][0]["node"]["last_name"]}/{title.strip(".:")}/OEBPS/content.opf', encoding='utf-8', xml_declaration=True)
    except:
        tree.write(f'{dir_of_file}/{json_file["authors"][0]["node"]["first_name"]} {json_file["authors"][0]["node"]["last_name"]}/{title.strip(".:")}/EPUB/content.opf', encoding='utf-8', xml_declaration=True)

#now write some gay xmls for the images

'''
<item id="cover" href="Images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>
<item id="page_Images_kcc-0000-kcc" href="Text/kcc-0000-kcc.xhtml" media-type="application/xhtml+xml"/>
<item id="img_Images_kcc-0000-kcc" href="Images/kcc-0000-kcc.jpg" media-type="image/jpeg"/>
<item id="page_Images_kcc-0001-kcc" href="Text/kcc-0001-kcc.xhtml" media-type="application/xhtml+xml"/>
<item id="img_Images_kcc-0001-kcc" href="Images/kcc-0001-kcc.jpg" media-type="image/jpeg"/>
<item id="page_Images_kcc-0002-kcc" href="Text/kcc-0002-kcc.xhtml" media-type="application/xhtml+xml"/>
<item id="img_Images_kcc-0002-kcc" href="Images/kcc-0002-kcc.jpg" media-type="image/jpeg"/>
'''

def append_manifest(folder_path):
    sorted_filenames = sorted(os.listdir(f'{folder_path}/OEBPS/images'), key=get_numeric_part)
    for i in sorted_filenames:
        i = os.path.splitext(i)[0] # strip file extension
        tree = ET.parse(f'{folder_path}/OEBPS/content.opf')
        root = tree.getroot()
        manifest = root.find('{http://www.idpf.org/2007/opf}manifest')
        item = ET.Element('{http://www.idpf.org/2007/opf}item')
        
        item.set('id', f'page_{i}')
        item.set('href', f'xhtml/{i}.xhtml')
        item.set('media-type', 'application/xhtml+xml')
        manifest.append(item)
        
        item = ET.Element('{http://www.idpf.org/2007/opf}item')  # Create a new item element
        
        item.set('id', f'img_{i}')
        item.set('href', f'images/{i}.png')
        item.set('media-type', 'image/png')  # Corrected media-type for PNG images
        if os.path.exists(f'{folder_path}/OEBPS/images/{i}.jpeg'):
            item.set('href', f'images/{i}.jpeg')
            item.set('media-type', 'image/jpeg')
        elif os.path.exists(f'{folder_path}/OEBPS/images/{i}.jpg'):
            item.set('href', f'images/{i}.jpg')
            item.set('media-type', 'image/jpeg')
        manifest.append(item)
        # Append the item element to the manifest element


        ET.indent(tree, '  ')
        tree.write(f'{folder_path}/OEBPS/content.opf')
    item = ET.Element('{http://www.idpf.org/2007/opf}item')  # Create a new item element
    item.set('id', 'css')
    item.set('href', 'xhtml/style.css')
    item.set('media-type', 'text/css')
    manifest.append(item)
    ET.indent(tree, '  ')
    tree.write(f'{folder_path}/OEBPS/content.opf')
        

def edit_spine(folder_path,xd):
    sorted_filenames = sorted(os.listdir(f'{folder_path}/OEBPS/images'), key=get_numeric_part)
    for i in sorted_filenames:
        xd +=1

                
        tree = ET.parse(f'{folder_path}/OEBPS/content.opf')
        root = tree.getroot()
        spine = root.find('{http://www.idpf.org/2007/opf}spine')
        spine.set('page-progression-direction', 'rtl')
        itemref = ET.Element('{http://www.idpf.org/2007/opf}itemref')
        for ext in ['.jpg', '.png', '.jpeg']:
            if i.endswith(ext):
                itemref.set('idref', f'page_{i.strip(ext)}')
        itemref.set('linear', 'yes')
        if xd == 1:
            itemref.set('properties', 'page-spread-right')
        elif xd == 2:
            itemref.set('properties', 'page-spread-left')
            xd = 0
        spine.append(itemref)
        ET.indent(tree, '  ')
        tree.write(f'{folder_path}/OEBPS/content.opf')

        



def literally_write_everything_to_xhtml(folder_path):
    for i in os.listdir(f'{folder_path}/OEBPS/images'):
        # I SWEAR THERE IS A BETTER WAY TO DO THIS
        # I CANT FIGURE IT OUT SO ILL JUST DO IT THE DUMB WAY
        if i.endswith(('.jpg', '.png', '.jpeg')):
            img_path = f'{folder_path}/OEBPS/images/{i}'
            img = Image.open(img_path)
            width, height = img.size
        

        # Create the XML tree
        tree = ET.ElementTree()


        # Create the declaration element
        declaration = ET.Comment('xml version="1.0" encoding="UTF-8"')
        tree._setroot(declaration)

        html = ET.Element('html', xmlns='http://www.w3.org/1999/xhtml', xmlns_epub='http://www.idpf.org/2007/ops')
        tree._setroot(html)

        head = ET.Element('head')
        html.append(head)

        title = ET.Element('title')
        title.text = f'{i.strip(".png")}'
        head.append(title)

        link = ET.Element('link', href='style.css', type='text/css', rel='stylesheet')
        head.append(link)

        meta = ET.Element('meta', name='viewport', content=f'width={width}, height={height}')
        head.append(meta)

        body = ET.Element('body', style='')
        html.append(body)

        img = ET.Element('img', width=f'{width}', height=f'{height}', src=f'../images/{i}')
        div = ET.Element('div', style=f'text-align:center;top:0.0%;')
        div.append(img)
        body.append(div)
        div = ET.Element('div', id='PV')    
        div2 = ET.Element('div', id='PV-TL')
        a = ET.Element('a', style='display:inline-block;width:100%;height:100%;', class_='app-amzn-magnify', data_app_amzn_magnify='{"targetId":"PV-TL-P", "ordinal":2}')
        div2.append(a)
        div.append(div2)
        div2 = ET.Element('div', id='PV-TR')
        a = ET.Element('a', style='display:inline-block;width:100%;height:100%;', class_='app-amzn-magnify', data_app_amzn_magnify='{"targetId":"PV-TR-P", "ordinal":1}')
        div2.append(a)
        div.append(div2)
        div2 = ET.Element('div', id='PV-BL')
        a = ET.Element('a', style='display:inline-block;width:100%;height:100%;', class_='app-amzn-magnify', data_app_amzn_magnify='{"targetId":"PV-BL-P", "ordinal":4}')
        div2.append(a)
        div.append(div2)
        div2 = ET.Element('div', id='PV-BR')
        a = ET.Element('a', style='display:inline-block;width:100%;height:100%;', class_='app-amzn-magnify', data_app_amzn_magnify='{"targetId":"PV-BR-P", "ordinal":3}')
        div2.append(a)
        div.append(div2)
        body.append(div)
        list_of_ids = ['PV-TL-P','PV-TR-P','PV-BL-P','PV-BR-P']
        xd = 0
        for j in list_of_ids:
            xd += 1
            div = ET.Element('div', class_='PV-P', id=f'{j}', style='')
            if xd == 1:
                img = ET.Element('img', style='position:absolute;left:0;top:0;', src=f'../images/{i}', width=f' {width*(3/2)}', height=f'{height*(3/2)}')
            elif xd == 2:
                img = ET.Element('img', style='position:absolute;right:0;top:0;', src=f'../images/{i}', width=f' {width*(3/2)}', height=f'{height*(3/2)}')
            elif xd == 3:
                img = ET.Element('img', style='position:absolute;left:0;bottom:0;', src=f'../images/{i}', width=f' {width*(3/2)}', height=f'{height*(3/2)}')
            elif xd == 4:
                img = ET.Element('img', style='position:absolute;right:0;bottom:0;', src=f'../images/{i}', width=f' {width*(3/2)}', height=f'{height*(3/2)}')
                xd = 0
            div.append(img)
            body.append(div)
        #html.append(body)
        #print(ET.tostring(root, encoding='utf-8', method='xml').decode())
        #pause()
        #tree = ET.ElementTree(root)
        ET.indent(tree, '  ')

        for ext in ['.jpg', '.png', '.jpeg']:
            if i.endswith(ext):
                file_path = f'{folder_path}/OEBPS/xhtml/{i.strip(ext)}.xhtml'
                tree.write(file_path, encoding='utf-8', xml_declaration=True)
                with open(file_path, 'r+', encoding='utf-8') as file:
                    content = file.read().replace('class_', 'class')
                    file.seek(0)
                    file.write(content)
                    file.truncate()

        






#contents of css file
'''

'''
#github copilot make it into a real css file for me thanks
def write_a_css_file(folder_path):
    file = open(f'{folder_path}/OEBPS/xhtml/style.css', 'w', encoding='utf-8')
    
    file.write('''@page {
margin: 0;
}
body {
display: block;
margin: 0;
padding: 0;
}
#PV {
position: absolute;
width: 100%;
height: 100%;
top: 0;
left: 0;
}
#PV-T {
top: 0;
width: 100%;
height: 50%;
}
#PV-B {
bottom: 0;
width: 100%;
height: 50%;
}
#PV-L {
left: 0;
width: 49.5%;
height: 100%;
float: left;
}
#PV-R {
right: 0;
width: 49.5%;
height: 100%;
float: right;
}
#PV-TL {
top: 0;
left: 0;
width: 49.5%;
height: 50%;
float: left;
}
#PV-TR {
top: 0;
right: 0;
width: 49.5%;
height: 50%;
float: right;
}
#PV-BL {
bottom: 0;
left: 0;
width: 49.5%;
height: 50%;
float: left;
}
#PV-BR {
bottom: 0;
right: 0;
width: 49.5%;
height: 50%;
float: right;
}
.PV-P {
width: 100%;
height: 100%;
top: 0;
position: absolute;
display: none;
}
''')
    file.close()
#i hope this works





def make_a_new_folder_func(json_file,filename):
    author = f'{json_file["authors"][0]["node"]["first_name"]} {json_file["authors"][0]["node"]["last_name"]}'
    title = f'{json_file["alternative_titles"]["ja"]} - {json_file["title"]}'
    dir_of_file = filename
    title = sanitize_filename(title)
    if os.path.isdir(f'{dir_of_file}/{author}/{title.strip(".:")}') == False:
        os.makedirs(f'{dir_of_file}/{author}/{title.strip(".:")}')
    else:
        pass
    #copy everything from temp folder to new folder and delete the temp folder
    os.system(f'robocopy "{dir_of_file}/temp" "{dir_of_file}/{author}/{title.strip(".:")}" /s /e')
    os.system(f'rmdir /s /q "{dir_of_file}/temp"')


# WIP 
def edit_ncx(folder_path):
    with open(f'{folder_path}/OEBPS/toc.ncx', 'r', encoding='utf-8') as f:
        xml_string = f.read()

    # Parse the XML string into a DOM object
    dom = xml.dom.minidom.parseString(xml_string)

    # Indent the DOM object
    xml_string_indented = dom.toprettyxml()

    # Export the indented XML string to a file
    with open(f'{folder_path}/OEBPS/toc_indented.ncx', 'w', encoding='utf-8') as f:
        f.write(xml_string_indented)

    tree = ET.parse(f'{folder_path}/OEBPS/toc_indented.ncx')
    leading_digit = os.listdir(f'{folder_path}/OEBPS/images')[0].split('_')[1].split('.')[0]
    leading_digit = len(leading_digit)
    print(leading_digit)
    root = tree.getroot()
    # iterate 
    current_img_no = 0
    '''    
    print(root)
    for child in root:
        print(child.tag, child.attrib)
        for child2 in child:
            print(child2.tag, child2.attrib)
            for child3 in child2:
                print(child3.tag, child3.attrib)
    '''
    for i in root:
        if i.tag == '{http://www.daisy.org/z3986/2005/ncx/}navMap':
            for j in i:
                if j.tag == '{http://www.daisy.org/z3986/2005/ncx/}navPoint':
                    toc_tag = j.get('id')
                    toc_tag = toc_tag.split('_')
                    chapter_number = toc_tag[1]
                    #print(chapter_number)
                    for k in j: # we need to set the src no here | this is the starting page of the chapter
                        if k.tag == '{http://www.daisy.org/z3986/2005/ncx/}content':
                            # this is the starting page of the chapter
                            #print(f'xhtml/{chapter_number}_{str(current_img_no).zfill(leading_digit)}.xhtml')
                            k.set('src', f'xhtml/{chapter_number}_{str(current_img_no).zfill(leading_digit)}.xhtml')
                            # print(k.attrib)
                        for l in k: #this is where the actual page is stored
                            if l.tag == '{http://www.daisy.org/z3986/2005/ncx/}content':
                                l.set('src', f'xhtml/{chapter_number}_{str(current_img_no).zfill(leading_digit)}.xhtml')
                                current_img_no += 1
                                # print(l.attrib)
    ET.indent(tree, '  ')
    tree.write(f'{folder_path}/OEBPS/toc.ncx')
    os.remove(f'{folder_path}/OEBPS/toc_indented.ncx')

    
    
    '''  
        current_img_no =+1
    # k.set('src', f'xhtml/{k.get("src")}')
    print(k.tag, k.attrib)
    print('getting!')  
    # Determine the starting index for new data
    starting_index = max_index + 1

    # Iterate over the navPoint elements
    for nav_point in root.findall(".//navPoint"):
        nav_point_id = nav_point.get("id")

        # Update the id attribute if it starts with "TOC_0_"
        if nav_point_id.startswith("TOC_0_"):
            updated_id = nav_point_id.replace("TOC_0_", f"TOC_0_{starting_index}_")
            nav_point.set("id", updated_id)

        # Update the content src attribute if it starts with "xhtml/0_"
        content_element = nav_point.find("content")
        if content_element is not None:
            content_src = content_element.get("src")
            if content_src.startswith("xhtml/0_"):
                updated_src = content_src.replace("xhtml/0_", f"xhtml/{starting_index}_")
                content_element.set("src", updated_src)

        # Update the text element if it starts with "Page "
        text_element = nav_point.find("navLabel/text")
        if text_element is not None:
            text = text_element.text
            if text.startswith("Page "):
                updated_text = f"Page {starting_index}"
                text_element.text = updated_text

        # Increment the starting index for new data
        starting_index += 1

    # Get the modified XML code
    modified_xml_code = ET.tostring(root, encoding="unicode")'''














def main(e_book_path,opf_location,filename,make_a_new_folder,ignore_MAL,manga_id):
    def get_orig_filename(filename):
        directory, filename = os.path.split(filename)
        # Remove the file extension
        directory_without_extension = os.path.splitext(directory)[0]
        return directory_without_extension # e.g D:\users\user\Documents\Mangas\Maou-sama to Kekkon shitai | since this location is derived from the original epub file path 
    title = get_opf_title(opf_location)
    print(title)
    #
    title = title.strip()
    print(title)
    title = sanitize_filename(title)
    print(title)
    #pause()
    url = "https://api.myanimelist.net/v2/manga"
    headers = {
        "X-MAL-CLIENT-ID": f"{client_id}"
    }
    params = {
        "q": f"{title}",
        "fields": "alternative_titles"
    }

    reque = send_request(url, headers, params)
    title_exists = check_MAL_existance(reque,title)
    
    if title_exists[0] == True and ignore_MAL == False:
        url = f"https://api.myanimelist.net/v2/manga/{title_exists[1]}"
        headers = {
            "X-MAL-CLIENT-ID": f"{client_id}"
        }
        params = {
            "fields": "main_picture,alternative_titles,main_picture,authors{first_name,last_name},mean,genres,start_date,synopsis,serialization,start_date"
        }
        response = send_request(url, headers, params)
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


    if ignore_MAL == True:
        url = f"https://api.myanimelist.net/v2/manga/{manga_id}"
        headers = {
            "X-MAL-CLIENT-ID": f"{client_id}"
        }
        params = {
            "fields": "main_picture,alternative_titles,main_picture,authors{first_name,last_name},mean,genres,start_date,synopsis,serialization,start_date"
        }
        response = send_request(url, headers, params)
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
    if make_a_new_folder == True:
        dir_of_file = get_orig_filename(filename)
        make_a_new_folder_func(json_file,dir_of_file)
    for i in root:
        for j in i:
            if j.tag == "{http://purl.org/dc/elements/1.1/}identifier":
                future_id = j.text
                break

    title = sanitize_filename(f'{json_file["alternative_titles"]["ja"]} - {json_file["title"]}')
    dir_of_file = get_orig_filename(filename)
    print(title)
    print(dir_of_file)
    try:
        tree = ET.parse(f'{dir_of_file}/{json_file["authors"][0]["node"]["first_name"]} {json_file["authors"][0]["node"]["last_name"]}/{title.strip(".:")}/OEBPS/content.opf')
    except:
        tree = ET.parse(f'{dir_of_file}/{json_file["authors"][0]["node"]["first_name"]} {json_file["authors"][0]["node"]["last_name"]}/{title.strip(".:")}/EPUB/content.opf')

    root = tree.getroot()
    declaration = ET.Element('xml', version='1.0', encoding='utf-8')
    root.insert(0, declaration)
    author = f'{json_file["authors"][0]["node"]["first_name"]} {json_file["authors"][0]["node"]["last_name"]}'
    title = f'{json_file["alternative_titles"]["ja"]} - {json_file["title"]}'
    title = sanitize_filename(title)
    literally_write_everything_to_content_opf(tree,root,json_file,future_id,dir_of_file,author)

        


    def add_folder_to_zip(folder_path, zip_file_path):
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)
        if os.path.supports_unicode_filenames:
            try:
                with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            if file_path == 'D:/users/user/Documents/Mangas/Mamahaha no Tsurego ga Moto Kanodatta/Kyousuke Kamishiro/継母の連れ子が元カノだった - Mamahaha no Tsurego ga Motokano datta\継母の連れ子が元カノだった - Mamahaha no Tsurego ga Motokano datta.epub':
                                pass
                            else:
                                zipf.write(file_path, os.path.relpath(file_path, folder_path))
                                print(f'Added {file_path} to {zip_file_path}')
            except FileNotFoundError:
                print("You may not have enabled long path support in Windows. Please enable it and try again.")
            else:
                print(f'Ran without errors. Added {folder_path} to {zip_file_path}')
                        

        # Specify the folder path and zip file path
    folder_path = f'{dir_of_file}/{json_file["authors"][0]["node"]["first_name"]} {json_file["authors"][0]["node"]["last_name"]}/{title}' #e.g D:\users\user\Documents\Mangas\Maou-sama to Kekkon shitai\Tanuma Ikeuchi\魔王様と結婚したい - Maou-sama to Kekkon shitai
    #                                                                                                                                          {                          dir_of_file                  }\{   author   }\{                  title                     }
    zip_file_path = f'{dir_of_file}/{json_file["authors"][0]["node"]["first_name"]} {json_file["authors"][0]["node"]["last_name"]}/{title}/{title}.epub'#e.g D:\users\user\Documents\Mangas\Maou-sama to Kekkon shitai\Tanuma Ikeuchi\魔王様と結婚したい - Maou-sama to Kekkon shitai\魔王様と結婚したい - Maou-sama to Kekkon shitai.epub
    #
    
    os.listdir(f'{folder_path}/OEBPS/images')[0]
    img = Image.open(f'{folder_path}/OEBPS/images/{os.listdir(f"{folder_path}/OEBPS/images")[0]}')
    width, height = img.size
    edit_ncx(folder_path)
    literally_write_everything_to_xhtml(folder_path)
    write_a_css_file(folder_path)
    append_manifest(folder_path)
    edit_spine(folder_path,0)
    # Call the function to add the folder to the zip file
    add_folder_to_zip(folder_path, zip_file_path)
            

    if reque.status_code != 200:
        print("Fatal Error:", reque.status_code)
filename2 = extract_epub(filename)
print(filename2)

opf_location = find_opf(filename2)
print(opf_location)

main(filename,opf_location,filename,True,True,123362)
#pause = input('pause')
