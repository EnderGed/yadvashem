import requests
import json

def get_book_title_and_image_list(book_id):
   url = 'https://documents.yadvashem.org/DocumentsWS.asmx/getDocumentDetails'
   headers = {'Content-Type': 'application/json'}
   data = {'bookId': book_id, 'langAPI': "ENG", 'detailsType': "_documentsDetails"}
   r = requests.post(url, headers=headers, json=data)
   title = r.json()['d']['Title']['Value']
   entries = r.json()['d']['Multimedia']['Value']
   images = [entry['image'] for entry in entries]
   return title, images

def get_books_ids(row_num):
   url = 'https://documents.yadvashem.org/DocumentsWS.asmx/getDocumentsList'
   headers = {'Content-Type': 'application/json'}
   unique_id = "7576418634111402006"
   data = {'uniqueId': unique_id, 'langApi': "ENG", 'rowNum': row_num, 'orderBy': "BOOK_ID", 'orderType': "asc"}
   r = requests.post(url, headers=headers, json=data)
   
def get_all_title_and_image_lists():
   res = {}
   l = len(ids)
   for i, id in enumerate(ids):
      print('Running {}/{}'.format(i, l))
      res[id] = get_book_title_and_image_list(id)
   with open('images_list.json', 'w') as f:
      json.dump(res, f)
   return res

