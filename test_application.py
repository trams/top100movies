import application

state = application.State("test_data/movies")


def test_not_existing_one():
    assert state.get("abracadabra") == []


def test_empty_query():
    assert state.get("") == []


def test_simple_query():
    assert state.get("garcia") == ["City Lights"]
