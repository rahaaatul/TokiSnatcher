from urllib.parse import quote

from gazpacho import Soup, get
from halo import Halo
from pick import pick


def search_book():
    SEARCH_URL = "https://tokybook.com/?s="
    spinner = Halo(text="Searching...", spinner="dots")
    query = input("Search query: ")
    spinner.start()

    html = get(SEARCH_URL + quote(query))
    soup = Soup(html)

    not_found = soup.find("h1", {"class": "entry-title"})

    if not_found:
        if not_found.text == "Nothing Found":
            print("No results found!")
            return search_book()

    results = soup.find("h2", {"class": "entry-title"})

    titles = [x.text for x in results]
    urls = [x.find("a").attrs.get("href") for x in results]

    spinner.stop()
    _, idx = pick(titles, "Search results:")
    return urls[idx]
