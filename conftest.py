import pytest
from main import BooksCollector

@pytest.fixture(scope="module")
def collector():
    return BooksCollector()
