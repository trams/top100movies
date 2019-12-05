import collections

Movie = collections.namedtuple("Movie", ["link", "name"])
Person = collections.namedtuple("Person", ["link", "name"])


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
    for tag in parsed_html.select("table.cast_list tr td:nth-of-type(2)"):
        link = tag.a['href']
        name = tag.a.text.strip()
        result.append(Person(link, name))

    return result
