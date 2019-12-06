import os
import json

from bs4 import BeautifulSoup

from model import *


def get_movies(parsed_movie_list, expected_amount=50):
    """Parse a movie list page and return a list of movies"""
    tags = parsed_movie_list.select("div[id=main] div.article div.col-title a")
    assert len(tags) == expected_amount
    result = []
    for tag in tags:
        link = tag['href']
        name = tag.text.strip()
        result.append(Movie(link, name))
    return result


def get_movie(parsed_html):
    """Extract a movie info from a movie full credits page"""
    tags = parsed_html.select("h3[itemprop='name'] a")
    if len(tags) == 0:
        raise Exception("Failed to find a movie title")
    if len(tags) > 1:
        raise Exception("Ambiguous title")

    link = tags[0]["href"]
    name = tags[0].text
    return Movie(link, name)


def get_cast_list(parsed_html):
    """Extract a movie cast list from a movie full credits page"""
    result = []
    for tag in parsed_html.select("table.cast_list tr td:nth-of-type(2) a"):
        link = tag['href']
        name = tag.text.strip()
        result.append(Person(link, name))

    return result


def get_others(parsed_html):
    """Extract all people involved from a movie full credits page"""
    result = []
    selector = "div[id=fullcredits_content] table td.name a"
    for tag in parsed_html.select(selector):
        link = tag['href']
        name = tag.text.strip()
        result.append(Person(link, name))

    return result


def load_all_data(folder):
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            with open(path) as f:
                parsed = BeautifulSoup(f, "html.parser")
                movie = get_movie(parsed)
                people = get_cast_list(parsed) + get_others(parsed)
                yield movie, people


def db_to_json(db, fp):
    json.dump(db, fp)


def json_to_db(fp):
    result = dict()
    obj = json.load(fp)
    if type(obj) is not dict:
        raise Exception("Json object is expected but this found: " + str(type(obj)))
    for key, value in obj.items():
        parsed_value = [Person(item[0], item[1]) for item in value]
        result[key] = parsed_value
    return result


if __name__ == "__main__":
    import sys
    try:
        from tqdm import tqdm
    except ImportError:
        def tqdm(iterator):
            return iterator

    data_folder, output_path = sys.argv[1:]
    db = dict()
    for movie, people in tqdm(load_all_data(data_folder)):
        db[movie.name] = people

    with open(output_path, "w") as f:
        db_to_json(db, f)
