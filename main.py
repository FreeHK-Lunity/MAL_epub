import ebooklib
from ebooklib import epub
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import requests
f = open('.env', 'r' , encoding='utf-8')
client_id = f.read()
client_id = client_id.replace('client_id = ', '')
client_id = client_id.replace("'", '')
client_id = client_id.strip()
print(client_id)
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

def main(e_book_path):
    book = epub.read_epub(f'{e_book_path}')
    e = book.get_metadata('DC', 'title')
    e = str(e)
    e = e.replace('[(\'', '')
    e = e.replace('\',)]', '')
    e = e.strip()
    req_mal = requests.get(f'https://api.myanimelist.net/v2/manga?q={e}', f'X-MAL-CLIENT-ID={client_id}' )
    print(req_mal.status_code)
main(filename)