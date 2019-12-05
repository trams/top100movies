import collections

Movie = collections.namedtuple("Movie", ["link", "name"])
Person = collections.namedtuple("Person", ["link", "name"])


def get_movies(parsed_movie_list, expected_amount=50):
    tags = parsed_movie_list.select("div[id=main] div.article div.col-title a")
    assert len(tags) == expected_amount
    result = []
    for tag in tags:
        link = tag['href']
        name = tag.text.strip()
        result.append(Movie(link, name))
    return result


def get_movie(parsed_html):
    tags = parsed_html.select("h3[itemprop='name'] a")
    if len(tags) == 0:
        raise Exception("Failed to find a movie title")
    if len(tags) > 1:
        raise Exception("Ambiguous title")

    link = tags[0]["href"]
    name = tags[0].text
    return Movie(link, name)


def get_cast_list(parsed_html):
    result = []
    for tag in parsed_html.select("table.cast_list tr td:nth-of-type(2) a"):
        link = tag['href']
        name = tag.text.strip()
        result.append(Person(link, name))

    return result


def get_others(parsed_html):
    result = []
    selector = "div[id=fullcredits_content] table td.name a"
    for tag in parsed_html.select(selector):
        link = tag['href']
        name = tag.text.strip()
        result.append(Person(link, name))

    return result
