import requests
import json
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen
from multiprocessing import Pool

# enter path where you want to save downloaded books
# BASE_PATH = Path('/Users/enderged/own-projects/yadvashem/')
BASE_PATH = Path('/Volumes/archiwa/yadvashem/')


def download_and_save(url, destination):
    with urlopen(url) as f:
        content = f.read()
    if len(content) < 100000:
        with urlopen(url + '?width=2000') as f:
            content = f.read()
    with destination.open('wb') as f:
        f.write(content)


def download_page(page_url_path):
    page_url, path = page_url_path
    page_name = '_'.join(page_url.split('/')[-2:])
    print(page_name)
    download_and_save(page_url, path / page_name)


def download_book(metadata):
    # We assume, that each title follows a pattern:
    # Testimony of [names], (...)
    # We cut everything after comma and remove "Testimony of"
    # A title that did not follow this pattern will still give some text
    print('Downloading {}'.format(metadata['Title']))
    author_name = metadata['Title'].split(',')[0]
    if author_name.startswith('Testimony of '):
        author_name = author_name[13:]
    # thanks to pathlib, this path joining will work on any OS
    path = BASE_PATH / 'O_3' / 'O_3_{}_{}'.format(metadata['fileNumber'], author_name)
    # make a folder for a new book, it's safe to run even if the folder already exists
    path.mkdir(parents=True, exist_ok=True)

    pages_list = metadata['Multimedia']

    # save book's metadata to a text file
    metadata['num_pages'] = len(pages_list)
    metadata['download_date'] = datetime.now().strftime("%Y-%m-%d")
    with (path / 'metadata.txt').open('w') as f:
        json.dump(metadata, f, indent=4)

    with Pool(10) as p:
        p.map(download_page, [(page, path) for page in pages_list])


    # pages_paths = [path / '_'.join(page_url.split('/')[-2:] for page_url in pages_list]
    #
    # for page_url in pages_list:
    #     # page name will be: number.JPG, e.g. 00032.JPG
    #     page_name = '_'.join(page_url.split('/')[-2:])
    #     print(page_name)
    #     download_and_save(page_url, path / page_name)


def get_book_metadata(book_id):
    url = 'https://documents.yadvashem.org/DocumentsWS.asmx/getDocumentDetails'
    headers = {'Content-Type': 'application/json'}
    data = {'bookId': book_id, 'langAPI': "ENG", 'detailsType': "_documentsDetails"}
    r = requests.post(url, headers=headers, json=data)
    metadata = r.json()['d']
    if '__type' in metadata.keys():
        del metadata['__type']
    if 'MoreData' in metadata.keys():
        metadata = {**metadata, **{k: v[0] for k, v in metadata['MoreData'].items()}}
        del metadata['MoreData']
    metadata = {k: v['Value'] for k, v in metadata.items()}
    metadata['Multimedia'] = [img['image'] for img in metadata['Multimedia']]

    print('{} {}'.format(metadata['Title'], metadata['fileNumber']))

    return metadata


def get_books_ids(row_num):
    url = 'https://documents.yadvashem.org/DocumentsWS.asmx/getDocumentsList'
    headers = {'Content-Type': 'application/json'}
    unique_id = "7576418634111402006"
    data = {'uniqueId': unique_id, 'langApi': "ENG", 'rowNum': row_num, 'orderBy': "BOOK_ID", 'orderType': "asc"}
    r = requests.post(url, headers=headers, json=data)


def get_all_title_and_image_lists(ids):
    res = {}
    l = len(ids)
    for i, id in enumerate(ids):
        print('Running {}/{}'.format(i, l))
        res[id] = get_book_metadata(id)     # to nie dziala
    with open('images_list.json', 'w') as f:
        json.dump(res, f)
    return res


if __name__ == '__main__':
    with open('all_ids.json', 'r') as f:
        all_ids = json.load(f)

    for book_id in all_ids[385:]:
        try:
            download_book(get_book_metadata(book_id))
        except Exception as e:
            with open('error.log', 'a') as f:
                f.write('Error downloading book {}: {}\n'.format(book_id, e))
