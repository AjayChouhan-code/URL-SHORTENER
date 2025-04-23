"""
Unit tests for the Flask URL Shortener application.
Covers the following APIs:
- POST /shorten
- GET /<short_url>
- GET /metrics

Mocking is used to isolate service behavior for consistent, fast testing.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch
from app import app as flask_app


@pytest.fixture
def client():
    """
    Pytest fixture to initialize the Flask test client.
    Enables testing without running the server.
    """
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


def test_shorten_url_valid(client):
    """
    Test POST /shorten with a valid URL.
    Expects status 200 and a shortened URL in response.
    """
    with patch('app.url_service.shorten') as mock_shorten:
        mock_shorten.return_value = 'abc123'
        response = client.post('/shorten', json={'url': 'http://example.com'})
        assert response.status_code == 200
        data = response.get_json()
        assert 'short_url' in data['data']
        assert data['data']['short_url'].endswith('abc123')


def test_shorten_url_missing(client):
    """
    Test POST /shorten with no URL in the payload.
    Expects status 400 and appropriate error message.
    """
    response = client.post('/shorten', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] is True
    assert data['message'] == 'URL is required'


def test_redirect_to_original_url_valid(client):
    """
    Test GET /<short_url> with a valid shortened URL.
    Expects a redirect (302) to the original URL.
    """
    with patch('app.url_service.get_original_url') as mock_get:
        mock_get.return_value = 'http://example.com'
        response = client.get('/abc123')
        assert response.status_code == 302
        assert response.location == 'http://example.com'


def test_redirect_to_original_url_not_found(client):
    """
    Test GET /<short_url> with a non-existent shortened URL.
    Expects a 404 Not Found error.
    """
    with patch('app.url_service.get_original_url') as mock_get:
        mock_get.return_value = None
        response = client.get('/invalid')
        assert response.status_code == 404


def test_metrics_endpoint(client):
    """
    Test GET /metrics to return top 3 domains shortened.
    Expects correct domain count mapping in response.
    """
    with patch('app.url_service.get_top_domains') as mock_metrics:
        mock_metrics.return_value = [('example.com', 5), ('test.com', 3)]
        response = client.get('/metrics')
        assert response.status_code == 200
        assert response.get_json() == {'example.com': 5, 'test.com': 3}