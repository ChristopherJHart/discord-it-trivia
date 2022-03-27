"""House pytest fixtures for unit tests."""

import pytest
from yaml import SafeLoader, load


@pytest.fixture
def question_pool():
    """Open question pool YAML file and return contents."""
    with open("./bot/models/question_pool.yaml") as pool_file:
        yield load(pool_file, SafeLoader)
