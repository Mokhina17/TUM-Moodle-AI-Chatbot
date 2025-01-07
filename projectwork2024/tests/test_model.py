import pytest
from unittest.mock import MagicMock
from projectwork2024.Integration import Model

@pytest.fixture
def model():
    m = Model()
    m.client = MagicMock()
    return m

def test_generate_response(model):
    model.client.chat.completions.create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="Response"))])
    response = model.generate_response("What is Django?", [("Relevant doc", 0.5)])
    assert response == "Response"