import re
from argparse import ArgumentParser
from pathlib import Path

import requests
from bs4 import BeautifulSoup


photos_url = f"https://account.altvr.com/photos"

hh={"User-Agent":"Mozilla/5.0"}

reg = re.compile(r'/photos/(\d+)')

def get_page_photo_ids(page: int, token: str):
    url = f"https://account.altvr.com/photos/share?token={token}&page={page}"
    res = requests.get(url, headers=hh)
    soup = BeautifulSoup(res.text, 'html.parser')
    image_hrefs = [a['href'] for a in soup.find_all('a', href=reg)]
    href_matches = [reg.match(href) for href in image_hrefs]

    return list(set([m.group(1) for m in href_matches if m is not None]))


def get_full_photo_url(photo_id: str):
    url = f"{photos_url}/{photo_id}"
    res = requests.get(url, headers=hh)
    soup = BeautifulSoup(res.text, 'html.parser')

    raw_reg = re.compile(fr'https://cdn-content-ingress.altvr.com/uploads/photo/image/{photo_id}')
    links = soup.find_all('a', href=raw_reg)

    return links[0]['href']

def download_image(url: str, out_dir: Path):
    res = requests.get(url)
    if res.status_code == 200:
        file_name = url.split('/')[-1]
        out_path = out_dir / file_name
        out_path.write_bytes(res.content)




parser = ArgumentParser()
parser.add_argument('--token', required=True, type=str, help="Token from the URL when you go to https://account.altvr.com/photos/share")
parser.add_argument('--download', type=Path, help="If the program should download the photos, this specifies the path to local directory")


args = parser.parse_args()

token = args.token
download = args.download

if download is not None:
    download = (Path.cwd() / download).resolve()

    if not download.exists():
        download.mkdir(parents=True, exist_ok=True)

page_idx = 1
should_run = True
while should_run:
    photo_ids = get_page_photo_ids(page_idx, token)

    if len(photo_ids) > 0:
        for photo_id in photo_ids:
            raw_url = get_full_photo_url(photo_id)
            print(raw_url)
            if download:
                download_image(raw_url, download)

    else:
        should_run = False

    page_idx += 1
