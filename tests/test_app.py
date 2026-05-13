import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange - No setup needed
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    # Arrange
    email = "test@example.com"
    activity = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    
    # Additional check: verify participant was added
    response = client.get("/activities")
    data = response.json()
    assert email in data[activity]["participants"]


def test_signup_nonexistent_activity():
    # Arrange
    email = "test@example.com"
    nonexistent_activity = "Nonexistent"
    
    # Act
    response = client.post(f"/activities/{nonexistent_activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate():
    # Arrange
    email = "duplicate@example.com"
    activity = "Programming Class"
    
    # Act - First signup
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Act - Second signup (should fail)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up for this activity"}


def test_remove_participant():
    # Arrange
    email = "remove@example.com"
    activity = "Gym Class"
    
    # Setup: Add participant first
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity}"}
    
    # Additional check: verify participant was removed
    response = client.get("/activities")
    data = response.json()
    assert email not in data[activity]["participants"]


def test_remove_nonexistent_participant():
    # Arrange
    email = "nonexistent@example.com"
    activity = "Chess Club"
    
    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found for this activity"}


def test_remove_from_nonexistent_activity():
    # Arrange
    email = "test@example.com"
    nonexistent_activity = "Nonexistent"
    
    # Act
    response = client.delete(f"/activities/{nonexistent_activity}/participants", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}