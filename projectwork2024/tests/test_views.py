import json
import pytest
from django.test import RequestFactory
from unittest.mock import MagicMock, patch
from projectwork2024.views import chat_response, start_new_chat, load_chat
from projectwork2024.DocStore import DocStore
from projectwork2024.Integration import Model

@pytest.fixture
def rf():
    return RequestFactory()

@pytest.fixture
def mock_doc_store():
    ds = MagicMock()
    ds.search.return_value = [("Document", 0.5)]
    return ds

@pytest.fixture
def mock_model():
    m = MagicMock()
    m.generate_response.return_value = "Generated response"
    return m

@pytest.mark.django_db
def test_chat_response(rf, mock_doc_store, mock_model, settings):
    settings.DOC_STORE = mock_doc_store
    settings.MODEL = mock_model
    request = rf.post('/chat_response', data={'user_query': 'Test query'}, content_type='application/json')
    response = chat_response(request)
    assert response.status_code == 200
    assert json.loads(response.content)['response'] == "Generated response"

@pytest.mark.django_db
def test_start_new_chat(rf, settings):
    settings.DOC_STORE = MagicMock()
    request = rf.post('/start_new_chat')
    response = start_new_chat(request)
    assert response.status_code == 200
    assert json.loads(response.content)['message'] == 'New chat started successfully.'

@pytest.mark.django_db
def test_load_chat(rf, settings):
    settings.DOC_STORE = MagicMock()
    request = rf.post('/load_chat', data={'chat_id': 1})
    with patch('views.Conversation.objects.filter') as mock_filter:
        mock_filter.return_value.order_by.return_value = [MagicMock(message='Test message', sender='user', timestamp='now')]
        response = load_chat(request, 1)
    assert response.status_code == 200
    assert json.loads(response.content)['messages'][0]['message'] == 'Test message'