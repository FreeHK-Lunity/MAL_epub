import ebookmeta
from io import BytesIO
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import requests
import json
from dotenv import load_dotenv
import os
from PIL import Image

load_dotenv()
client_id = os.getenv("CLIENT_ID")
print(client_id)
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
meta = ebookmeta.get_metadata(f'{filename}')

print(meta)
'''author = meta.author_list
author2 = ''.join(author)
meta.author_list = author2
meta.set_author_list_from_string(author2)
ebookmeta.set_metadata(f'{filename}', meta)
meta = ebookmeta.get_metadata(f'{filename}')
print(meta.author_list)'''