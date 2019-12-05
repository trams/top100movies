import os

import requests
from bs4 import BeautifulSoup

import parser


def get_top1000_url(start):
    baseurl_pattern = "https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&start={}&ref_=adv_nxt"
    return baseurl_pattern.format(start)


def get_fullcredits_page(movie):
    baseurl = "https://www.imdb.com/{}fullcredits/"
    return baseurl.format(movie.link[1:])


def get_movie_uid(movie):
    parts = [item for item in movie.link.split("/") if item != ""]
    assert len(parts) == 2
    assert parts[0] == "title"
    return parts[1]


def fetch_all_movie_pages(limit=100, output_folder="data"):
    for start in range(1, limit, 50):
        url = get_top1000_url(start)
        response = requests.get(url)
        if not response.ok:
            raise Exception("Failed to fetch part of movie list starting with {}. Error: {}".format(start, response.text))
        parsed_movie_list = BeautifulSoup(response.text, "html.parser")
        for movie in parser.get_movies(parsed_movie_list):
            movie_url = get_fullcredits_page(movie)
            print("Downloading {} using {} ...".format(movie.name, movie_url))

            fullcredits = requests.get(movie_url)
            if not fullcredits.ok:
                raise Exception("Failed to fetch full credits for {}. Error: {}".format(movie.link, response.text))

            movie_uid = get_movie_uid(movie)
            with open(os.path.join(output_folder, movie_uid), "w") as f:
                f.write(fullcredits.text)


if __name__ == "__main__":
    import sys
    output_folder, limit = sys.argv[1:]
    limit = int(limit)
    fetch_all_movie_pages(limit, output_folder)
