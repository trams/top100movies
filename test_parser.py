import parser

from bs4 import BeautifulSoup


html_doc = None
with open("test_data/tt0054215_full_credits") as f:
    html_doc = f.read()

parsed_html = BeautifulSoup(html_doc, 'html.parser')


def test_get_movie():
    movie = parser.get_movie(parsed_html)
    assert movie.name == "Psycho"
    assert movie.link == "/title/tt0054215/"


def test_get_cast_list():
    cast_list = parser.get_cast_list(parsed_html)
    assert len(cast_list) == 36
    assert cast_list[0].link == "/name/nm0000578/"
    assert cast_list[0].name == "Anthony Perkins"
