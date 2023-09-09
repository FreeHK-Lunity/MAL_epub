import ebooklib
from ebooklib import epub
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import requests
'''
on9 My anime list needs to verify user on99 nd make code challenge
'''
import secrets

def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]

code_verifier = code_challenge = get_new_code_verifier()

print(len(code_verifier))
print(code_verifier)
'''
rubbish code challenge END
'''
client_id = '---' # put ur client id here
requests.get(f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={clinet_id}&code_challenge={code_challenge}&code_challenge_method=plain')
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

def main(e_book_path):
    book = epub.read_epub(f'{e_book_path}')
    e = book.get_metadata('DC', 'title')
    e = str(e)
    e = e.replace('[(\'', '')
    e = e.replace('\',)]', '')
    e = e.strip()
    req_mal = requests.get(f'https://api.myanimelist.net/v2/manga?q={e}')
    print(req_mal.status_code)
main(filename)