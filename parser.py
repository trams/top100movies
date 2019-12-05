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
