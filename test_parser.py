import parser

from bs4 import BeautifulSoup


html_doc = None
with open("test_data/tt0054215_full_credits") as f:
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