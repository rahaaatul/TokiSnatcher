from gazpacho import get, Soup
from urllib.parse import urlparse
from re import search
from os import makedirs, path
import os
from json5 import loads
from src.download import download

SKIP_CHAPTER = "https://file.tokybook.com/upload/welcome-you-to-tokybook.mp3"
MEDIA_URL = "https://files01.tokybook.com/audio/"
MEDIA_FALLBACK_URL = "https://files02.tokybook.com/audio/"
SLASH_REPLACE_STRING = " out of "

def get_chapters(BOOK_URL):
    html = get(BOOK_URL)

    soup = Soup(html)
    js = soup.find("script")

    for crap in js:
        match = search(r"tracks\s*=\s*(\[[^\]]+\])\s*", crap.text)
        if match:
            string = match.group(1)
            break

    json = loads(string)
    chapters = [
        {"name": x["name"], "url": x["chapter_link_dropbox"]}
        for x in json
        if x["chapter_link_dropbox"] != SKIP_CHAPTER
    ]

    o = urlparse(BOOK_URL)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    download_folder = os.path.join(current_directory, "downloads", os.path.basename(o.path))

    print(f"Download folder: {download_folder}")

    try:
        makedirs(download_folder, exist_ok=True)
    except OSError as e:
        print(f"Error creating download folder: {e}")
        return

    for item in chapters:
        try:
            download(
                MEDIA_URL + item["url"],
                path.join(download_folder, SLASH_REPLACE_STRING.join(item["name"].split("/")) + ".mp3"),
            )
            print()

        except OSError as e:
            print(f"Error creating download folder: {e}")
            return
        
        except RuntimeError:
            try:
                download(
                    MEDIA_FALLBACK_URL + item["url"],
                    path.join(download_folder, item["name"] + ".mp3"),
                )
                print()

            except Exception as e:
                print(f"An error occured: {e}")
                break

        except Exception as e:
            print(f"An error occured: {e}")
            break