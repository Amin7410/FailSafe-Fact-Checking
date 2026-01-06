
import pytest
from unittest.mock import MagicMock
from factcheck.utils.llmclient.base import BaseClient

@pytest.fixture
def mock_llm_client():
    """
    Returns a MagicMock that mimics a Generic LLM Client.
    """
    mock_client = MagicMock(spec=BaseClient)
    # Default behavior: return a simple string
    mock_client.call.return_value = "Mocked LLM Response"
    mock_client.construct_message_list.return_value = [{"role": "user", "content": "test"}]
    mock_client.usage = {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
    return mock_client

@pytest.fixture
def mock_config(monkeypatch):
    """
    Mocks the config loader to avoid reading real config.yaml or env vars.
    """
    mock_conf = {
        'llm': {'default_model': 'test-model'},
        'pipeline': {'retriever': 'hybrid'},
        'database': {'sqlite_path': ':memory:'}
    }
    
    # We mock the dictionary returned by config.get(key)
    # Since config uses dot notation in this project (config.get('llm.default_model')),
    # we need a side_effect to handle that.
    
    def mock_get(key, default=None):
        keys = key.split('.')
        val = mock_conf
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default

    monkeypatch.setattr("factcheck.utils.config_loader.config.get", mock_get)
    return mock_conf
