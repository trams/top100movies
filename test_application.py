import application

state = application.State("test_data/movies.json")


def test_not_existing_one():
    assert state.naive_get("abracadabra") == []
    assert state.naive_get("abracadabra") == []


def test_empty_query():
    assert state.naive_get("") == []
    assert state.get("") == []


def test_simple_query():
    assert state.naive_get("garcia") == ["City Lights"]
    assert state.get("garcia") == ["City Lights"]


def test_repeated_word():
    assert state.naive_get("garcia garcia") == ["City Lights"]
    assert state.get("garcia garcia") == ["City Lights"]
