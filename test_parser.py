import parser

import io

from bs4 import BeautifulSoup


html_doc = None
with open("test_data/movies/tt0054215_full_credits") as f:
    html_doc = f.read()


movie_list_html = None
with open("test_data/movie_list") as f:
    movie_list_html = f.read()

parsed_html = BeautifulSoup(html_doc, "html.parser")
parsed_movie_list = BeautifulSoup(movie_list_html, "html.parser")


def test_get_movies():
    movies = parser.get_movies(parsed_movie_list)
    assert len(movies) == 50
    psycho_movie = movies[1]
    assert psycho_movie.name == "Psycho"
    assert psycho_movie.link == "/title/tt0054215/"


def test_get_movie():
    movie = parser.get_movie(parsed_html)
    assert movie.name == "Psycho"
    assert movie.link == "/title/tt0054215/"


def test_get_cast_list():
    cast_list = parser.get_cast_list(parsed_html)
    assert len(cast_list) == 36
    assert cast_list[0].link == "/name/nm0000578/"
    assert cast_list[0].name == "Anthony Perkins"


def test_get_others():
    others = parser.get_others(parsed_html)
    assert len(others) == 80
    assert others[0].name == "Alfred Hitchcock"
    assert others[-1].name == "Dolores Stockton"


def test_load_all_data():
    by_family_name = dict()
    db = dict()
    for movie, people in parser.load_all_data("test_data/movies"):
        db[movie.name] = people
        for person in people:
            family_name = person.name.split(" ")[-1]
            by_family_name.setdefault(family_name, set()).add(movie.name)

    assert len(db) == 2
    people = db["Psycho"]
    assert len(people) == 116
    assert by_family_name["Hitchcock"] == set(["Psycho"])
    assert by_family_name["Garcia"] == set(["City Lights"])


def test_ser_deser():
    db = dict()
    for movie, people in parser.load_all_data("test_data/movies"):
        db[movie.name] = people

    stream = io.StringIO()
    parser.db_to_json(db, stream)
    stream.seek(0)
    newdb = parser.json_to_db(stream)

    assert newdb == db
