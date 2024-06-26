from functools import partial
from pathlib import Path
from shutil import copyfileobj

from requests import get
from tqdm.auto import tqdm


def download(url, filename):
    r = get(url, stream=True, allow_redirects=True)
    if r.status_code != 200:
        r.raise_for_status()  # Will only raise for 4xx codes, so...
        raise RuntimeError(f"Request to {url} returned status code {r.status_code}")
    file_size = int(r.headers.get("Content-Length", 0))

    path = Path(filename).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    desc = "(Unknown total file size)" if file_size == 0 else ""
    r.raw.read = partial(r.raw.read, decode_content=True)  # Decompress if needed
    with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
        with path.open("wb") as f:
            copyfileobj(r_raw, f)

    return path


def get_input():
    url = input("Enter URL: ")

    if not url.startswith("https://tokybook.com/"):
        print("Invalid URL!")
        return get_input()

    return url
