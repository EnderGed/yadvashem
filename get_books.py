from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

# enter path where you want to save downloaded books
BASE_PATH = Path('/Users/enderged/own-projects/yadvashem/')


def download_and_save(url, destination):
    with urlopen(url) as f:
        content = f.read()
    with destination.open('wb') as f:
        f.write(content)


def download_book(catalog_id, yadvashem_id, title, pages_list):
    # We assume, that each title follows a pattern:
    # Testimony of [names], (...)
    # We cut everything after comma and remove "Testimony of"
    # A title that did not follow this pattern will still give some text
    author_name = title.split(',')[0]
    if author_name.starts_with('Testimony of '):
        author_name = author_name[13:]
    # thanks to pathlib, this path joining will work on any OS
    path = BASE_PATH / '{}-{}'.format(catalog_id, author_name)
    # make a folder for a new book, it's safe to run even if the folder already exists
    path.mkdir(parents=True, exist_ok=True)

    # save book's metadata to a text file
    with (path / 'metadata.txt').open('w') as f:
        f.write('yadvashem_id:  {}\n'.format(yadvashem_id))
        f.write('catalog_id:    {}\n'.format(catalog_id))
        f.write('title:         {}\n'.format(title))
        f.write('num_pages:     {}\n'.format(len(pages_list)))
        f.write('download_date: {}\n'.format(datetime.now().strftime("%Y-%m-%d")))

    for page_url in pages_list:
        # page name will be: number.JPG, e.g. 00032.JPG
        page_name = page_url.split('/')[-1]
        download_and_save(page_url, path / page_name)
