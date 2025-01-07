import pytest
from unittest.mock import patch, MagicMock
from projectwork2024.DocStore import DocStore

@pytest.fixture
def doc_store():
    ds = DocStore()
    ds.model = MagicMock()
    ds.index = MagicMock()
    return ds

def test_search(doc_store):
    doc_store.index.search.return_value = ([0.0], [0])
    doc_store.documents = ["Document 1"]
    results = doc_store.search("query", k=1)
    assert len(results) == 1
    assert results[0][0] == "Document 1"