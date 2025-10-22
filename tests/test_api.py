import pytest
import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))

from fastapi.testclient import TestClient  # noqa: E402
from app.api import app  # noqa: E402

client = TestClient(app)


def setup_module():
    """Setup test environment"""
    # Ensure clean test data directory
    if os.path.exists("data/strings.json"):
        os.remove("data/strings.json")


def test_create_string():
    """Test POST /strings endpoint"""
    response = client.post("/strings", json={"value": "hello world"})
    assert response.status_code == 201
    data = response.json()
    assert data["value"] == "hello world"
    assert "id" in data
    assert "properties" in data
    assert "created_at" in data
    assert data["properties"]["length"] == 11
    assert data["properties"]["word_count"] == 2
    assert data["properties"]["is_palindrome"] is False


def test_create_duplicate_string():
    """Test creating duplicate string returns 409"""
    client.post("/strings", json={"value": "test string"})
    response = client.post("/strings", json={"value": "test string"})
    assert response.status_code == 409


def test_create_string_invalid_type():
    """Test creating string with invalid type returns 422"""
    response = client.post("/strings", json={"value": 123})
    assert response.status_code == 422


def test_get_specific_string():
    """Test GET /strings/{string_value} endpoint"""
    # First create a string
    client.post("/strings", json={"value": "get me"})

    # Then retrieve it
    response = client.get("/strings/get me")
    assert response.status_code == 200
    data = response.json()
    assert data["value"] == "get me"


def test_get_nonexistent_string():
    """Test getting non-existent string returns 404"""
    response = client.get("/strings/nonexistent")
    assert response.status_code == 404


def test_get_all_strings():
    """Test GET /strings endpoint"""
    response = client.get("/strings")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "count" in data
    assert "filters_applied" in data
    assert isinstance(data["data"], list)


def test_filter_strings():
    """Test GET /strings with filters"""
    # Create test palindrome
    client.post("/strings", json={"value": "racecar"})

    response = client.get("/strings?is_palindrome=true")
    assert response.status_code == 200
    data = response.json()
    assert data["filters_applied"]["is_palindrome"] is True
    # Check if racecar is in results
    palindromes = [
        item for item in data["data"] if item["value"] == "racecar"
    ]
    assert len(palindromes) > 0


def test_natural_language_filter():
    """Test GET /strings/filter-by-natural-language endpoint"""
    query = "palindromic strings"
    response = client.get(
        f"/strings/filter-by-natural-language?query={query}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "count" in data
    assert "interpreted_query" in data
    assert data["interpreted_query"]["original"] == "palindromic strings"


def test_delete_string():
    """Test DELETE /strings/{string_value} endpoint"""
    # Create string first
    client.post("/strings", json={"value": "delete me"})

    # Delete it
    response = client.delete("/strings/delete me")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get("/strings/delete me")
    assert response.status_code == 404


def test_delete_nonexistent_string():
    """Test deleting non-existent string returns 404"""
    response = client.delete("/strings/does not exist")
    assert response.status_code == 404


def test_palindrome_analysis():
    """Test palindrome detection"""
    # Test true palindrome
    response = client.post(
        "/strings",
        json={"value": "A man a plan a canal Panama"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["properties"]["is_palindrome"] is True

    # Test false palindrome
    response = client.post("/strings", json={"value": "not palindrome"})
    data = response.json()
    assert data["properties"]["is_palindrome"] is False


def test_character_frequency():
    """Test character frequency mapping"""
    response = client.post("/strings", json={"value": "hello"})
    data = response.json()
    freq_map = data["properties"]["character_frequency_map"]
    assert freq_map["h"] == 1
    assert freq_map["e"] == 1
    assert freq_map["l"] == 2
    assert freq_map["o"] == 1


if __name__ == "__main__":
    pytest.main([__file__])
