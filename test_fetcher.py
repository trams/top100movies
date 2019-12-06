import pytest

import fetcher
import model


def test_get_top1000_url():
    expected_output = "https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&start=51&ref_=adv_nxt"
    assert fetcher.get_top1000_url(51) == expected_output


def test_get_full_credits():
    movie = model.Movie("/title/title_id/", "Movie name")
    url = fetcher.get_fullcredits_page(movie)
    assert url == "https://www.imdb.com/title/title_id/fullcredits/"


def test_get_movie_uid():
    movie = model.Movie("/title/title_id/", "Movie name")
    assert fetcher.get_movie_uid(movie) == "title_id"


def test_get_movie_uid_fails():
    bad_movie = model.Movie("/title/first_part/second_part", "Movie name")
    with pytest.raises(AssertionError):
        fetcher.get_movie_uid(bad_movie)

    other_bad_movie = model.Movie("/not_title/some_id/", "Movie name")
    with pytest.raises(AssertionError):
        fetcher.get_movie_uid(other_bad_movie)
